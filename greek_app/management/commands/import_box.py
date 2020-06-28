from django.core.management.base import BaseCommand, CommandError
from greek_app.models import Symbol 
from pathlib import Path
from boxsdk import OAuth2, Client
from GreekPal.settings_secret import BOX_CLIENT_ID, BOX_CLIENT_SECRET, BOX_DEVELOPER_TOKEN
auth = OAuth2(
    client_id=BOX_CLIENT_ID,
    client_secret=BOX_CLIENT_SECRET,
    access_token=BOX_DEVELOPER_TOKEN,
)

client = Client(auth)
user = client.user().get()

class Command(BaseCommand):
    help = 'A bulk importer. Input is the path to a zip file'

    def add_arguments(self, parser):
        parser.add_argument('fileids', nargs='+', type=str)

    def handle(self, *args, **options):
        for fileid in options['fileids']:
            box_file = client.as_user(user).file(file_id=fileid).get()
            output_file = open(box_file.name, 'wb')
            box_file.download_to(output_file)
            self.stdout.write(self.style.SUCCESS(f'imported from {fileid}'))
