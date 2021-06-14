import json

from string import capwords

from django.forms import CheckboxInput, Select, SelectMultiple
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.conf import settings


class selectfilterwidget(Select):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelChoiceField
    """

    def __init__(
            self,
            fields,
            filter,
            *args,
            **kwargs
    ):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(selectfilterwidget, self).__init__(*args, **kwargs)
        self.fields = fields
        self.filter = filter

    def render(self, name, value,
               attrs=None, choices=(), **kwargs):
        if value is None:
            value = []
        output = []
        modal_name = 'modal' + escape(name)
        modal_add_button = 'modal_add_button_' + escape(name)
        output.append("<div id='{}widget'>".format(escape(name)))
        output.append(
            '''<div  class="openmodal{}">
<select name="{}" id="id_{}" class="{}"   style="width:75%"></select></div>
			<!-- Modal -->
            <div class="modal fade" id="{}" tabindex="-1" role="dialog" aria-hidden="false">
                <div class="modal-dialog modal-dialog-scrollable" role="document">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="false">&times;</span>
                            </button>
                        </div>
                    <div class="modal-body" >'''.format(escape(modal_name), escape(name), escape(name), escape(name),
                                                        escape(modal_name)))
        # head = self.render_head()
        # output.append(head)
        #  body = self.render_body(name, value, attrs, **kwargs)
        #  output.append(body)
        output.append(
            ' <button id="filter{}"  class="btn btn-primary btn-full-width"  name="search"> Search </button> '.format(
                escape(name)))

        for field in self.filter:
            output.append(
                " <div class='col-sm'> <label >{}</label> <input type='text' id='{}'> </div>".format(field, field))

        output.append('''
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                Search Results
                            </h4>
                        </div>
                            <div class="panel-body">
                                <div class="col-sm-12" id='results_wrapped'>
                                    <table id="results{}" class="table table-striped table-bordered"> </table>
                                </div>
                            </div>
                    </div>'''.format(escape(name)))
        output.append('''</div> <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            <button type="button" id="{}" class="btn btn-primary">Add selected rows</button>
                       </div></div> </div> </div>'''.format(escape(modal_add_button)))
        output.append(
            "<script>$('.openmodal{}').click(function(){{ $('#{}').modal('show');}}); var table;</script>".format(
                escape(modal_name), escape(modal_name)))
        output.append(" <script>  $('#filter{}').click(function(e) ".format(escape(name)))
        output.append(''' {{ e.preventDefault();
	     var content={{}};
		$("#{}widget input").each(function(e)
		{{	
		var key = this.id;
        if (typeof key === "undefined") {{
            return
        }}
         //avoid empty shadowed parameters
         if(this.value != ''){{
            content[key] = this.value;
         }}
		}});
		console.log(content)
        '''.format(escape(name)))
        output.append(' table = $("#results{}").DataTable( '.format(escape(name)))
        output.append('''		
		{
                "searching": false,
                "paging": true,
                "pageLength": 25,
                "serverSide": true,
                "order": [[0, "asc"]],
				"select": 'single',
                "destroy": true,
                "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
			    "ajax": {
		''')
        output.append(' "url": "{}/{}/" ,'.format(settings.BACKEND, escape(name)))
        output.append('''
                    "data": content,
                    "type": "POST"
                },
                columns: [	''')
        for column in self.fields:
            output.append("	{{data: '{}' , 'title': '{}'}},".format(column, column))
        output.append('''			
                ],

            });
			table.on('select.dt', function() {
			  var array = [];
			  table.rows('.selected').every(function(rowIdx) {
				 array.push(table.row(rowIdx).data())
			  })   
			  console.log(array);
			})
        })


</script>
             ''')
        output.append('''<script>
								$("#{}").click(function()
								{{  
								  table.rows(".selected").every(function(rowIdx) {{
								  var newOption = new Option(table.row(rowIdx).data()["name"], table.row(rowIdx).data()["id"], true, true);
								$('.{}').append(newOption).trigger('change');
									 console.log(table.row(rowIdx).data()["id"])
									 console.log(table.row(rowIdx).data()["name"])
								  }});   
								   table.clear().destroy();
								   //table.draw();
								  $("#{}").modal("hide");
								 }})</script>'''.format(modal_add_button, escape(name), modal_name))
        output.append("<script>$(document).ready(function() {{  $('.{}').select2(); }});</script>".format(escape(name)))
        output.append("</div>")

        return mark_safe('\n'.join(output))


class multiselectfilterwidget(SelectMultiple):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelMultipleChoiceField
    """

    def __init__(
            self,
            fields,
            filter,
            *args,
            **kwargs
    ):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(multiselectfilterwidget, self).__init__(*args, **kwargs)
        self.fields = fields
        self.filter = filter

    def render(self, name, value,
               attrs=None, choices=(), **kwargs):
        if value is None:
            value = []
        output = []
        modal_name = 'modal' + escape(name)
        modal_add_button = 'modal_add_button_' + escape(name)
        output.append("<div id='{}widget'>".format(escape(name)))
        output.append(
            '''<div  class="openmodal{}">
<select name="{}" id="id_{}"  class="{}"  multiple="multiple" style="width:75%"></select></div>
			<!-- Modal -->
            <div class="modal fade" id="{}" tabindex="-1" role="dialog" aria-hidden="false">
                <div class="modal-dialog modal-dialog-scrollable" role="document">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="false">&times;</span>
                            </button>
                        </div>
                    <div class="modal-body" >'''.format(escape(modal_name), escape(name), escape(name), escape(name),
                                                        escape(modal_name)))
        # head = self.render_head()
        # output.append(head)
        #  body = self.render_body(name, value, attrs, **kwargs)
        output.append(
            ' <button id="filter{}"  class="btn btn-primary btn-full-width"  name="search"> Search </button> '.format(
                escape(name)))

        for field in self.filter:
            output.append(
                " <div class='col-sm'> <label >{}</label> <input type='text' id='{}'> </div>".format(field, field))

        output.append('''
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                Search Results
                            </h4>
                        </div>
                            <div class="panel-body">
                                <div class="col-sm-12" id='results_wrapped'>
                                    <table id="results{}" class="table table-striped table-bordered"> </table>
                                </div>
                            </div>
                    </div>'''.format(escape(name)))
        output.append('''</div> <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            <button type="button" id="{}" class="btn btn-primary">Add selected rows</button>
                       </div></div> </div> </div>'''.format(escape(modal_add_button)))

        output.append(
            "<script>$('.openmodal{}').click(function(){{ $('#{}').modal('show');}}); var table; </script>".format(
                escape(modal_name), escape(modal_name)))
        output.append(" <script>  $('#filter{}').click(function(e) ".format(escape(name)))
        output.append(''' {{ e.preventDefault();
	    var content={{}};
		$("#{}widget input").each(function(e)
		{{	
		var key = this.id;
        if (typeof key === "undefined") {{
            return
        }}

         //avoid empty shadowed parameters
         if(this.value != ''){{
            content[key] = this.value;
         }}
		}});
		console.log(content)
        '''.format(escape(name)))
        output.append(' table = $("#results{}").DataTable( '.format(escape(name)))
        output.append('''		
		{
                "searching": false,
                "paging": true,
                "pageLength": 25,
                "serverSide": true,
                "order": [[0, "asc"]],
                "destroy": true,
                "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
				 select: {
					style: "multi"
				},
                "ajax": {
		''')
        output.append(' "url": "{}/{}/" ,'.format(settings.BACKEND, escape(name)))
        output.append('''
        		"data": content,
                    "type": "POST"
                },
                   columns: [	''')
        for column in self.fields:
            output.append("	{{data: '{}' , 'title': '{}'}},".format(column, column))
        output.append('''			
                ],
            });
        })
</script>
             ''')

        output.append('''<script>
								$("#{}").click(function()
								{{  
								  table.rows(".selected").every(function(rowIdx) {{
								  var newOption = new Option(table.row(rowIdx).data()["name"], table.row(rowIdx).data()["id"].toString(), true, true);
								$('.{}').append(newOption).trigger('change');
									 console.log(table.row(rowIdx).data()["id"])
									 console.log(table.row(rowIdx).data()["name"])
								  }});   
								   table.clear().destroy();
								//  table.draw();
								  $("#{}").modal("hide");
								 }})</script>'''.format(modal_add_button, escape(name), modal_name))
        output.append("<script>$(document).ready(function() {{  $('.{}').select2(); }});</script>".format(escape(name)))
        output.append("</div>")
        return mark_safe('\n'.join(output))


def get_underscore_attrs(attrs, item):
    for attr in attrs.split('__'):
        if callable(attr):
            item = attr(item)
        elif callable(getattr(item, attr)):
            item = getattr(item, attr)
        else:
            item = getattr(item, attr)
    if item is None:
        return ""
    return item


def clean_underscores(string):
    """
    Helper function to clean up table headers.  Replaces underscores
    with spaces and capitalizes words.
    """
    s = capwords(string.replace("_", " "))
    return s