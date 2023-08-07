import pathlib

from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates new factory"

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name",
            type=str,
            help="App name where the factory will be created"
        )

    def handle(self, *args, **options):
       
        base_dir = pathlib.Path(settings.BASE_DIR) 
        
        app_name = options["app_name"]

        app_dir = (base_dir / f"apps/{app_name}" 
                if app_name != "core" 
                else base_dir / "code")

        seeder_dir = app_dir / "seeder"

        if seeder_dir.exists():
            raise CommandError("Seeder already exists.")

        if not app_dir.exists():
            raise CommandError("App not found.")
        else:
            seeder_dir.mkdir(parents=True, exist_ok=True)
        
        (seeder_dir / "__init__.py").write_text('')        

        (seeder_dir / "seeders.py").write_text("""
def your_seeder():
    pass
        """.replace("\n", "", 1))        
        
        (seeder_dir / "factories.py").write_text("""
import factory
from factory.django import DjangoModelFactory
import faker

class YourModelFactory(DjangoModelFactory):
    class Meta:
        model = "your.Model"

    some_field = factory.Faker("some_fake")
        """.replace("\n", "", 1))

        self.stdout.write(self.style.SUCCESS("Seeder created successfully."))
