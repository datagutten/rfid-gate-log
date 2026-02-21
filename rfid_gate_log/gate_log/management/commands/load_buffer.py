import json
from datetime import datetime
from pathlib import Path

import django.db
from django.core.management.base import BaseCommand

from gate_log import models


class Command(BaseCommand):
    help = 'Load gate_log data from buffer json'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='?', type=str)

    def handle(self, *args, **options):
        path = Path('../parsed_data')
        for gate in path.iterdir():
            if not gate.is_dir():
                continue
            gate_obj = models.Gate.objects.get(serial=gate.name)
            for date in gate.iterdir():
                if not date.is_dir():
                    continue
                file = date.joinpath('ReadBuffer.json')
                if not file.exists():
                    continue
                with file.open() as fp:
                    data = json.load(fp)
                    for timestamp, tags in data.items():
                        date_obj = datetime.fromtimestamp(int(timestamp))
                        for tag in tags:
                            try:
                                models.LogEntry(gate=gate_obj, time=date_obj, tag=tag).save()
                            except django.db.IntegrityError:
                                continue
                    pass

            pass
