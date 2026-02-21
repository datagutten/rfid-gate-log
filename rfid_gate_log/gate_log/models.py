from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100, help_text='Library branch name')
    lms_url = models.URLField(help_text='Library branch LMS url', null=True, blank=True)
    lms_user = models.CharField(max_length=100, help_text='Library branch LMS user name', null=True, blank=True)
    lms_password = models.CharField(max_length=100, help_text='Library branch LMS password', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'branches'


class Gate(models.Model):
    serial = models.IntegerField('Serial number', primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='gates')
    name = models.CharField('Name', max_length=100, null=True, blank=True)
    ip = models.GenericIPAddressField('IP address', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.branch.name, self.name or self.serial)


class Title(models.Model):
    tag = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class LogEntry(models.Model):
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, related_name='logs')
    time = models.DateTimeField()
    tag = models.CharField('Tag', max_length=100)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True, related_name='logs')

    class Meta:
        unique_together = ('gate', 'time', 'tag')
        verbose_name_plural = 'log entries'

    def __str__(self):
        return '%s %s %s' % (self.gate, self.time, self.title or self.tag)


class PeopleCounter(models.Model):
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, related_name='people_count')
    date = models.DateField()
    people_in = models.IntegerField()
    people_out = models.IntegerField()

    class Meta:
        unique_together = ('gate', 'date')


class PeopleCounterTime(models.Model):
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, related_name='people_count_time')
    time = models.DateTimeField(auto_now_add=True)
    people_in = models.IntegerField()
    people_out = models.IntegerField()

    class Meta:
        unique_together = ('gate', 'time')
