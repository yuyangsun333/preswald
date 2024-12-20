from click.testing import CliRunner
from preswald.cli import cli


def test_init_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "test_project"])
    assert result.exit_code == 0
    assert "Initialized a new Preswald project" in result.output


def test_run_command_missing_script():
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "missing.py"])
    assert result.exit_code == 0
    assert "Error: Script 'missing.py' not found." in result.output


def test_deploy_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["deploy", "--port", "9000"])
    assert result.exit_code == 0
    assert "Deploying app locally on http://localhost:9000" in result.output
