from django.core.management.base import BaseCommand

from mailings.utils import send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mailing()
