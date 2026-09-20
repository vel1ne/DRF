import os
from celery import Celery


# Установка переменной окружения для Django from django.conf import settings
os.environ.setdefault('DJANGO_SETTING_MOUDLE', 'config.settings')

app = Celery('config')

# Использование строки здесь озачает, что worker не должен сериализировать
# объект конфигурации для дочерних процессов.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка задач из всех зарегистрированных Django apps/
app.autodiscover_tasks()


@app.task(blind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
