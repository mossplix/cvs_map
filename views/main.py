from django.shortcuts import  render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from mapping.lib.utils import *
from mapping.lib.marker import *
from mapping.settings import start_date,end_date,MAP_URLS,min_lat,max_lat,min_lon,max_lon,MAP_TYPES,MAP_KEY
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


def geoCode(name):
    
    """
    use geonames to geocode the locations
    """
    from xml.dom import minidom
    import urllib
    
    url="http://ws.geonames.org/search?q=%s&maxRows=1&style=SHORT&lang=en&country=ug"%name
    raw_data=urllib.urlopen(url).read()
    xmldoc = minidom.parseString(raw_data)
    lng=float(xmldoc.getElementsByTagName('lng')[0].childNodes[0].data)
    lat=float(xmldoc.getElementsByTagName('lat')[0].childNodes[0].data)
    return (lat,lng)
    
    
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
def getZoomFacilities(zoom):
    """
    get the facilities at a given zoom
    """
    if zoom<=8:
        return ["Hospital"]
    elif zoom ==9:
        return ["Hospital","HCIV"]
    elif zoom in [10,11]:
        return ["Hospital","HCIV","HCIII"]
    elif zoom >11:
        return ["Hospital","HCIV","HCIII","HCII"]
          
def health_facilities(request):
    from cvs.models import Facility
    try:
        zoom=int(request.GET.get('zoom', 8))
    
    except:
        zoom=8
    
    facility_dict={}
    facilities=Facility.objects.all().order_by('name').filter(kind__name__in=getZoomFacilities(zoom))
    for facility in facilities:
        
        fac={}
        fac['name']=facility.name
        fac['latitude']=str(facility.latitude)
        fac['longitude']=str(facility.longitude)
        fac['type']="health_facilities"
        fac['timestamp']=""
        fac['absolute_url']=""
        fac['description']=facility.kind.name
        fac['zoom']=zoom
#        fac['icon']="/Media/img/"+MAP_TYPES['health_facilities'][0]
        fac['icon']="http://chart.apis.google.com/chart?chst=d_simple_text_icon_below&chld=%s (%s)|12|14740A|medical|12|FF8888|FFF"%(facility.name,facility.kind.name)
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
    facilities=Facility.objects.all()
    maxvalue=0
    n=1
        
   
    for facility in facilities:
        
        
        try:
            dr=Dreports.filter(reporter__healthreporter__facility=facility)
            if len(dr) !=0:
                death={}
#                import pdb
#                pdb.set_trace()
                death['name']="Facility:" +str(dr[0].reporter.healthreporter.facility.name)
                death['latitude']=str(dr[0].reporter.healthreporter.facility.latitude)
                death['longitude']=str(dr[0].reporter.healthreporter.facility.longitude)
                death['type']="deaths"
                total_deaths=dr.count()
                if total_deaths>maxvalue:
                    maxvalue=total_deaths
                death['data']=total_deaths
                death['type']="deaths"
                death['description']="total_deaths: "+str(total_deaths)
                death['timestamp']=""
                death['absolute_url']=""
                death['icon']="/Media/img/"+MAP_TYPES['deaths'][0]
                death['color']=MAP_TYPES['deaths'][1]
                death_reports[n]=death
                n=n+1
           
            
        except:
            continue
    death_reports['maxvalue']=maxvalue
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
    facilities=Facility.objects.all()
    maxvalue=0
    n=1
    
    for facility in facilities:
        try:
            btrt=birth_reports.filter(reporter__healthreporter__facility=facility)
            br={}
            br['latitude']=str(btrt[0].reporter.healthreporter.facility.latitude)
            br['longitude']=str(btrt[0].reporter.healthreporter.facility.longitude)   
            br['name']="Facility: "+str(btrt[0].reporter.healthreporter.facility.name)    
            br['type']="births"
            birth_count=btrt.count()
            if birth_count>maxvalue:
                maxvalue=birth_count
            br['data']=birth_count
            br['timestamp']=""
            br['description']="Birth Reports: "+str(birth_count)
            br['absolute_url']=""
            br['icon']="/Media/img/"+MAP_TYPES['births'][0]
            br['color']=MAP_TYPES['births'][1]
            breports_dict[n]=br
            n=n+1
        except:
            continue
    breports_dict['maxvalue']=maxvalue
    
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
    facilities=Facility.objects.all()
    maxvalue=0
    n=1
    #for mc in mauc:
    for facility in facilities:
        
        try:
            mc=mauc.filter(reporter__healthreporter__facility=facility)
            mr={}
            mr['name']="Facility:"+str(mc[0].reporter.healthreporter.facility.name)
            mr['latitude']=str(mc[0].reporter.healthreporter.facility.latitude)
            mr['longitude']=str(mc[0].reporter.healthreporter.facility.longitude)
            mr['type']="malnutrition"
            
            mauc_count=mc.count()
            if mauc_count>maxvalue:
                maxvalue=mauc_count
            mr['data']=mauc_count
            mr['description']="Number Of Cases:"+str(mauc_count)
            mr['ts']=""
            mr['url']=""
            mr['icon']="/Media/img/"+MAP_TYPES['malnutrition'][0]
            mr['color']=MAP_TYPES['malnutrition'][1]
            mauc_reports[n]=mr
            n=n+1
        except:
            continue
    mauc_reports['maxvalue']=maxvalue
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
    map_key=MAP_KEY
    Map_urls=mark_safe(simplejson.dumps(MAP_URLS))
    map_types=mark_safe(simplejson.dumps(MAP_TYPES))
    minLon,maxLon,minLat,maxLat=mark_safe(min_lat),mark_safe(max_lat),mark_safe(min_lon),mark_safe(max_lon)
    slider_ranges=date_range(start_date,end_date)
    return render_to_response("map.html",locals(),context_instance=RequestContext(request))




