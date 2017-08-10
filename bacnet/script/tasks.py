from NAEInteract1 import main, findNAE, close
import sched, time
from bacnet.celery import app
from celery.schedules import crontab


def pull_data(sender, **kwargs):
    sender.add_periodic_task(100.0, main.s(), name='pull_data')