from django.urls import path

from monitor.views import WorkersView, TasksView

urlpatterns = [
    path('workers/', WorkersView.as_view(), name='workers'),
    path('tasks/', TasksView.as_view(), name='tasks'),
]
