from django.urls import path, include

from gate_log import views

urlpatterns = [
    path('branches', views.branches, name='branches'),
    path('gates', views.gates, name='gates'),
    path('peoplecount', views.peoplecount, name='peoplecount'),
    path('peoplecount_sum', views.peoplecount_sum, name='peoplecount_sum'),
    path('people_count_hour', views.people_count_hour, name='peoplecount_hour'),
    path('people_count_day', views.people_count_day, name='peoplecount_day'),
    path('gate_log', views.alarms, name='gate_log'),
]
