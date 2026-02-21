from django.contrib import admin

from gate_log import models


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['tag', 'title']


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = ['branch', 'name', 'ip', 'serial']
    list_filter = ['branch']


@admin.register(models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['gate', 'time', 'tag', 'title']
    list_filter = ['gate', 'time']
