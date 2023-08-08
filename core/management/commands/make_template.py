import pathlib

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Make a template"

    def add_arguments(self, parser):
        parser.add_argument(
            "template_path",
            help=(
                "App where the template will be created:"
                " app_name/{sub_dir}/template_name.html."
            ),
        )

    def handle(self, *args, **options):
        base_dir: pathlib.Path = settings.BASE_DIR

        template_full_path = options["template_path"]
        app_name, template_path = template_full_path.split("/", 1)

        template: pathlib.Path = (
            base_dir
            / settings.APPS_DIR
            / app_name
            / "templates"
            / app_name
            / template_path
        )

        if not template.parent.exists():
            template.parent.mkdir(parents=True, exist_ok=True)

        if template.parent.exists() and not template.exists(): 
            template.write_text('{% extends "base.html" %}')
            self.stdout.write(self.style.SUCCESS(template))
            self.stdout.write(self.style.SUCCESS("Done!"))
        else:
            self.stdout.write(self.style.ERROR("Template already exists!"))

