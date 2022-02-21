import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """The Django command to pause execution unit database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for the database')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('The Database is not available, waiting 1 second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Successfully connected to the database'))
