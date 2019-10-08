from django.contrib import admin
from greek_app.models import *

# Register your models here.
class SymbolAdmin(admin.ModelAdmin):
    list_display = ('expansion','type','date','manuscript')
    search_fields = ['expansion',]
    list_filter = ('type', 'date','scribe','manuscript')

admin.site.register(Symbol, SymbolAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)


class TypeAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


admin.site.register(Type, TypeAdmin)

