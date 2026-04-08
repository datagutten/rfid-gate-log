import datetime
import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from gate_log import models


class Command(BaseCommand):
    help = 'Load visitor count from json'

    def handle(self, *args, **options):
        path = Path('parsed_data')
        for gate in path.iterdir():
            if not gate.is_dir():
                continue
            gate_obj, created = models.Gate.objects.get_or_create(serial=int(gate.name))

            for date in gate.iterdir():
                if not date.is_dir() or not re.match(r'(\d{4}-\d{2}-\d{2})', date.name):
                    continue
                counter_file = date.joinpath('PeopleCounterResponse.json')
                if not counter_file.exists():
                    continue
                with counter_file.open() as fp:
                    entries = json.load(fp)
                for timestamp, counts in entries.items():
                    time_obj = datetime.datetime.fromtimestamp(int(timestamp))
                    stat, created = models.PeopleCounterTime.objects.get_or_create(
                        gate=gate_obj,
                        time=time_obj,
                        defaults={'people_in': counts['in'],
                                  'people_out': counts['out']})
                    pass
