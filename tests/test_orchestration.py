from preswald.orchestration import run_workflow, log_message
from unittest.mock import MagicMock

def test_run_workflow():
    step_one = MagicMock()
    step_two = MagicMock()
    
    steps = [step_one, step_two]
    run_workflow(steps)
    
    step_one.assert_called_once()
    step_two.assert_called_once()

def test_log_message(caplog):
    log_message("info", "Test info message")
    assert "Test info message" in caplog.text
