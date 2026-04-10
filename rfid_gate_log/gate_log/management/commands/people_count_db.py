from django.core.management.base import BaseCommand
from django.db.models import Max

from gate_log import models
from gate_log.views import _calculate_people_count


class Command(BaseCommand):
    help = 'Calculate visitors per day'

    def handle(self, *args, **options):
        for gate_obj in models.Gate.objects.all():
            last_date = models.PeopleCounter.objects.aggregate(Max('date'))
            last_date = last_date['date__max']
            for date_obj in gate_obj.people_count_time.filter(time__date__gte=last_date).dates('time', 'day'):
                counts = gate_obj.people_count_time.filter(time__date=date_obj)
                people_in = _calculate_people_count(counts, 'people_in')
                people_out = _calculate_people_count(counts, 'people_out')

                stat, created = models.PeopleCounter.objects.get_or_create(gate=gate_obj, date=date_obj,
                                                                           defaults={'people_in': people_in,
                                                                                     'people_out': people_out})
                if not created:
                    if people_in != stat.people_in or people_out != stat.people_out:
                        stat.people_in = people_in
                        stat.people_out = people_out
                        stat.save()
                    pass
