from django.shortcuts import  render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from mapping.lib.utils import *
from mapping.lib.marker import *
from mapping.settings import start_date,end_date,MAP_URLS,min_lat,max_lat,min_lon,max_lon
from django.utils.safestring import mark_safe
from django.utils import simplejson


class JsonResponse(HttpResponse):
        """ return json content type   """
        def __init__(self, obj):
            self.original_obj = obj
            HttpResponse.__init__(self, self.serialize())
            self["Content-Type"] = "text/javascript"
    
        def serialize(self):
            return(simplejson.dumps(self.original_obj))

"""
draw marker  given color,width and opacity
"""

def marker(request,radius=50,color='#1ebfd2',opacity=1.0,text=""):
    radius = int(radius)
    stroke_width = 1
    # Defaults
    fill_color = color
    stroke_color = '#1f9ecd'
    opacity = int(opacity)
    img=make_marker(radius,fill_color,stroke_color,stroke_width,opacity,text)
    response=HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response        
def health_facilities(request,limit=100,start_date=None,end_date=None):
    from cvs.models import Facility
    facility_options={"HCI":"Hc1","HCII":"Hc2","HCIII":"Hc3","HCIV":"Hc4","Ministry":"Min",\
                      "District Health Office":"DHO","Hospital":"Hos"}
    
    facility_dict={}
    facilities=Facility.objects.all().order_by('name')[0:3]
    for facility in facilities:
        
        fac={}
        fac['name']=facility.name
        fac['latitude']=str(facility.latitude)
        fac['longitude']=str(facility.longitude)
        fac['type']=facility.kind.name
        fac['timestamp']=""
        fac['absolute_url']=""
        fac['icon']="/marker/25/"+facility_options[str(facility.kind.name)]+"/marker.png"
        facility_dict[str(facility.name)]=fac
        
    #facility_data.append(facility_dict)
        
  
    return JsonResponse(facility_dict)
def epi(request,start=None,end=None):
    pass
def map(request):
    Map_urls=mark_safe(simplejson.dumps(MAP_URLS))
    minLon,maxLon,minLat,maxLat=mark_safe(min_lat),mark_safe(max_lat),mark_safe(min_lon),mark_safe(max_lon)
    slider_ranges=date_range(start_date,end_date)
    return render_to_response("map.html",locals())




