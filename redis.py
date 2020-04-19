from app import app
from flask_apscheduler import APScheduler
from app.service import task

#created Schedular to schedule our back and expire removal task to perform in every 60 seconds
scheduler = APScheduler()
scheduler.add_job(id='Scheduled task',func=task,trigger='interval',seconds=60)
scheduler.start()

