from django.urls import path, include

from gate_log import views

urlpatterns = [
    path('branches', views.branches, name='branches'),
    path('peoplecount', views.peoplecount, name='peoplecount'),
    path('peoplecount_sum', views.peoplecount_sum, name='peoplecount_sum'),
    path('gate_log', views.alarms, name='gate_log'),
]
