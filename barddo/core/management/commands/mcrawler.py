from optparse import make_option

from django.core.management.base import BaseCommand

from crawler.importer import threaded_crawler


class Command(BaseCommand):
    """
    Provides a simple command for crawling the website http://centraldemangas.net
    """

    option_list = BaseCommand.option_list + (
        make_option('--threads',
                    '-t',
                    dest='_threads',
                    default=None,
                    help='Total threads to fetch data'),
    )

    def handle(self, *args, **options):
        threads_count = options['_threads']
        threaded_crawler(int(threads_count))
