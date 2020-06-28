from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse

from greek_app.models import Symbol, Type
from greek_app.similarity import similarity
from django.utils.html import escape, format_html, mark_safe
import json

def home(request):
    context = {}
    if request.POST:

        data = request.POST.get('data',None)
        
        if data:
            data = json.loads(data)
            symbols = Symbol.objects.all()
            for symbol in symbols:
                if symbol.sketch:
                    symbol.similarity = similarity(data, symbol.sketch)['dh']
                    symbol.save()                
                        
        context['symbols'] = Symbol.objects.all()
        return render(request, 'index.html', context)
    else:
        symbols = Symbol.objects.all()
        
        context['symbols'] = symbols
        return render(request, 'index.html', context)

@staff_member_required
def edit(request):
    if request.POST:
        data = request.POST.get('data',None)
        data = json.loads(data)
        data_id = data['id']
        symbol = Symbol.objects.get(id=data_id)
        symbol.sketch = data
        symbol.save()
    context = {}
    symbols = [s.__dict__ for s in Symbol.objects.all()]
    context['symbols'] = symbols
    return render(request, 'edit.html', context)

def logout_view(request):
    logout(request)
    return redirect(home)

def symbol_json(request, symbol_id):
    symbol = Symbol.objects.get(id=symbol_id)
    return JsonResponse(symbol.sketch)



#server side
class SymbolJson(BaseDatatableView):
    # the model you're going to show
    model = Symbol

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # image = models.ImageField(upload_to='symbols/', blank=True, null=True, editable=True,)
    # image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="400")
    # image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default=None)
    # expansion = models.CharField(max_length=220, blank=True, null=True)
    # base_expansion = models.CharField(max_length=220, blank=True, null=True)
    # transcription = models.CharField(max_length=220, blank=True, null=True)
    # symbol_type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, related_name='symbol_type')
    # author = models.CharField(max_length=220, blank=True, null=True)
    # text_title = models.CharField(max_length=220, blank=True, null=True)
    # archive =  models.CharField(max_length=220, blank=True, null=True)
    # city =  models.CharField(max_length=220, blank=True, null=True)
    # date = models.CharField(max_length=220, blank=True, null=True)
    # place = models.CharField(max_length=220, blank=True, null=True)
    # scribe = models.CharField(max_length=220, blank=True, null=True)
    # folia = models.CharField(max_length=220, blank=True, null=True)
    # manuscript_shelfmark = models.CharField(max_length=220, blank=True, null=True)
    # notes = RichTextField(blank=True, null=True)
    # public = models.BooleanField(default=True)
    # sketch = JSONField(blank=True, null=True)
   
    # define columns that will be returned
    # they should be the fields of your model, and you may customize their displaying contents in render_column()
    # don't worry if your headers are not the same as your field names, you will define the headers in your template
    columns = ['image', 'base_expansion', 'transcription', 'symbol_type', 'text_title', 'date', 'place', 'scribe', 'manuscript_shelfmark',]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns displayed by datatables
    # for non sortable columns use empty value like ''
    order_columns = ['image', 'base_expansion', 'transcription', 'symbol_type', 'text_title', 'date', 'place', 'scribe', 'manuscript_shelfmark',]

    # set max limit of records returned
    # this is used to protect your site if someone tries to attack your site and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):
        # we want to render 'translation' as a custom column, because 'translation' is defined as a Textfield in Image model,
        # but here we only want to check the status of translating process.
        # so, if 'translation' is empty, i.e. no one enters any information in 'translation', we display 'waiting';
        # otherwise, we display 'processing'.
        if column == 'image':
            return mark_safe(format_html(f"<img style='height=100px;' src='/static/symbols/{row.image.name}'>"))

        if column == 'base_expansion':
            return format_html("<p>{}</p>", row.base_expansion,)
        if column == 'transcription':
            return format_html("<p>{}</p>", row.transcription,)
        if column == 'symbol_type':
            return format_html("<p>{}</p>", row.symbol_type)
        if column == 'text_title':
            return format_html("<p>{}</p>", row.text_title,)
        if column == 'date':
            return format_html("<p>{}</p>", row.date)
        if column == 'place':
            return format_html("<p>{}</p>", row.place)
        if column == 'scribe':
            return format_html("<p>{}</p>", row.scribe)
        if column == 'manuscript_shelfmark':
            return format_html("<p>{}</p>",row.manuscript_shelfmark)

        else:
            return super(SymbolJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        pass

        return qs
