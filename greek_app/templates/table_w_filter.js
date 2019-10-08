<script>

    $('#example-table').datatable({
    pageSize: 50,
    sort: [true, true, true, true, true, true, true, true, true],
    filters: [false, true, true, 'select', true, true, true, true, 'select'],
    filterText: 'search',
    onChange: function(old_page, new_page){
      console.log('changed from ' + old_page + ' to ' + new_page);
    }
}) ;



    </script>

/*
Good examples
https://codepen.io/sfauch1/pen/YGWGyN
https://codepen.io/hoogw/pen/vJrzGB
*/

{% for symbol in symbols %}
              <tr>
                 <td><img style="height=10px;" src="{% static symbol.image.name  %}"></td>
                 <td>{{ symbol.expansion|default_if_none:"" }}</td>
              <td>{{ symbol.transcription|default_if_none:"" }}</td>
              <td>{{ symbol.type|default_if_none:"" }}</td>
                <td>{{ symbol.text|default_if_none:"" }}</td>
              <td>{{ symbol.date|default_if_none:"" }}</td>
              <td>{{ symbol.place|default_if_none:"" }}</td>
              <td>{{ symbol.scribe|default_if_none:"" }}</td>
              <td>{{ symbol.manuscript|default_if_none:"" }}</td>
              </tr>
          {% endfor %}