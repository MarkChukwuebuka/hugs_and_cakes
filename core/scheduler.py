from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger


def set_task_to_run(task, schedule_date=None, cron_task=False, *args, **kwargs):
    """
    _ = set_task_to_run(task=send_password_reset, email=email, first_name=first_name, otp=otp)
    _ = set_task_to_run(task=send_password_reset, cron_task=True, cron="min hr day month day_of_week timezone",
    email=email, first_name=first_name, otp=otp)

    :param cron_task: True if a cron function
    :param schedule_date: Time to run the task
    :param task: function to run
    :param args:
    :param kwargs: arguments to insert into function
    :return:
    """
    scheduler = BackgroundScheduler()

    if schedule_date:
        trigger = DateTrigger(run_date=schedule_date)
    elif cron_task:
        trigger = CronTrigger.from_crontab(kwargs.pop('cron'))
    else:
        trigger = None

    scheduler.add_job(
        func=task,
        trigger=trigger,
        args=args,
        kwargs=kwargs
    )
    scheduler.start()