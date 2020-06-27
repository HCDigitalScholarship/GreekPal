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

    list_display = ('base_expansion','symbol_type','date','manuscript_shelfmark')
    search_fields = ['base_expansion',]
    exclude = ['sketch',]
    list_filter = ('symbol_type', 'date','scribe','manuscript_shelfmark')
    autocomplete_fields = ['symbol_type']

admin.site.register(Symbol, SymbolAdmin)



class TypeAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Type, TypeAdmin)

class CollectionAdmin(admin.ModelAdmin):
  pass

admin.site.register(Collection, CollectionAdmin)
