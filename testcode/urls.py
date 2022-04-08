from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', code, name='home'),
    path('tasks/', tasks, name='tasks'),
    path('task/<task_name>/', task, name='task'),
    path('ajax', ajax, name='ajax'),
]
