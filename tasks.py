from celery import Celery
from celery.utils.log import get_task_logger

# Create the celery app and get the logger
#celery_app = Celery('tasks', broker='pyamqp://guest@rabbit//')
celery_app = Celery('tasks', broker='pyamqp://guest:guest@localhost:5672/')
logger = get_task_logger(__name__)


@celery_app.task
def show_resume(x):
   res = x
   logger.info("show resume %s" % (x))
   return res

    
