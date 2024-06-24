from django.core.management.base import BaseCommand
from rolepermissions.roles import assign_role

from users.models import User


class Command(BaseCommand):
    """
    CUSTOM COMMAND
    --------------
        To create operator user and assign operator role

    COMMAND LINE ARGUMENTS
    ---------------------
        user_type: str - type of user to create [operator, planner, readonly]
        username: str - username for the user
        password: str - password for the user
    """

    help = "Command to create a user and assign a role"

    def handle(self, *args, **options):
        user_role = input("Enter the user type (operator, planner, readonly): ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")

        if user_role not in ["operator", "planner", "readonly"]:
            raise ValueError(
                "Invalid user_type. Must be one of ['operator', 'planner', 'readonly']"
            )

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username, email=username, password=password, is_active=True
            )
            assign_role(user, user_role)  # Assign user role based on user_type
            msg = self.style.SUCCESS(
                f"User with username: {username} was created and assigned {user_role} role"
            )
        else:
            msg = self.style.NOTICE(f"User with username: {username} already exists")

        self.stdout.write(msg)
