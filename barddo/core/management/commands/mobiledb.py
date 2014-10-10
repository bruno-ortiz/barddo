from django.core.management.base import BaseCommand

from crawler.mobile_import import import_to_mobile


class Command(BaseCommand):
    """
    Provides a simple command for crawling the website http://centraldemangas.net
    """
    def handle(self, *args, **options):
        import_to_mobile()
