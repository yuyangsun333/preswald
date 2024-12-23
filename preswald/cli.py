import os
import click
from preswald.server import start_server


@click.group()
def cli():
    """
    Preswald CLI - A lightweight framework for interactive data apps.
    """
    pass


@cli.command()
@click.argument("name", default="preswald_project")
def init(name):
    """
    Initialize a new Preswald project.

    This creates a directory with boilerplate files like `hello.py` and `config.toml`.
    """
    try:
        os.makedirs(name, exist_ok=True)

        # Create boilerplate files
        with open(os.path.join(name, "hello.py"), "w") as f:
            f.write(
                '''from preswald import text

text("# Welcome to Preswald!")
text("This is your first app. 🎉")
'''
            )
        with open(os.path.join(name, "config.toml"), "w") as f:
            f.write(
                '''
[project]
title = "Preswald Project"
version = "0.1.0"
port = 8501

[theme.color]
primary = "#4CAF50"
secondary = "#FFC107"
background = "#FFFFFF"
text = "#000000"

[theme.font]
family = "Arial, sans-serif"
size = "16px"
'''
            )
        with open(os.path.join(name, "secrets.toml"), "w") as f:
            f.write("# Add your secrets (e.g., API keys) here.\n")
        with open(os.path.join(name, ".gitignore"), "w") as f:
            f.write("secrets.toml\n")
        with open(os.path.join(name, "README.md"), "w") as f:
            f.write("README.md\n")

        click.echo(f"Initialized a new Preswald project in '{name}/'")
    except Exception as e:
        click.echo(f"Error initializing project: {e}")


@cli.command()
@click.argument("script", default="hello.py")
@click.option("--port", default=8501, help="Port to run the server on.")
def run(script, port):
    """
    Run a Preswald app.

    By default, it runs the `hello.py` script on localhost:8501.
    """
    if not os.path.exists(script):
        click.echo(f"Error: Script '{script}' not found.")
        return

    click.echo(f"Running '{script}' on http://localhost:{port}")
    start_server(script=script, port=port)


@cli.command()
@click.option("--port", default=8501, help="Port for local deployment.")
def deploy(port):
    """
    Deploy your Preswald app locally.

    This allows you to share the app within your local network.
    """
    try:
        click.echo(f"Deploying app locally on http://localhost:{port}...")
        start_server(port=port)
    except Exception as e:
        click.echo(f"Error deploying app: {e}")


if __name__ == "__main__":
    cli()  # Ensures the CLI is callable when executed directly
