from django.template.context import RequestContext
from django.template.base import TemplateDoesNotExist
from django.shortcuts import render_to_response
from django.http import HttpResponse
from piston.emitters import Emitter
from util.toshp import OpenClimateShp
from util.helpers import get_temp_path

from util.ncconv.in_memory_oo_multi_core import as_geojson, as_tabular,\
    as_keyTabular

class OpenClimateEmitter(Emitter):
    """
    Superclass for all OpenClimateGIS emitters.
    """
    def render(self,request):
        raise NotImplementedError


class IdentityEmitter(OpenClimateEmitter):
    """
    The standard Django Piston emitter does unnecessary computations when an
    emitter is searching for the raw data from its associated handler.
    """
    
    def construct(self):
        return self.data


class HelloWorldEmitter(OpenClimateEmitter):
    
    def render(self,request):
        names = [n['name'] for n in self.construct()]
        msg = 'Hello, World!! The climate model names are:<br><br>{0}'.format('<br>'.join(names))
        return HttpResponse(msg)


class HTMLEmitter(Emitter):
    """Emits an HTML representation 
    """
    def render(self, request):
        from handlers import ApiHandler
        
        c = RequestContext(request)
        
        if isinstance(self.handler, ApiHandler):
            # return the API HTML page (not based on a data model)

            response = render_to_response(
                template_name='api.html', 
                context_instance=c,
            )
        else:
            if request.url_args.has_key('is_collection'):
                is_collection = request.url_args['is_collection']
            else:
                None
            try:
                # use the HTML template that matches the data model name
                template_name = self.data.model._meta.object_name + '.html'
                response = render_to_response(
                    template_name=template_name, 
                    dictionary={
                        'data': self.construct(), 
                        'is_collection': is_collection,
                    },
                    context_instance=c,
                )
            except TemplateDoesNotExist:
                # render the default HTML response
                response = render_to_response(
                    template_name='default_html_emitter.html',
                    dictionary={
                        'data': self.construct(), 
                        'is_collection': is_collection,
                    },
                    context_instance=c,
                )
        return response
Emitter.register('html', HTMLEmitter, 'text/html; charset=utf-8')


class ShapefileEmitter(IdentityEmitter):
    """
    Emits zipped shapefile (.shz)
    """
    
    def render(self,request):
        elements = self.construct()
        path = get_temp_path(suffix='.shp')
        shp = OpenClimateShp(path,elements)
        shp.write()
        return shp.zip_response()


class KmlEmitter(IdentityEmitter):
    """
    Emits raw KML (.kml)
    """

    def render(self,request):
        pass


class KmzEmitter(KmlEmitter):
    """
    Subclass of KmlEmitter. Emits KML in a zipped format (.kmz)
    """
    
    def render(self,request):
        kml = super(KmzEmitter,self).render()


class GeoJsonEmitter(IdentityEmitter):
    """
    JSON format for geospatial data (.json)
    """
    
    def render(self,request):
        ## return the elements
        elements = self.construct()
        ## conversion
        conv = as_geojson(elements)
        return(conv)


class CsvEmitter(IdentityEmitter):
    """
    Tabular CSV format. (.csv)
    """
    
    def render(self,request):
        elements = self.construct()
        var = request.ocg.simulation_output.netcdf_variable.code
        conv = as_tabular(elements,var)
        return(conv)


class CsvKeyEmitter(IdentityEmitter):
    """
    Tabular CSV format reduced to relational tables. (.csv)
    """
    
    def render(self,request):
        elements = self.construct()
        var = request.ocg.simulation_output.netcdf_variable.code
        conv = as_keyTabular(elements,var)
        print(conv)
        return(conv)


#Emitter.register('helloworld',HelloWorldEmitter,'text/html; charset=utf-8')
Emitter.register('shz',ShapefileEmitter,'application/zip; charset=utf-8')
#Emitter.unregister('json')
Emitter.register('geojson',GeoJsonEmitter,'application/geojson; charset=utf-8')
Emitter.register('csv',CsvEmitter,'text/html; charset=utf-8')
Emitter.register('kcsv',CsvKeyEmitter,'text/html; charset=utf-8')