from django.core.management.base import BaseCommand

from gate_log import models
from lookup.lookup import LMSLookup


class Command(BaseCommand):
    help = 'Lookup titles from LMS'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='?', type=str)

    def handle(self, *args, **options):
        lms = {}
        for entry in models.LogEntry.objects.filter(title__isnull=True):
            branch_id = entry.gate.branch_id
            branch = entry.gate.branch
            if entry.gate.branch_id not in lms:
                lms[branch_id] = LMSLookup(branch.lms_url)
                lms[branch_id].sip_connect(branch.lms_user, branch.lms_password)

            try:
                title_obj = models.Title.objects.get(tag=entry.tag)
            except models.Title.DoesNotExist:
                response_tag = lms[branch_id].query(entry.tag)
                if response_tag == 'Unknown':
                    print('Unknown tag %s' % entry.tag)
                    continue
                title_obj = models.Title(tag=entry.tag, title=response_tag)
                title_obj.save()
            entry.title = title_obj
            entry.save()
