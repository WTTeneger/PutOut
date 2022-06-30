from django.core.management.base import BaseCommand

from .file.translator import translate_po


class Command(BaseCommand):
    help = 'The translator'

    def handle(self, *args, **options):
        if options['language']:
            e = translate_po(options['language'])
            return e
        else:
            pass

    def add_arguments(self, parser):
        parser.add_argument(
        '-l',
        '--language',
        action='store',
        default=False,
        help='Язык для перевода'
        )