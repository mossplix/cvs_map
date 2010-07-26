from django.shortcuts import  render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from mapping.lib.utils import *
from mapping.lib.marker import *
from mapping.settings import start_date,end_date,MAP_URLS,min_lat,max_lat,min_lon,max_lon,MAP_TYPES
from django.utils.safestring import mark_safe
from django.utils import simplejson
from djangosms.stats.models import *
from djangosms.reporter.models import *
from cvs.models import *
class JsonResponse(HttpResponse):
        """ return json content type   """
        def __init__(self, obj):
            self.original_obj = obj
            HttpResponse.__init__(self, self.serialize())
            self["Content-Type"] = "text/javascript"
    
        def serialize(self):
            return(simplejson.dumps(self.original_obj))



def marker(request,radius=50,color='#1ebfd2',opacity=1.0,text=""):
    """
draw marker  given color,width and opacity
"""
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
    facilities=Facility.objects.all().order_by('name')
    for facility in facilities:
        
        fac={}
        fac['name']=facility.name
        fac['latitude']=str(facility.latitude)
        fac['longitude']=str(facility.longitude)
        fac['type']=facility.kind.name
        fac['timestamp']=""
        fac['absolute_url']=""
        fac['description']=""
        fac['icon']="/marker/25/"+facility_options[str(facility.kind.name)]+"/marker.png"
        facility_dict[str(facility.name)]=fac
    return JsonResponse(facility_dict)

    
month_opts={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Nov":9,"oct":10,"Nov":11,"Dec":12}       
def format_date(date,start=True):
    """ format the date into a python datetime object"""
    import datetime
    month,year=date.split("-")
    month=month_opts[month]
    return datetime.datetime.strptime(year+"-"+str(month)+"-01",'%Y-%m-%d')
    if start==False:
        month=(int(month)+1)%12
        if month==0:
            month=1
            year=year+1
        return datetime.datetime.strptime(year+"-"+str(month)+"-01",'%Y-%m-%d')
          
def deaths(request):
    try:
        start_date=request.GET.get('start', None)
        end_date=request.GET.get('end',None)
        
    
    except:
        start_date,end_date=None,None
        
        
    #Month=month_options[month][1]
    
    death_reports={}
    if str(start_date)=="undefined" or str(end_date)=="undefined":
        start_date,end_date=None,None
    if start_date==None or end_date==None:
        
        Dreports=Report.objects.filter(kind__slug='death').order_by('source__time')
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        Dreports=Report.objects.filter(kind__slug='death').filter(source__time__range=(start_date,end_date)).order_by('source__time')
    n=1
    for dr in Dreports:
        try:
            death={}
            
            death['name']=""
            death['latitude']=str(dr.source.connection.user.reporter.healthreporter.facility.latitude)
            death['longitude']=str(dr.source.connection.user.reporter.healthreporter.facility.longitude)
            death['type']="EPI"
            death['description']="<p>%s</p> "%(" ".join(str(dr.source).split(",")[1:4]))
            death['timestamp']=str(dr.source.time)
            death['absolute_url']=""
            death['icon']="/marker/25/black/Dth/marker.png"
            death_reports[n]=death
            n=n+1
            
        except:
            continue
    return JsonResponse(death_reports)
def births(request):
    try:
        start_date=request.GET.get('start', None)
        end_date=request.GET.get('end',None)
        
    
    except:
        start_date,end_date=None,None
        
        
    breports_dict={}
    if str(start_date)=="undefined" or str(end_date)=="undefined":
        start_date,end_date=None,None
    if start_date==None or end_date==None:
        birth_reports=BirthReport.objects.all().order_by('source__time')
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        birth_reports=BirthReport.objects.all().filter(source__time__range=(start_date,end_date)).order_by('source__time')
    for btrt in birth_reports:
        br={}
        br['name']=str(btrt.patient.name)
        br['latitude']=str(btrt.patient.last_reported_on_by.reporter.healthreporter.facility.latitude)
        br['longitude']=str(btrt.patient.last_reported_on_by.reporter.healthreporter.facility.longitude)
        br['type']="Birth"
        br['timestamp']=str(btrt.source.time)
        br['description']=""
        br['absolute_url']=""
        br['icon']="/marker/25/orange/Bth/marker.png"
        breports_dict[str(btrt.patient.name)]=br
    return JsonResponse(breports_dict)
def malnutrition(request,start_date=None,end_date=None):
    try:
        start_date=request.GET.get('start', None)
        end_date=request.GET.get('end',None)
        
    
    except:
        start_date,end_date=None,None
        
        
    #Month=month_options[month][1]
    
    mauc_reports={}
    if str(start_date)=="undefined" or str(end_date)=="undefined":
        start_date,end_date=None,None
    if start_date==None or end_date==None:
        mauc=NutritionReport.objects.all().order_by('source__time')
        
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        mauc=NutritionReport.objects.all().filter(source__time__range=(start_date,end_date)).order_by('source__time')
    for mc in mauc:
        try:
            mr={}
            mr['name']=mc.patient.name
            mr['latitude']=str(mc.patient.last_reported_on_by.reporter.healthreporter.facility.latitude)
            mr['longitude']=str(mc.patient.last_reported_on_by.reporter.healthreporter.facility.longitude)
            mr['type']="Malnutrition"
            mr['description']="<p>%s</p> "%(" ".join(str(mc.source).split(",")[1:4]))
            mr['ts']=str(mc.source.time)
            mr['url']=""
            mr['icon']="/Media/img/pin.png"
            mauc_reports[str(mc.patient.name)]=mr
        except:
            continue
    return JsonResponse(mauc_reports)
        

def epi_kind(request,kind,start=None,end=None):
    from django.db.models import Sum,Count
    kind=str(kind)
    try:
        start_date=request.GET.get('start', None)
        end_date=request.GET.get('end',None)
        
    
    except:
        start_date,end_date=None,None
        
        
    #Month=month_options[month][1]
    KIND="epidemiological_observations_%s"%kind
    epi_obs={}
    if str(start_date)=="undefined" or str(end_date)=="undefined":
        start_date,end_date=None,None
    if start_date==None or end_date==None:
        
        main_query=Observation.objects.filter(kind__slug=KIND).order_by('report__source__time')
        
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        main_query=Observation.objects.filter(kind__slug=KIND).filter(report__source__time__range=(start_date,end_date)).order_by('report__source__time')
    facilities=Facility.objects.all()
    n=1
    maxvalue=0
    for facility  in facilities:
        try:
            er = main_query.filter(report__source__connection__user__reporter__healthreporter__facility=facility)
            if len(er) != 0:
            
            
                epi={}
                result=er.aggregate(Sum('value'),Count('value'))
                sum,count=int(result.get('value__sum')),int(result.get('value__count'))
                normalized_value=sum/count
                if normalized_value>maxvalue:
                    maxvalue=normalized_value
                epi['name']= str(er[0].report.source.connection.user.reporter.healthreporter.facility.name)
                
                epi['latitude']=str(er[0].report.source.connection.user.reporter.healthreporter.facility.latitude)
                epi['longitude']=str(er[0].report.source.connection.user.reporter.healthreporter.facility.longitude)
                epi['type']=kind
                epi['data']=normalized_value
                epi['description']="<p>total number of cases: %s</p><p>number of reports: %s</p>"%(sum,count)
                epi['ts']=str(er[0].report.source.time)
                epi['url']=""
                if kind in MAP_TYPES.keys():
                    epi['icon']="/Media/img/"+MAP_TYPES[kind][0]
                    epi['color']=MAP_TYPES[kind][1]
                else:
                    epi['icon']="/marker/25/orange/%s/marker.png"%kind
                epi_obs[n]=epi
                n=n+1
            
        except:
            continue
    epi_obs['maxvalue']=maxvalue
    return JsonResponse(epi_obs)
    
def map(request):
    Map_urls=mark_safe(simplejson.dumps(MAP_URLS))
    map_types=mark_safe(simplejson.dumps(MAP_TYPES))
    minLon,maxLon,minLat,maxLat=mark_safe(min_lat),mark_safe(max_lat),mark_safe(min_lon),mark_safe(max_lon)
    slider_ranges=date_range(start_date,end_date)
    return render_to_response("map.html",locals())




