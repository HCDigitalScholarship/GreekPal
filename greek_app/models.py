import uuid
from django.db import models
import PIL.Image
from greek_accentuation.characters import base
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from greek_app.preprocess_image import get_preprocessed_image, resize_image
from django.core.files.base import ContentFile
from pathlib import Path


class Type(models.Model):
    name = models.CharField(max_length=220, blank=True, null=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    file = models.ImageField(upload_to='symbols/')

    def __str__(self):
        return self.file.name

# Create your models here.
class Symbol(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='symbols/original', blank=True, null=True, editable=True,)
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default=None)
    cleaned = models.ImageField(upload_to='symbols/cleaned', blank=True, null=True, editable=True,)
    expansion = models.CharField(max_length=220, blank=True, null=True)
    base_expansion = models.CharField(max_length=220, blank=True, null=True)
    transcription = models.CharField(max_length=220, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, related_name='symbol_type')
    text = models.CharField(max_length=220, blank=True, null=True)
    date = models.CharField(max_length=220, blank=True, null=True)
    place = models.CharField(max_length=220, blank=True, null=True)
    scribe = models.CharField(max_length=220, blank=True, null=True)
    manuscript = models.CharField(max_length=220, blank=True, null=True)
    notes = RichTextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    sketch = JSONField(blank=True, null=True)

    def __str__(self):
        return self.expansion

    def save(self):
        self.base_expansion = ''.join([base(i) for i in self.expansion])
        if not self.image:
            return

        super(Symbol, self).save()
        resize_image(self.image.path) #resizes to 400,400 and saves to static/symbols/original
        get_preprocessed_image(self.image.path) #creates the cleaned file and saves to static/symbols/cleaned
        self.cleaned.save(self.image.path.split('/')[-1], ContentFile(Path(self.image.path.replace('original','cleaned')).read_bytes()), save=False)

        

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbols = models.ManyToManyField(Symbol, blank=True)
