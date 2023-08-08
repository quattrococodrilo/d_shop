import pathlib

from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

class Command(BaseCommand):
    help = "Creates a new secret key for Django project."

    def handle(self, *args, **options):
        secret = (get_random_secret_key() + get_random_secret_key())[:66]
        self.stdout.write(self.style.SUCCESS(f"Secret key: {secret}"))
