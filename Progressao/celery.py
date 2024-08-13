import os
from celery import Celery

# Defina o nome do projeto Django como o nome do Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')

app = Celery('seu_projeto')

# Use configurações do Django para o Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregue as tarefas do Celery a partir de todos os arquivos tasks.py
app.autodiscover_tasks()
