from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from greek_app.models import Symbol, Type
from greek_app.similarity import similarity
from django.utils.html import escape, format_html, mark_safe
import json

def home(request):
    context = {}
    if request.POST:

        data = request.POST.get('data',None)
        results = []
        if data:
            data = json.loads(data)
            symbols = Symbol.objects.all()
            for symbol in symbols:
                symbol_dict = symbol.__dict__
                symbol_type_id = symbol_dict.get('symbol_type_id')
                if  symbol_type_id:
                    symbol_dict['symbol_type'] = Type.objects.get(id=symbol_type_id).name

                if not symbol.sketch is None:
                    similarity0 = similarity(data, symbol.sketch)
                    symbol_dict['similarity'] = round(similarity0['dh'],4)
                else:
                     symbol_dict['similarity'] = 0
                
                results.append(symbol_dict)
                
        context['symbols'] = results

        return render(request, 'index.html', context)
    else:
        symbols = [s.__dict__ for s in Symbol.objects.all()]
        for symbol in symbols:
            symbol_type_id = symbol.get('symbol_type_id')
            if  symbol_type_id:
                symbol['symbol_type'] = Type.objects.get(id=symbol_type_id).name
            
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
    return render(request, 'symbols.html', context)

def logout_view(request):
    logout(request)
    return redirect(home)



class SymbolJson(BaseDatatableView):
    # the model you're going to show
    model = Symbol

   
    # define columns that will be returned
    # they should be the fields of your model, and you may customize their displaying contents in render_column()
    # don't worry if your headers are not the same as your field names, you will define the headers in your template
    columns = ['image', 'expansion', 'transcription', 'type', 'text', 'date', 'place', 'scribe', 'manuscript',]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns displayed by datatables
    # for non sortable columns use empty value like ''
    order_columns = ['image', 'expansion', 'transcription', 'type', 'text', 'date', 'place', 'scribe', 'manuscript',]

    # set max limit of records returned
    # this is used to protect your site if someone tries to attack your site and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):
        # we want to render 'translation' as a custom column, because 'translation' is defined as a Textfield in Image model,
        # but here we only want to check the status of translating process.
        # so, if 'translation' is empty, i.e. no one enters any information in 'translation', we display 'waiting';
        # otherwise, we display 'processing'.
        if column == 'image':
            return mark_safe(format_html(f"<img style='height=10px;' src='/static/{row.image.name}'>"))

        if column == 'expansion':
            return format_html("<p>{}</p>", row.expansion,)
        if column == 'transcription':
            return format_html("<p>{}</p>", row.transcription,)
        if column == 'type':
            return format_html("<p>{}</p>", row.type)
        if column == 'text':
            return format_html("<p>{}</p>", row.text,)
        if column == 'date':
            return format_html("<p>{}</p>", row.date)
        if column == 'place':
            return format_html("<p>{}</p>", row.place)
        if column == 'scribe':
            return format_html("<p>{}</p>", row.scribe)
        if column == 'manuscript':
            return format_html("<p>{}</p>",row.manuscript)

        else:
            return super(SymbolJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        pass

        return qs
