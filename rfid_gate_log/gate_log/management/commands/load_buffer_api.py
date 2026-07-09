import base64
import os
from datetime import datetime
from json import JSONDecodeError

import requests
from django.core.management.base import BaseCommand

from gate_log import models


class Command(BaseCommand):
    help = 'Load gate_log data from buffer via API'

    # def add_arguments(self, parser):
    #     parser.add_argument('gate', nargs='?', type=str)

    def handle(self, *args, **options):
        for gate in models.Gate.objects.exclude(ip=None):
            print('Saving tags from %s:' % gate)
            response = requests.get('%s/buffer?gate=%s' % (os.getenv('FEIG_API_URL', 'http://gate-api'), gate.ip))
            if not response.ok:
                try:
                    if 'error' in response.json():
                        print(response.json()['error'])
                        continue
                except JSONDecodeError:
                    pass
                print(response.content)
                continue
            data = response.json()
            print('Data: ', data)
            if 'tags' not in data:
                print('No tags in buffer for gate %s' % gate)
                continue
            raw_data = base64.b64decode(data['raw'])
            raw_obj = models.BufferRaw.objects.create(gate=gate, time=datetime.now(), data=raw_data)
            for tag in data['tags']:
                if not tag:
                    continue
                print(tag)
                models.LogEntry.objects.create(gate=gate, time=datetime.now(), tag=tag)
                raw_obj.tags.add(tag)
            response = requests.get(
                '%s/buffer_clear?gate=%s' % (os.getenv('FEIG_API_URL', 'http://http-proxy'), gate.ip))
            print('Clear: ', response.json())
