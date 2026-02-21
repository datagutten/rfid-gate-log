import os

import requests
from django.core.management.base import BaseCommand

from gate_log import models


class Command(BaseCommand):
    help = 'Load people counter data via API'

    def handle(self, *args, **options):
        for gate in models.Gate.objects.exclude(ip=None):
            response = requests.get('%s/people?gate=%s' % (os.getenv('FEIG_API_URL', 'http://gate-api'), gate.ip))
            if not response.ok:
                continue
            counter = response.json()
            counter_obj = models.PeopleCounterTime.objects.create(gate=gate, people_in=counter['in'],
                                                                  people_out=counter['out'])
            counter_obj.save()

            pass
