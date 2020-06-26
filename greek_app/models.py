import uuid
from django.db import models
from PIL import Image
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


# Create your models here.
class Symbol(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='symbols/', blank=True, null=True, editable=True,)
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="400")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default=None)
    expansion = models.CharField(max_length=220, blank=True, null=True)
    base_expansion = models.CharField(max_length=220, blank=True, null=True)
    transcription = models.CharField(max_length=220, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, related_name='symbol_type')
    author = models.CharField(max_length=220, blank=True, null=True)
    text_title = models.CharField(max_length=220, blank=True, null=True)
    archive =  models.CharField(max_length=220, blank=True, null=True)
    city =  models.CharField(max_length=220, blank=True, null=True)
    date = models.CharField(max_length=220, blank=True, null=True)
    place = models.CharField(max_length=220, blank=True, null=True)
    scribe = models.CharField(max_length=220, blank=True, null=True)
    folia = models.CharField(max_length=220, blank=True, null=True)
    manuscript_shelfmark = models.CharField(max_length=220, blank=True, null=True)
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
        im = Image.open(self.image)
        size = 400,400
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(self.image.path, "JPEG")

        

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbols = models.ManyToManyField(Symbol, blank=True)
