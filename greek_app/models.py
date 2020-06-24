import uuid
from django.db import models
import PIL.Image
from greek_accentuation.characters import base
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


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
    image = models.ImageField(upload_to='symbols/', blank=True, null=True, editable=True,)
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default=None)
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
    #sketch = models.CharField(max_length=220, blank=True, null=True)
    def __str__(self):
        return self.expansion

    def save(self):
        self.base_expansion = ''.join([base(i) for i in self.expansion])
        if not self.image:
            return

        super(Symbol, self).save()
        image = PIL.Image.open(self.image)
        (width, height) = image.size
        size = (150, 150)
        image.thumbnail(size)
        #image = image.resize(size)
        image.save(self.image.path)

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbols = models.ManyToManyField(Symbol, blank=True)
