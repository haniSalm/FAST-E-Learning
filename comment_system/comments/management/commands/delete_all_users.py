from django.core.management.base import BaseCommand
from authapp.models import CustomUser  # Adjust according to the actual location of CustomUser

class Command(BaseCommand):
    help = 'Delete all users from the database'

    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all users'))
