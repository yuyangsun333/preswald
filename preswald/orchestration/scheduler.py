from apscheduler.schedulers.background import BackgroundScheduler

def schedule_workflow(workflow, trigger, **trigger_args):
    """
    Schedule a workflow to run based on a trigger (e.g., interval, cron).
    
    Args:
        workflow (callable): The workflow function to execute.
        trigger (str): The type of trigger (e.g., 'interval', 'cron').
        **trigger_args: Additional arguments for the trigger (e.g., hours, minutes).
    
    Returns:
        BackgroundScheduler: The scheduler object.
    """
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(workflow, trigger, **trigger_args)
        scheduler.start()
        print(f"Workflow scheduled with trigger: {trigger}, args: {trigger_args}")
        return scheduler
    except Exception as e:
        print(f"Error scheduling workflow: {e}")
        raise
