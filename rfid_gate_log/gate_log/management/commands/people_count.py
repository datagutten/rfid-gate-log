import json
import re
import sys
from pathlib import Path
import json
import os
import datetime
from pathlib import Path

import django.db
from django.core.management.base import BaseCommand
from feig.people_count import day_stats

from gate_log import models
from lookup.lookup import LMSLookup


class Command(BaseCommand):
    help = 'Calculate visitors per day'

    def handle(self, *args, **options):
        path = Path('parsed_data')
        today = datetime.date.today()
        for gate in path.iterdir():
            if not gate.is_dir():
                continue
            gate_obj, created = models.Gate.objects.get_or_create(serial=int(gate.name))

            for date in gate.iterdir():
                if not date.is_dir() or not re.match(r'(\d{4}-\d{2}-\d{2})', date.name):
                    continue
                date_obj = datetime.date.fromisoformat(date.name)
                counter_file = date.joinpath('PeopleCounterResponse.json')
                if not counter_file.exists():
                    continue

                people_in, people_out, day_min_in, day_max_in = day_stats(counter_file)
                stat, created = models.PeopleCounter.objects.get_or_create(gate=gate_obj, date=date_obj,
                                                                           defaults={'people_in': people_in,
                                                                                     'people_out': people_out})
                # stat = models.PeopleCounter(gate=gate_obj, date=date_obj, people_in=people_in, people_out=people_out)
                if not created:
                    if people_in != stat.people_in or people_out != stat.people_out:
                        stat.people_in = people_in
                        stat.people_out = people_out
                        stat.save()
                    pass
