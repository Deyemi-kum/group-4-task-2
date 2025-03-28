from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a default user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='Deyemi-kum').exists():
            User.objects.create_superuser('Deyemi-kum', 'deyemi@example.com', 'password123')
            self.stdout.write(self.style.SUCCESS('Default user created: Deyemi-kum'))
        else:
            self.stdout.write(self.style.WARNING('Default user already exists'))
