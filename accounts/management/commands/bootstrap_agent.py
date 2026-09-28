import os

from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = "Create the delivery agent (admin) account from AGENT_USERNAME and AGENT_PASSWORD."

    def handle(self, *args, **options):
        username = os.environ.get('AGENT_USERNAME')
        password = os.environ.get('AGENT_PASSWORD')
        if not username or not password:
            self.stdout.write('AGENT_USERNAME / AGENT_PASSWORD not set, skipping.')
            return

        user, created = User.objects.get_or_create(username=username)
        user.is_delivery_agent = True
        user.is_staff = True
        user.is_superuser = True
        if created:                      # never overwrite an existing password
            user.set_password(password)
        user.save()
        self.stdout.write(f"Agent account '{username}' {'created' if created else 'already exists, updated'}.")