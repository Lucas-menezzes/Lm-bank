from django.core.management.base import BaseCommand
import subprocess
import sys

class Command(BaseCommand):
    help = 'Run tests and start the Django server if tests pass.'

    def handle(self, *args, **kwargs):
        result = subprocess.run([sys.executable, '-m', 'pytest'])

        if result.returncode == 0:
            self.stdout.write(self.style.SUCCESS('All tests passed. Starting the Django server...'))
            subprocess.run([sys.executable, 'manage.py', 'runserver'])
        else:
            self.stdout.write(self.style.ERROR('Some tests failed. Please fix the issues before starting the server.'))
            sys.exit(1)