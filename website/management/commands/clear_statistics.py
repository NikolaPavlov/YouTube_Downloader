from django.core.management.base import BaseCommand

from website.models import Statistics


class Command(BaseCommand):
    help = 'Clear the statistics, so the user downloads are reseted to 0'

    def handle(self, *args, **options):
        Statistics.objects.all().delete()
