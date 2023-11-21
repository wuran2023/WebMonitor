from django.apps import AppConfig
from django.db.utils import OperationalError
from apscheduler.schedulers.background import BackgroundScheduler

class TaskConfig(AppConfig):
    name = 'task'
    verbose_name = '任务管理'

    scheduler = BackgroundScheduler()

    def ready(self):
        self.scheduler.add_job(
            self.start_tasks,
            'interval',
            minutes=10,  # 每隔4小时运行一次
        )
        self.scheduler.start()

    def start_tasks(self):
        try:
            from .models import TaskStatus, Task, RSSTask
            from task.utils.scheduler import add_job, monitor

            tasks_to_start = TaskStatus.objects.filter(task_status=0)
            for task_status in tasks_to_start:
                if task_status.task_type == 'html':
                    task = Task.objects.get(id=task_status.task_id)
                    add_job(task.id, task.frequency, type='html')
                elif task_status.task_type == 'rss':
                    task = RSSTask.objects.get(id=task_status.task_id)
                    add_job(task.id, task.frequency, type='rss')
                  
        except OperationalError:
            print('数据库尚未准备好')
            pass
