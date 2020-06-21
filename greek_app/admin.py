from django.contrib import admin
from django.contrib.flatpages.models import FlatPage

from greek_app.models import *

from django.contrib.flatpages.models import FlatPage

#Note: We are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms

class FlatpageForm(FlatpageFormOld):
  content = forms.CharField(widget=CKEditorUploadingWidget())
  class Meta:
    model = FlatPage # this is not automatically inherited from FlatpageFormOld
    fields = '__all__'
    
class FlatPageAdmin(FlatPageAdminOld):
  form = FlatpageForm
  
#We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

# Register your models here.
class SymbolAdmin(admin.ModelAdmin):
    list_display = ('expansion','type','date','manuscript')
    search_fields = ['expansion',]
    list_filter = ('type', 'date','scribe','manuscript')
    autocomplete_fields = ['type']

admin.site.register(Symbol, SymbolAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)


class TypeAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Type, TypeAdmin)

