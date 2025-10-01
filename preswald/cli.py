import os
import sys
import tempfile
from pathlib import Path

import click

from preswald.engine.telemetry import TelemetryService

# --- Optional pretty output with Rich ---
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    _RICH = True
    _CONSOLE = Console()
except Exception:
    _RICH = False
    _CONSOLE = None


def _human_bytes(n: int) -> str:
    """Convert a byte count into a human-readable string."""
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    x = float(n)
    while x >= 1024 and i < len(units) - 1:
        x /= 1024.0
        i += 1
    return f"{x:.1f} {units[i]}"


def _render_deploy_summary(meta: dict, force_plain: bool = False) -> None:
    """
    Pretty-print a deploy/export summary.

    meta keys (fill what you have):
      - project, outdir, index, assets, size_bytes, elapsed
    """
    use_rich = _RICH and (not force_plain) and sys.stdout.isatty()

    project = str(meta.get("project", ""))
    outdir = str(meta.get("outdir", ""))
    index = str(meta.get("index", ""))
    assets = str(meta.get("assets", ""))
    size = _human_bytes(int(meta.get("size_bytes", 0)))
    elapsed = meta.get("elapsed", None)
    elapsed_str = (
        f"{elapsed:.2f}s"
        if isinstance(elapsed, (int, float))
        else (str(elapsed) if elapsed else "")
    )

    if use_rich:
        _CONSOLE.rule("[bold]Preswald Deploy[/bold]")
        tbl = Table(expand=True)
        tbl.add_column("Item", no_wrap=True)
        tbl.add_column("Value")

        rows = [
            ("Project", project),
            ("Output Dir", outdir),
            ("Index File", index),
            ("Assets", assets),
            ("Bundle Size", size),
            ("Duration", elapsed_str),
        ]
        for k, v in rows:
            if v:
                tbl.add_row(k, v)

        _CONSOLE.print(tbl)
        _CONSOLE.print(Panel.fit("Deployed/Exported successfully", title="Status"))
    else:
        print("=" * 12 + " Preswald Deploy " + "=" * 12)
        if project:
            print(f"Project     : {project}")
        if outdir:
            print(f"Output Dir  : {outdir}")
        if index:
            print(f"Index File  : {index}")
        if assets:
            print(f"Assets      : {assets}")
        print(f"Bundle Size : {size}")
        if elapsed_str:
            print(f"Duration    : {elapsed_str}")


# Create a temporary directory for IPC
TEMP_DIR = os.path.join(tempfile.gettempdir(), "preswald")
os.makedirs(TEMP_DIR, exist_ok=True)

# Initialize telemetry service
telemetry = TelemetryService()


@click.group()
@click.version_option()
def cli():
    """
    Preswald CLI - A lightweight framework for interactive data apps.
    """
    pass


def _create_default_init_files(target_dir: str, project_slug: str):
    """Create default project files in the target directory using templates."""
    from importlib.resources import as_file, files

    # hello.py
    with as_file(files("preswald").joinpath("templates/hello.py.template")) as path:
        with open(path) as f:
            hello_content = f.read()
        with open(os.path.join(target_dir, "hello.py"), "w") as f:
            f.write(hello_content)

    # preswald.toml
    with as_file(
        files("preswald").joinpath("templates/preswald.toml.template")
    ) as path:
        with open(path) as f:
            toml_content = f.read().format(project_slug=project_slug)
        with open(os.path.join(target_dir, "preswald.toml"), "w") as f:
            f.write(toml_content)

    # secrets.toml
    with as_file(files("preswald").joinpath("templates/secrets.toml.template")) as path:
        with open(path) as f:
            secrets_content = f.read()
        with open(os.path.join(target_dir, "secrets.toml"), "w") as f:
            f.write(secrets_content)

    # data/sample.csv
    os.makedirs(os.path.join(target_dir, "data"), exist_ok=True)
    with as_file(files("preswald").joinpath("templates/sample.csv.template")) as path:
        with open(path) as f:
            sample_data = f.read()
        with open(os.path.join(target_dir, "data", "sample.csv"), "w") as f:
            f.write(sample_data)


@cli.command()
@click.argument("name", default="preswald_project")
def init(name):
    """
    Initialize a new Preswald project.
    Creates a directory with basic project structure.
    """
    from preswald.utils import generate_slug
    import shutil
    from importlib.resources import as_file, files

    try:
        os.makedirs(name, exist_ok=True)
        os.makedirs(os.path.join(name, "images"), exist_ok=True)
        os.makedirs(os.path.join(name, "data"), exist_ok=True)

        # Generate a unique slug for the project
        project_slug = generate_slug(name)

        # Copy default branding files
        with as_file(files("preswald").joinpath("static/favicon.ico")) as path:
            shutil.copy2(path, os.path.join(name, "images", "favicon.ico"))

        with as_file(files("preswald").joinpath("static/logo.png")) as path:
            shutil.copy2(path, os.path.join(name, "images", "logo.png"))

        # Create basic project files
        _create_default_init_files(name, project_slug)

        # Track initialization
        telemetry.track_command(
            "init",
            {
                "project_name": name,
                "project_slug": project_slug,
            },
        )

        click.echo(f"Initialized a new Preswald project in '{name}/' 🎉!")
        click.echo(f"Project slug: {project_slug}")
    except Exception as e:
        click.echo(f"Error initializing project: {e} ❌")


@cli.command()
@click.option("--port", default=8501, help="Port to run the server on.")
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default=None,
    help="Set the logging level (overrides config file)",
)
@click.option(
    "--disable-new-tab",
    is_flag=True,
    default=False,
    help="Disable automatically opening a new browser tab",
)
def run(port, log_level, disable_new_tab):
    """
    Run a Preswald app from the current directory.

    Looks for preswald.toml in the current directory and runs the script specified in the entrypoint.
    """
    config_path = "preswald.toml"
    if not os.path.exists(config_path):
        click.echo("Error: preswald.toml not found in current directory. ❌")
        click.echo("Make sure you're in a Preswald project directory.")
        return

    import tomli
    from preswald.main import start_server
    from preswald.utils import configure_logging, read_port_from_config

    try:
        with open(config_path, "rb") as f:
            config = tomli.load(f)
    except Exception as e:
        click.echo(f"Error reading preswald.toml: {e} ❌")
        return

    if "project" not in config or "entrypoint" not in config["project"]:
        click.echo(
            "Error: entrypoint not defined in preswald.toml under [project] section. ❌"
        )
        return

    script = config["project"]["entrypoint"]
    if not os.path.exists(script):
        click.echo(f"Error: Entrypoint script '{script}' not found. ❌")
        return

    log_level = configure_logging(config_path=config_path, level=log_level)
    port = read_port_from_config(config_path=config_path, port=port)

    # Track run command
    telemetry.track_command(
        "run",
        {
            "script": script,
            "port": port,
            "log_level": log_level,
            "disable_new_tab": disable_new_tab,
        },
    )

    url = f"http://localhost:{port}"
    click.echo(f"Running '{script}' on {url} with log level {log_level}  🎉!")

    try:
        if not disable_new_tab:
            import webbrowser

            webbrowser.open(url)

        start_server(script=script, port=port)
    except Exception as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument("script", default=None, required=False)
@click.option(
    "--target",
    type=click.Choice(["local", "gcp", "aws"], case_sensitive=False),
    default="local",
    help="Target platform for deployment.",
)
@click.option("--port", default=8501, help="Port for deployment.")
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default=None,
    help="Set the logging level (overrides config file)",
)
def deploy(script, target, port, log_level):
    """
    Deploy your Preswald app.

    This allows you to share the app within your local network or deploy to production.
    If no script is provided, it will use the entrypoint defined in preswald.toml.
    """
    try:
        if target == "aws":
            click.echo(
                "\nWe're working on supporting AWS soon! Please enjoy some ☕ and 🍌 in the meantime"
            )
            return

        # First try to read from preswald.toml in current directory
        config_path = "preswald.toml"
        if os.path.exists(config_path):
            import tomli

            try:
                with open(config_path, "rb") as f:
                    config = tomli.load(f)
                if "project" in config and "entrypoint" in config["project"]:
                    script = script or config["project"]["entrypoint"]
            except Exception as e:
                click.echo(f"Warning: Error reading preswald.toml: {e}")
                # Continue with provided script argument if config reading fails

        if not script:
            click.echo(
                "Error: No script specified and no entrypoint found in preswald.toml ❌"
            )
            click.echo(
                "Either provide a script argument or define entrypoint in preswald.toml"
            )
            return

        if not os.path.exists(script):
            click.echo(f"Error: Script '{script}' not found. ❌")
            return

        from preswald.deploy import deploy as deploy_app
        from preswald.utils import configure_logging, read_port_from_config

        config_path = os.path.join(os.path.dirname(script), "preswald.toml")
        log_level = configure_logging(config_path=config_path, level=log_level)
        port = read_port_from_config(config_path=config_path, port=port)

        # Track deployment
        telemetry.track_command(
            "deploy",
            {
                "script": script,
                "target": target,
                "port": port,
                "log_level": log_level,
            },
        )

        url = deploy_app(script, target, port=port)

        # Deployment Success Message
        success_message = f"""

        ===========================================================

        🎉 Deployment successful! ✅

        🌐 Your app is live and running at:
        {url}

        💡 Next Steps:
            - Open the URL above in your browser to view your app

        🚀 Deployment Summary:
            - App: {script}
            - Environment: {target}
            - Port: {port}
        """

        click.echo(click.style(success_message, fg="green"))

    except Exception as e:
        click.echo(click.style(f"Deployment failed: {e!s} ❌", fg="red"))
        sys.exit(1)


@cli.command()
@click.option(
    "--target",
    type=click.Choice(["local", "gcp", "aws"], case_sensitive=False),
    default="local",
    help="Target platform to stop the deployment from.",
)
def stop(target):
    """
    Stop the currently running deployment.

    This command must be run from the same directory as your Preswald app.
    """
    try:
        from preswald.deploy import cleanup_gcp_deployment

        # Track stop command
        telemetry.track_command("stop", {"target": target})
        config_path = "preswald.toml"
        if not os.path.exists(config_path):
            click.echo("Error: preswald.toml not found in current directory. ❌")
            click.echo("Make sure you're in a Preswald project directory.")
            return

        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        if target == "gcp":
            try:
                click.echo("Starting GCP deployment cleanup... 🧹")
                for status_update in cleanup_gcp_deployment(current_dir):
                    status = status_update.get("status", "")
                    message = status_update.get("message", "")

                    if status == "error":
                        click.echo(click.style(f"❌ {message}", fg="red"))
                    elif status == "success":
                        click.echo(click.style(f"✅ {message}", fg="green"))
                    else:
                        click.echo(f"i {message}")
                click.echo(
                    click.style(
                        "✅ GCP deployment cleaned up successfully!", fg="green"
                    )
                )
            except Exception as e:
                click.echo(click.style(f"❌ GCP cleanup failed: {e!s}", fg="red"))
                sys.exit(1)
        else:
            from preswald.deploy import stop_local_deployment

            stop_local_deployment(current_dir)
            click.echo("Deployment stopped successfully. 🛑 ")
    except Exception:
        sys.exit(1)


@cli.command()
@click.pass_context
def tutorial(ctx):
    """
    Run the Preswald tutorial app.

    This command runs the tutorial app located in the package's tutorial directory.
    """
    import preswald

    package_dir = os.path.dirname(preswald.__file__)
    tutorial_dir = os.path.join(package_dir, "tutorial")

    if not os.path.exists(tutorial_dir):
        click.echo(f"Error: Tutorial directory '{tutorial_dir}' not found. ❌")
        click.echo("👉 The tutorial files may be missing from your installation.")
        return

    # Track tutorial command
    telemetry.track_command("tutorial", {})

    click.echo("🚀 Launching the Preswald tutorial app! 🎉")

    # Save current directory
    current_dir = os.getcwd()
    try:
        # Change to tutorial directory
        os.chdir(tutorial_dir)
        # Invoke the 'run' command from the tutorial directory
        ctx.invoke(run, port=8501)
    finally:
        # Change back to original directory
        os.chdir(current_dir)


@cli.command()
@click.option(
    "--format",
    type=click.Choice(["pdf", "html"]),
    required=True,
    help="Export format - pdf creates a static report, html creates an interactive web app",
)
@click.option("--output", type=click.Path(), help="Path to the output directory")
@click.option(
    "--client",
    type=click.Choice(["auto", "websocket", "postmessage", "comlink"]),
    default="comlink",
    help="Communication client to use - auto will choose based on context",
)
def export(format, output, client):
    """Export the current Preswald app as a PDF report or HTML app."""
    # Check for preswald.toml and get entrypoint
    config_path = "preswald.toml"
    if not os.path.exists(config_path):
        click.echo("Error: preswald.toml not found in current directory. ❌")
        click.echo("Make sure you're in a Preswald project directory.")
        return

    import tomli

    try:
        with open(config_path, "rb") as f:
            config = tomli.load(f)
        if "project" not in config or "entrypoint" not in config["project"]:
            click.echo(
                "Error: entrypoint not defined in preswald.toml under [project] section. ❌"
            )
            return
        script = config["project"]["entrypoint"]
    except Exception as e:
        click.echo(f"Error reading preswald.toml: {e} ❌")
        return

    if not os.path.exists(script):
        click.echo(f"Error: Entrypoint script '{script}' not found. ❌")
        return

    if format == "pdf":
        output_path = output or "preswald_report.pdf"
        click.echo(f"📄 Rendering '{script}'...")

        from preswald.main import render_once
        from preswald.utils import export_app_to_pdf

        layout = render_once(script)

        click.echo(
            f"✅ Render complete. Found {len(layout['rows'])} rows of components."
        )

        component_ids = []
        for row in layout["rows"]:
            for component in row:
                cid = component.get("id")
                ctype = component.get("type")
                if cid and ctype:
                    component_ids.append({"id": cid, "type": ctype})

        # Pass the component IDs to the export function
        export_app_to_pdf(component_ids, output_path)

        click.echo(f"\n✅ Export complete. PDF saved to: {output_path}")

    elif format == "html":
        # Create output directory
        output_dir = output or "preswald_export"

        click.echo(f"📦 Exporting '{script}' to HTML...")

        try:
            from preswald.utils import prepare_html_export

            # Prepare HTML export (writes index.html, project_fs.json, assets/)
            prepare_html_export(
                script_path=script,
                output_dir=output_dir,
                project_root_dir=".",
                client_type=client,
            )

            click.echo(
                f"""
✨ Export complete! Your interactive HTML app is ready:

   📁 {output_dir}/
      ├── index.html           # The main HTML file
      ├── project_fs.json      # Your project files
      └── assets/              # Required JavaScript and CSS

Note: The app needs to be served via HTTP server - opening index.html directly won't work.
"""
            )

            # ---- Pretty summary right after success echo ----
            outdir = Path(output_dir)
            index_html = outdir / "index.html"
            assets_dir = outdir / "assets"

            # Friendly project name from config; fallback to folder name
            project_name = ""
            try:
                project_name = (config.get("project", {}) or {}).get("name") or ""
            except Exception:
                project_name = ""
            if not project_name:
                project_name = Path.cwd().name

            meta = {
                "project": project_name,
                "outdir": str(outdir.resolve()),
                "index": str(index_html.resolve()) if index_html.exists() else "",
                "assets": sum(1 for _ in assets_dir.rglob("*"))
                if assets_dir.exists()
                else 0,
                "size_bytes": sum(
                    f.stat().st_size for f in outdir.rglob("*") if f.is_file()
                ),
                "elapsed": None,  # fill if you add timing later
            }

            _render_deploy_summary(meta)

        except Exception as e:
            click.echo(f"❌ Export failed: {e!s}")
            return


if __name__ == "__main__":
    cli()
