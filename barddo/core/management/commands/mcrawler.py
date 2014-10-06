from optparse import make_option

from django.core.management.base import BaseCommand

from crawler.fetch import INITIAL_URL, execute


class Command(BaseCommand):
    """
    Provides a simple command for crawling the website http://centraldemangas.net
    """

    option_list = BaseCommand.option_list + (
        make_option('--file',
                    '-f',
                    dest='_file',
                    default=None,
                    help='File containing the data of the site'),
    )

    def handle(self, *args, **options):
        file_ = options['_file']
        if file_:
            msg = "Voce gostaria de importa os dados do arquivo {} '(s/n)'?".format(file_)
        else:
            msg = "Voce tem certeza que gostaria de executar o crawler na url {} '(s/n)'?".format(INITIAL_URL)
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('s', 'n'):
                confirm = raw_input('Entre s ou n!: ')
            elif confirm == 's':
                data = execute(file_)
