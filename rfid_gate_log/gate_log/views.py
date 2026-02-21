import datetime
from zoneinfo import ZoneInfo

from django.http import JsonResponse
from django.shortcuts import render
from gate_log import models
from django.db.models import Sum
from django.conf import settings


def _grafana_time(request):
    tz = ZoneInfo(settings.TIME_ZONE)
    time_from = datetime.datetime.fromisoformat(request.GET.get('from')).astimezone(tz).replace(tzinfo=None)
    time_to = datetime.datetime.fromisoformat(request.GET.get('to')).astimezone(tz).replace(tzinfo=None)
    return time_from, time_to


def branches(request):
    return JsonResponse(list(models.Branch.objects.all().values_list('name', flat=True)), safe=False)


def peoplecount(request):
    time_from, time_to = _grafana_time(request)
    branch = request.GET.get('branch')
    records = models.PeopleCounter.objects.filter(date__gte=time_from, date__lte=time_to, gate__branch__name=branch)
    return JsonResponse(list(records.values()), safe=False)


def peoplecount_sum(request):
    time_from, time_to = _grafana_time(request)
    branch = request.GET.get('branch')
    # records = models.PeopleCounter.objects.filter(date__gte=time_from, date__lte=time_to, gate__branch__name=branch)
    records = models.PeopleCounterTime.objects.filter(time__gte=time_from, time__lte=time_to, gate__branch__name=branch)
    sum_in = records.aggregate(Sum('people_in'))
    counts = {'total': sum_in['people_in__sum']}
    for gate in models.Gate.objects.filter(branch__name=branch):
        records = gate.people_count.filter(date__gte=time_from, date__lte=time_to)
        gate_sum = records.aggregate(Sum('people_in'))
        counts[gate.name] = gate_sum['people_in__sum']

    return JsonResponse(counts)


def alarms(request):
    time_from, time_to = _grafana_time(request)
    branch = request.GET.get('branch')
    logs = models.LogEntry.objects.filter(time__gte=time_from, time__lte=time_to,
                                          gate__branch__name=branch).select_related('title').order_by('-time')
    return JsonResponse(list(logs.values('time', 'gate__name', 'tag', 'title__title')), safe=False)
