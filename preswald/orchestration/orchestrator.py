def run_workflow(steps):
    """
    Run a sequence of steps in a workflow.
    
    Args:
        steps (list): A list of callables (functions) to execute in order.
    
    Returns:
        None
    """
    try:
        for step in steps:
            print(f"Executing step: {step.__name__}")
            step()
        print("Workflow completed successfully.")
    except Exception as e:
        print(f"Error during workflow execution: {e}")
        raise
