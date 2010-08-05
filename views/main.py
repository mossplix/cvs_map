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



#def marker(request,radius=50,color='#1ebfd2',opacity=1.0,text=""):
#    """
#draw marker  given color,width and opacity
#"""
#    radius = int(radius)
#    stroke_width = 1
#    # Defaults
#    fill_color = color
#    stroke_color = '#1f9ecd'
#    opacity = int(opacity)
#    img=make_marker(radius,fill_color,stroke_color,stroke_width,opacity,text)
#    response=HttpResponse(content_type='image/png')
#    img.save(response, 'PNG')
#    return response        
def health_facilities(request,limit=100,start_date=None,end_date=None):
    from cvs.models import Facility
    
    
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
        fac['description']=facility.kind.name
        fac['icon']="/Media/img/"+MAP_TYPES['health_facilities'][0]
        fac['color']=MAP_TYPES['health_facilities'][1]
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
        
        #Dreports=Report.objects.filter(kind__slug='death').order_by('source__time')
        Dreports=DeathReport.objects.order_by('message__time').filter(valid=True)
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        Dreports=DeathReport.objects.filter(valid=True).order_by('message__time').filter(message__time__range=(start_date,end_date))
        
    for dr in Dreports:
        try:
            death={}
            
            death['name']=str(dr.patient.name)
            death['latitude']=str(dr.reporter.healthreporter.facility.latitude)
            death['longitude']=str(dr.reporter.healthreporter.facility.longitude)
            death['type']="EPI"
            death['description']="<p>%s %s</p> "%(str(dr.patient.name), str(dr.patient.age) )
            death['timestamp']=str(dr.message.time)
            death['absolute_url']=""
            death['icon']="/Media/img/"+MAP_TYPES['deaths'][0]
            death['color']=MAP_TYPES['deaths'][1]
            death_reports[str(dr.patient.name)]=death
           
            
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
        birth_reports=NewBirthReport.objects.filter(valid=True).order_by('message__time')
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        birth_reports=NewBirthReport.objects.filter(valid=True).filter(message__time__range=(start_date,end_date)).order_by('message__time')
    for btrt in birth_reports:
        try:
            br={}
            br['latitude']=str(btrt.reporter.healthreporter.facility.latitude)
            br['longitude']=str(btrt.reporter.healthreporter.facility.longitude)    
            br['name']=str(btrt.patient.name)    
            br['type']="Birth"
            br['timestamp']=str(btrt.message.time)
            br['description']=str(btrt.patient.name) + "  age:"+str(btrt.patient.age) 
            br['absolute_url']=""
            br['icon']="/Media/img/"+MAP_TYPES['births'][0]
            br['color']=MAP_TYPES['births'][1]
            breports_dict[str(btrt.patient.name)]=br
        except:
            continue
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
        mauc=MuacReport.objects.filter(valid=True).order_by('message__time')
        
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        mauc=MuacReport.objects.filter(valid=True).filter(message__time__range=(start_date,end_date)).order_by('message__time')
    for mc in mauc:
        try:
            mr={}
            mr['name']=mc.patient.name
            mr['latitude']=str(mc.reporter.healthreporter.facility.latitude)
            mr['longitude']=str(mc.reporter.healthreporter.facility.longitude)
            mr['type']="Malnutrition"
            mr['description']="<p>%s</p> "%(" ".join(str(mc.message).split(",")[1:4]))
            mr['ts']=str(mc.message.time)
            mr['url']=""
            mr['icon']="/Media/img/"+MAP_TYPES['malnutrition'][0]
            mr['color']=MAP_TYPES['malnutrition'][1]
            mauc_reports[str(mc.patient.name)]=mr
        except:
            continue
    return JsonResponse(mauc_reports)
        

def epi_kind(request,kind,start=None,end=None):
    from django.db.models import Sum,Count
    KIND=str(kind)
    try:
        start_date=request.GET.get('start', None)
        end_date=request.GET.get('end',None)
        
    
    except:
        start_date,end_date=None,None
        
        
    #Month=month_options[month][1]
   
    
    epi_obs={}
    if str(start_date)=="undefined" or str(end_date)=="undefined":
        start_date,end_date=None,None
    if start_date==None or end_date==None:
        
        main_query=EpiReport.objects.filter(valid=True,disease=KIND).order_by('message__time')
        
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        main_query=EpiReport.objects.filter(valid=True,disease=KIND).filter(message__time__range=(start_date,end_date)).order_by('message__time')
    facilities=Facility.objects.all()
    n=1
    maxvalue=0
    for facility  in facilities:
        try:
            er = main_query.filter(reporter__healthreporter__facility=facility)
            
            
            if len(er) != 0:
                
            
            
                epi={}
                result=er.aggregate(Sum('value'),Count('value'))
                sum,count=int(result.get('value__sum')),int(result.get('value__count'))
                normalized_value=sum/count
                if normalized_value>maxvalue:
                    maxvalue=normalized_value
                epi['name']= str(er[0].reporter.healthreporter.facility.name)
                
                epi['latitude']=str(er[0].reporter.healthreporter.facility.latitude)
                epi['longitude']=str(er[0].reporter.healthreporter.facility.longitude)
                epi['type']=kind
                epi['data']=normalized_value
                epi['description']="<p>total number of cases: %s</p><p>number of reports: %s</p>"%(sum,count)
                epi['ts']=str(er[0].message.time)
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




