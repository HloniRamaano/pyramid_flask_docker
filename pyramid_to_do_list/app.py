from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import requests
import os
from pyramid.renderers import render_to_response

here = os.path.dirname(os.path.abspath(__file__))

from colander import (
    Boolean,
    Integer,
    Length,
    MappingSchema,
    OneOf,
    SchemaNode,
    SequenceSchema,
    String
)

from deform import (
    Form,
    ValidationFailure,
    widget
)

@view_config(
    route_name='home',
    renderer='templates/home.jinja2'
)
def home(request):
    response = requests.get("http://127.0.0.1:5000/list/")
    
    lists = response.json()
    print(lists)
    return {"Lists": lists}

@view_config(
    route_name='search_page',
    renderer='templates/search.jinja2'
)
def search_page(request, search_item):
    serviceurl = 'http://127.0.0.1:5000/search/' + search_item + "/"
    payload = {'item': search_item}
    r = requests.post(serviceurl, data=payload)
    print(r.json())
    
    search_list = r.json()
    
    return {"Lists": search_list}

class MySchema(MappingSchema):
    add_item = SchemaNode(String(),
                       widget = widget.TextInputWidget(size=40),
                       validator = Length(max=10),
                       description = 'Add New Item on list here')

@view_config(
    route_name='add',
    renderer='form.pt'
)
def form_view(request):
    schema = MySchema()
    myform = Form(schema, buttons=('submit',))
    template_values = {}
    template_values.update(myform.get_widget_resources())

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = myform.validate(controls)
            print (appstruct['add_item'])
            new_item = appstruct['add_item']
            serviceurl = 'http://127.0.0.1:5000/add/' + new_item + "/"
            payload = {'item': new_item}
            r = requests.post(serviceurl, data=payload)
            print(r.text)
            
        except ValidationFailure as e:
            template_values['form'] = e.render()
        else:
            template_values['form'] = 'Welldone, Item was successfully added, you a Star!!!'
            
        return template_values
    
    template_values['form'] = myform.render()
    return template_values

class MySchemaSearch(MappingSchema):
    search_item = SchemaNode(String(),
                       description = 'Search Items on the list here')
    
@view_config(
    route_name='search',
    renderer='form_search.pt'
)
def form_view_search(request):
    schema = MySchemaSearch()
    myform = Form(schema, buttons=('submit',))
    template_values = {}
    template_values.update(myform.get_widget_resources())
    search_item = ''
    
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = myform.validate(controls)
        except ValidationFailure as e:
            template_values['form'] = e.render()
        else:
            template_values['form'] = 'OK'
            print (appstruct['search_item'])
            search_item = appstruct['search_item']
            serviceurl = 'http://127.0.0.1:5000/search/' + search_item + "/"
            payload = {'item': search_item}
            r = requests.post(serviceurl, data=payload)
            print(r.json())
    
            search_list = r.json()
            return render_to_response('templates/search.jinja2',
                              {'Lists':search_list},
                              request=request)
            
        
        # return template_values

    template_values['form'] = myform.render()
    return template_values

def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("Button Clicked")

if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_chameleon')
        config.add_route('home', '/')
        config.add_route('add', '/add')
        config.add_route('search', '/search')
        config.add_route('search_page', '/search/results')
        config.add_view(form_view, renderer=os.path.join(here, 'form.pt'))
        config.add_static_view('static', 'deform:static')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()