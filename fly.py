#!/usr/bin/env python3

import argparse
from ast import Tuple
import pathlib
import platform
import shlex
import shutil
import subprocess
from os import getenv
from typing import Any, Dict, List

import requests
from colorama import Fore, Style
from dotenv import load_dotenv

from core.testing import dd


class EnvData:
    """Load environment variables data."""

    APPS_DIR: str = "./apps"

    APP_URL: str = "https://github.com/quattrococodrilo/Django-Vite-Tailwind-Docker/archive/refs/heads/main.zip"

    DOCKER_PROD: str = "docker-compose.yml"
    DOCKER_DEV: str = "docker-compose.yml"

    DOCKER_COMPOSE: str = "docker compose"

    def __init__(self) -> None:
        load_dotenv()

        self.APPS_DIR: str = getenv("APPS_DIR", "./apps")
        self.APP_PORT: str = getenv("APP_PORT", "80")
        self.SSL_APP_PORT: str = getenv("SSL_APP_PORT", "443")
        self.DB_APP_SERVICE: str = getenv("DB_HOST", "db")
        self.DB_HOST: str = getenv("DB_HOST", "db")
        self.DB_NAME: str = getenv("DB_NAME", "postgres")
        self.DB_PASSWORD: str = getenv("DB_PASSWORD", "postgres")
        self.DB_PORT: str = getenv("DB_PORT", "3306")
        self.VITE_PORT: str = getenv("DB_PORT", "5432")
        self.DB_USERNAME: str = getenv("DB_USERNAME", "postgres")
        self.DJANGO_APP_PORT: str = getenv("DJANGO_APP_PORT", "80")
        self.DJANGO_APP_SERVICE: str = getenv("APP_SERVICE", "web")
        self.FLY_DJANGO_IMAGE: str = getenv("FLY_DJANGO_IMAGE", "fly-dj4")
        self.FLY_FILES: str | None = getenv("FLY_FILES")
        self.FLY_NETWORK: str = getenv("FLY_NETWORK", "fly_network")
        self.NODE_APP_SERVICE: str = getenv("APP_SERVICE", "node")
        self.WWWGROUP: str = getenv("GROUPID", "1000")
        self.WWWUSER: str = getenv("USERID", "1000")


class Printer:
    """Handle print."""

    def printer(self, text: str, color: str = "white", style: str = "normal") -> None:
        """Print text with color and style"""
        print(getattr(Fore, color.upper()) + getattr(Style, style.upper()) + text)

    def line(self, text: str) -> None:
        self.printer(text)

    def error(self, text: str) -> None:
        self.printer(text, color="red", style="bright")

    def warning(self, text: str) -> None:
        self.printer(text, color="yellow", style="bright")

    def success(self, text: str) -> None:
        self.printer(text, color="green", style="bright")

    def info(self, text: str) -> None:
        self.printer(text, color="blue", style="bright")


class Argument:
    """Argument class."""

    def __init__(
        self,
        flags: List[str],
        action: Any | None = None,
        nargs: Any | None = None,
        const: Any = None,
        default: Any = None,
        type: Any = None,
        choices: Any = None,
        required: bool = False,
        help: str | None = None,
        metavar: str | None = None,
        dest: str | None = None,
    ) -> None:
        self.flags = flags
        self.action = action
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar
        self.dest = dest

    def make(self) -> tuple[List[str], Dict[str, Any]]:
        options: Dict[str, Any] = {}

        for attr, value in vars(self).items():
            if attr != "flags" and value:
                options[attr] = value

        return (self.flags, options)


class BaseCommand:
    """Base command class."""

    ENV: EnvData = EnvData()

    subparser_dest: str
    command_name: str
    command_help: str
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    command_args: List[Argument] = [
        Argument(
            flags=["args"],
            nargs=argparse.REMAINDER,
        ),
    ]

    printer: Printer = Printer()

    def command(self, args):
        """Define your command here."""
        pass

    def set_main_parser(self, subparsers):
        """Set main parser."""
        self.subparsers = subparsers
        return self

    def add_parser(self, subparsers):
        """Add parser to subparsers."""
        parser = subparsers.add_parser(self.command_name, help=self.command_help)
        for arg in self.command_args:
            [flag, options] = arg.make()
            parser.add_argument(*flag, **options)
        parser.set_defaults(func=self.command)

    def run_command(
        self,
        command: str,
        extra_args: List[str] = [],
        stdout_null: bool = False,
        stderr_null: bool = False,
        stdout: bool = False,
        stderr: bool = False,
    ) -> subprocess.CompletedProcess:
        """Runs command."""

        _command: List[str] = shlex.split(command)

        kwargs: Dict[str, Any] = {}

        if len(extra_args):
            _command = _command + extra_args

        if stdout_null and not stdout:
            kwargs["stdout"] = subprocess.DEVNULL
        elif not stdout_null and stdout:
            kwargs["stdout"] = subprocess.PIPE

        if stderr_null and not stderr:
            kwargs["stderr"] = subprocess.DEVNULL
        elif not stderr_null and stderr:
            kwargs["stderr"] = subprocess.PIPE

        return subprocess.run(_command, **kwargs)

    def check_docker(
        self,
        validate_file=True,
        validate_docker=True,
        validate_docker_compose=True,
        validate_fly=True,
    ):
        """Check if all related with docker is ok to run some commands."""

        if not self.docker_compose_file_exists() and validate_file:
            self.printer.error("Missing docker compose file.")
            exit(1)

        if not self.docker_is_installed() and validate_docker:
            self.printer.error("Missing docker.")
            exit(1)

        if not self.docker_compose_is_installed() and validate_docker_compose:
            self.printer.error("Missing docker compose.")
            exit(1)

        if not self.fly_is_running() and validate_fly:
            self.printer.warning("Fly is not running.")
            exit(1)

    def docker_compose_file_exists(self):
        """Check if docker compose file exists."""

        if pathlib.Path(self.ENV.DOCKER_PROD).exists():
            return True
        if pathlib.Path(self.ENV.DOCKER_DEV).exists():
            return True
        return False

    def docker_is_installed(self):
        """Check if docker is installed."""

        try:
            completed_process = self.run_command(
                "docker info",
                stdout_null=True,
                stderr=True,
            )
        except FileNotFoundError:
            return False

        if completed_process.returncode == 0:
            return True
        return False

    def docker_compose_is_installed(self):
        """Check if docker compose is installed."""

        try:
            completed_process = self.run_command(
                "docker compose",
                stdout_null=True,
                stderr=True,
            )
            self.ENV.DOCKER_COMPOSE = "docker compose"
        except FileNotFoundError:
            try:
                completed_process = self.run_command(
                    "docker-compose",
                    stdout_null=True,
                    stderr=True,
                )
                self.ENV.DOCKER_COMPOSE = "docker-compose"
            except FileNotFoundError:
                return False

        if completed_process.returncode == 0:
            return True
        return False

    def fly_is_running(self):
        """Check if Fly is running."""

        completed_process = self.run_command(
            f"docker compose ps {self.ENV.DJANGO_APP_SERVICE}",
            stdout_null=True,
            stderr=True,
        )

        if completed_process.returncode == 0:
            return True
        return False


class Fly:
    """
    Fly commands.
    """

    ENV: EnvData = EnvData()

    commands: List[Dict[str, Any]] = []

    printer: Printer = Printer()

    def __init__(self):
        self._system = self.uname_s()

        if self._system != "Linux" and self._system != "Darwin":
            self.printer.error("System not supported")
            raise ValueError("System not supported")

        self.parser = argparse.ArgumentParser(
            description="Fly is a command line tool for managing your Django projects."
        )
        self.subparsers = self.parser.add_subparsers()
        self.start_parser()

    @classmethod
    def run(cls):
        """Run Fly."""

        return cls()

    def command_register(self):
        """Commands register."""

        return [
            InstallFlyCommand().set_main_parser(self.subparsers),
            BuildServicesCommand().set_main_parser(self.subparsers),
            UpServicesCommand().set_main_parser(self.subparsers),
            DownServicesCommand().set_main_parser(self.subparsers),
            DockerComposeCommand().set_main_parser(self.subparsers),
            PipCommand().set_main_parser(self.subparsers),
            DjangoManageCommand().set_main_parser(self.subparsers),
            NpmCommand().set_main_parser(self.subparsers),
            MySqlCommand().set_main_parser(self.subparsers),
            PostgreSqlCommand().set_main_parser(self.subparsers),
            DjangoServerRunAloneCommand().set_main_parser(self.subparsers),
        ]

    def start_parser(self):
        """Start the parser."""

        self.register()
        args = self.parser.parse_args()
        if "func" in args:
            args.func(args)
        else:
            self.parser.print_help()

    def register(self):
        """Register parser in subparsers."""

        for command in self.command_register():
            command.add_parser(self.subparsers)

    def uname_s(self):
        """Check OS type."""

        info = platform.uname()
        return info.system


class InstallFlyCommand(BaseCommand):
    """Installs app."""

    subparser_dest: str = "Install"
    command_name: str = "install"
    command_help: str = "Install app."

    def command(self, args):
        python_packages = shlex.split("pip install colorama requests python-dotenv")
        subprocess.run(python_packages)

        self.printer.success("Basic install, done...")
        self.printer.info("Installing app..")

        zip_file = pathlib.Path("django_fly.zip")
        project_dir = pathlib.Path("Django-Vite-Tailwind-Docker-main")

        response = requests.get(self.ENV.APP_URL)
        zip_file.write_bytes(response.content)

        # result = subprocess.run(shlex.split(f"unzip {zip_file} -d ."))
        result = self.run_command(f"unzip {zip_file} -d .")
        if result.returncode != 0:
            print(f"Error al descomprimir {zip_file}")
            return

        if zip_file.exists():
            zip_file.unlink()

        if project_dir.exists():
            for file in project_dir.iterdir():
                shutil.move(file, ".")

            shutil.rmtree(project_dir)

class BuildServicesCommand(BaseCommand):
    """Build services."""

    subparser_dest: str = "Build"
    command_name: str = "build"
    command_help: str = "Build services."

    def command(self, args):
        self.check_docker(validate_fly=False)
        try:
            self.printer.info("Shuting down old services...")
            self.run_command(
                "docker rm -f $(docker ps -aq)",
                stdout_null=True,
                stderr_null=True,
            )
            self.run_command(
                f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} build",
                extra_args=args.args,
            )
        except KeyboardInterrupt:
            self.printer.info("Services removed.")


class UpServicesCommand(BaseCommand):
    """Up services."""

    subparser_dest: str = "Up"
    command_name: str = "up"
    command_help: str = "Up services."

    def command(self, args):
        self.check_docker(validate_fly=False)
        try:
            self.printer.info("Shuting down old services...")
            self.run_command(
                "docker rm -f $(docker ps -aq)",
                stdout_null=True,
                stderr_null=True,
            )
            self.run_command(
                f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} up",
                extra_args=args.args,
            )
        except KeyboardInterrupt:
            self.printer.info("Services removed.")


class DownServicesCommand(BaseCommand):
    """Down services."""

    subparser_dest: str = "Down"
    command_name: str = "down"
    command_help: str = "Down services."

    def command(self, args):
        self.check_docker()
        try:
            self.run_command(
                f"docker compose -f {self.ENV.DOCKER_DEV} down",
                extra_args=args.args,
            )
            self.run_command(
                "docker rm -f $(docker ps -aq)",
                stdout_null=True,
                stderr_null=True,
            )
        except KeyboardInterrupt:
            self.printer.info("Services removed.")


class DockerComposeCommand(BaseCommand):
    """Execute docker compose commands."""

    subparser_dest: str = "docker_compose"
    command_name: str = "d"
    command_help: str = "Execute docker compose commands."

    def command(self, args):
        self.check_docker()
        self.run_command(
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV}", extra_args=args.args
        )


class PipCommand(BaseCommand):
    """Execute pip commands."""

    subparser_dest: str = "pip"
    command_name: str = "pip"
    command_help: str = "Execute pip commands"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly"
            f" {self.ENV.DJANGO_APP_SERVICE} venv/bin/pip"
        )
        self.run_command(cmd, extra_args=args.args)


class DjangoManageCommand(BaseCommand):
    """Execute manage.py commands."""

    subparser_dest: str = "manage"
    command_name: str = "manage"
    command_help: str = "Execute Django Manager"

    def command(self, args):
        self.check_docker()

        if "startapp" in args.args:
            app_name = args.args[-1]
            apps_path = pathlib.Path(self.ENV.APPS_DIR)
            if (apps_path / app_name).exists():
                self.printer.error(f"App {app_name} already exists.")
                exit(1)

        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly "
            f" {self.ENV.DJANGO_APP_SERVICE} venv/bin/python manage.py"
        )
        self.run_command(cmd, extra_args=args.args)

        new_app_name: str = args.args[-1]
        new_app = pathlib.Path(args.args[-1])

        if "startapp" in args.args and new_app.exists():
            apps_file = new_app / "apps.py"
            apps_file_content = apps_file.read_text()
            apps_dir = pathlib.Path(self.ENV.APPS_DIR)
            apps_file_content = apps_file_content.replace(
                "name = '", f"name = '{apps_dir.name}."
            )
            apps_file.write_text(apps_file_content)
            shutil.move(new_app_name, apps_dir / new_app_name)
            self.printer.success(f"App {new_app} created.")

            config_app_name: str = (
                new_app_name.replace("_", " ").title().replace(" ", "")
            )
            self.printer.success(
                f'"{apps_dir.name}.{new_app_name}.apps.{config_app_name}Config"'
            )


class DjangoServerRunAloneCommand(BaseCommand):
    """Run Django server alone."""

    subparser_dest: str = "django_server"
    command_name: str = "runserve-alone"
    command_help: str = "Run Django server alone"
    command_args: List[Argument] = [
        Argument(
            flags=["args"],
            nargs=argparse.REMAINDER,
        ),
        Argument(
            flags=["--https"],
            action="store_true",
            help="Run in HTTPS mode. Requires: pyOpenSSL, werkzeug",
        ),
    ]

    def command(self, args):
        self.check_docker()

        web_service = subprocess.Popen(
            shlex.split(f"{self.ENV.DOCKER_COMPOSE} ps {self.ENV.DJANGO_APP_SERVICE}"),
            stdout=subprocess.PIPE,
        )

        grep_data = subprocess.Popen(
            shlex.split(f"grep {self.ENV.DJANGO_APP_SERVICE}"),
            stdin=web_service.stdout,
            stdout=subprocess.PIPE,
        )

        web_service.stdout.close()

        output, errors = grep_data.communicate()

        output = output.decode("UTF-8").replace("  ", "").split(" ")

        network = pathlib.Path().cwd().name.lower() + "_" + self.ENV.FLY_NETWORK

        self.run_command(
            f"docker compose stop {self.ENV.DJANGO_APP_SERVICE}",
        )

        if args.https:
            self.run_command(
                f"docker run -it --entrypoint /bin/bash --env-file ./.env -v .:/code"
                f" -p {self.ENV.SSL_APP_PORT}:8443 --network={network} {self.ENV.FLY_DJANGO_IMAGE}"
                # ' -c "venv/bin/python manage.py runserver_plus 0.0.0.0:8000"'
                ' -c "venv/bin/python manage.py runserver_plus 0.0.0.0:8443 --cert-file /tmp/cert.crt --key-file /tmp/cert.key"',
            )
        else:
            self.run_command(
                f"docker run -it --entrypoint /bin/bash --env-file ./.env -v .:/code"
                f" -p {self.ENV.APP_PORT}:8000 --network={network} {self.ENV.FLY_DJANGO_IMAGE}"
                ' -c "venv/bin/python manage.py runserver 0.0.0.0:8000"'
            )


class NpmCommand(BaseCommand):
    """Execute NPM commands."""

    subparser_dest: str = "npm"
    command_name: str = "npm"
    command_help: str = "Execute npm"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly"
            f" {self.ENV.NODE_APP_SERVICE} npm"
        )
        self.run_command(cmd, extra_args=args.args)


class NpxCommand(BaseCommand):
    """Execute NPX commands."""

    subparser_dest: str = "npx"
    command_name: str = "npx"
    command_help: str = "Execute npx"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec -u fly"
            f" {self.ENV.NODE_APP_SERVICE} npx"
        )
        self.run_command(cmd, extra_args=args.args)


class MySqlCommand(BaseCommand):
    """Execute MySql commands."""

    subparser_dest: str = "mysql"
    command_name: str = "mysql"
    command_help: str = "Execute MySql"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV} exec db bash -c"
            f' "MYSQL_PWD={self.ENV.DB_PASSWORD}'
            f' mysql -u {self.ENV.DB_USERNAME} {self.ENV.DB_NAME}"'
        )
        self.run_command(cmd, extra_args=args.args)


class PostgreSqlCommand(BaseCommand):
    """Execute PostgreSQL commands."""

    subparser_dest: str = "psql"
    command_name: str = "psql"
    command_help: str = "Execute PostgreSQL"

    def command(self, args):
        self.check_docker()
        cmd = (
            f"{self.ENV.DOCKER_COMPOSE} -f {self.ENV.DOCKER_DEV}"
            f" exec {self.ENV.DB_APP_SERVICE} bash -c"
            f' "PGPASSWORD={self.ENV.DB_PASSWORD}'
            f' psql -U {self.ENV.DB_USERNAME} {self.ENV.DB_NAME}"'
        )
        self.run_command(cmd, extra_args=args.args)


if __name__ == "__main__":
    Fly.run()
