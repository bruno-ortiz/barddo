from django.core.management import call_command

from django.core.management.base import BaseCommand
from django.utils.termcolors import make_style


class Command(BaseCommand):
    """
    Provides a simple command for reseting the database
    """

    def handle(self, *args, **options):
        self.stdout.write('\nReseting Database!', make_style(opts=('bold',), fg='red'))
        call_command('reset_db', interactive=False)
        self.stdout.write('\nExecuting syncdb!', make_style(opts=('bold',), fg='green'))
        call_command('syncdb')
        self.stdout.write('\nMigrating database!', make_style(opts=('bold',), fg='green'))
        call_command('migrate', all_apps=True)