from django.core.management.base import BaseCommand, CommandError
from greek_app.models import Symbol,Type
from pathlib import Path
from zipfile import ZipFile
from django.conf import settings
import shutil
from django.core.files import File
import os 


class Command(BaseCommand):
    help = 'A bulk importer. Input is a directory of png files'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+', type=str)

    def handle(self, *args, **options):
        for filepath in options['filepath']:
            document = filepath.split('/')
            #if there is a trailing slash in the filepath, then the -1 item is '', so use one before
            if len(document[-1]) == 0:
                document = document[-2]
            else:
                document = document[-1]

            #<city>-<archive>-<manuscript or shelfmark>-<text title>-<date>-<place>-<folia>-<author>-<scribe>
            #Rome-Biblioteca Vallicelliana-ms.F 86-Ὁ Καρπός-13th cent.-blank-blank-56r–63r-ps-Ptolemy-blank
            keys = ["city","archive", "manuscript_shelfmark", "text_title", "date","place","folia","author","scribe",]
            data_doc = dict(zip(keys, document.split("-")[:]))
            
            for file in Path(filepath).iterdir():
                #<base>-<transcription>-<type>-<number>-<“o” or “h” or “d”>.png
                keys = ["base_expansion","transcription","symbol_type","number","display"]
                name = file.stem.split('-')
                if len(name) == 5:
                    data_png = dict(zip(keys, name))
                    if data_png['display'] == 'd':
                        del data_png['display']
                        del data_png['number']
                        data_png['symbol_type'] = data_png['symbol_type'].title()
                        kwargs = {**data_doc, **data_png}
                        #symbol_type, created = Type.objects.get_or_create(name=kwargs["symbol_type"])

                        obj, created = Symbol.objects.update_or_create(
                            #image = File(file.read_bytes()),
                            city=kwargs['city'],
                            archive=kwargs["archive"], 
                            manuscript_shelfmark=kwargs["manuscript_shelfmark"],
                            text_title=kwargs["text_title"], 
                            date=kwargs["date"],
                            place=kwargs["place"],
                            folia=kwargs["folia"],
                            author=kwargs["author"],
                            scribe=kwargs["scribe"],
                            base_expansion=kwargs["base_expansion"],
                            transcription=kwargs["transcription"],
                            #symbol_type=symbol_type,
                        )
                        #copy file to STATIC 
                        destination = os.path.join(settings.MEDIA_ROOT, str(file.name))
                        
                        shutil.copyfile(str(file), destination) 
                        obj.image.name= '/symbols/' + str(file.name)
                        obj.save()
                
                self.stdout.write(self.style.SUCCESS(f'added {file.stem}'))
