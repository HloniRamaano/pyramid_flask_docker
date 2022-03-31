import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator

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


here = os.path.dirname(os.path.abspath(__file__))

class MySchema(MappingSchema):
    add_item = SchemaNode(String(),
                       widget = widget.TextInputWidget(size=40),
                       validator = Length(max=10),
                       description = 'A very short title')
    
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
        except ValidationFailure as e:
            template_values['form'] = e.render()
        else:
            template_values['form'] = 'OK'
            
        return template_values
    
    

    template_values['form'] = myform.render()
    return template_values

if __name__ == '__main__':
    settings = dict(reload_templates=True)
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_view(form_view, renderer=os.path.join(here, 'form.pt'))
    config.add_static_view('static', 'deform:static')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5432, app)
    server.serve_forever()