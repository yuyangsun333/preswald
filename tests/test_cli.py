import os
import pytest
from click.testing import CliRunner
from preswald.cli import cli  # Import the CLI entry point

# Initialize the CLI Runner
runner = CliRunner()

def test_cli_version():
    """Test the --version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "Preswald CLI Version" in result.output

def test_init_command(tmp_path):
    """Test the init command for creating project structure."""
    project_name = tmp_path / "test_project"
    result = runner.invoke(cli, ["init", str(project_name)])
    assert result.exit_code == 0
    assert f"Initialized new Preswald project: {project_name}" in result.output
    assert (project_name / "ingestion").exists()
    assert (project_name / "transformations").exists()

def test_pipeline_run_command():
    """Test the pipeline_run command."""
    # Simulate a pipeline execution
    result = runner.invoke(cli, ["pipeline_run", "test_pipeline"])
    assert result.exit_code == 0
    assert "Running pipeline: test_pipeline" in result.output
    assert "Pipeline execution completed successfully." in result.output

def test_run_command():
    """Test the run command for starting a server."""
    result = runner.invoke(cli, ["run"], input="Ctrl+C")
    assert result.exit_code == 0 or result.exit_code == 1
    assert "Starting local server..." in result.output

def test_deploy_command():
    """Test the deploy command."""
    result = runner.invoke(cli, ["deploy", "--prod"])
    assert result.exit_code == 0
    assert "Deploying project to production environment..." in result.output

def test_api_generate_command():
    """Test the api_generate command."""
    result = runner.invoke(cli, ["api_generate", "sales_summary"])
    assert result.exit_code == 0
    assert "Generating API for model: sales_summary" in result.output
    assert "API endpoint generated" in result.output

def test_debug_command():
    """Test the debug command."""
    result = runner.invoke(cli, ["debug"])
    assert result.exit_code == 0
    assert "Starting interactive debug mode..." in result.output
