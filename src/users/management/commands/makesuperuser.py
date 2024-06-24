from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    CUSTOM COMMAND
    --------------
        To create superuser using environment variables

    ENV VARIABLES
    -------------
        SUPERUSER_USERNAME: str - email or username
        SUPERUSER_PASSWORD: str - password for account
    """

    help = "Command to create a superuser"

    def handle(self, *args, **options):
        username = str(settings.SUPERUSER_USERNAME)
        password = str(settings.SUPERUSER_PASSWORD)
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=username, password=password, is_active=True
            )
            msg = self.style.SUCCESS(f"Admin with username: {username} was created")
        else:
            msg = self.style.NOTICE(f"Admin with username: {username} already exists")
        self.stdout.write(msg)
