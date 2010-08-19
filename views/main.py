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

          
def health_facilities(request):
    from cvs.models import Facility,HealthReporter
    try:
        zoom=int(request.GET.get('zoom', 8))
        type=int(request.GET.get('type', 0))
    
    except:
        zoom=8
        type=0
    
    facility_list=[]
    facilities=Facility.objects.all().order_by('name').all()
    facilities_with_reporters=[hc.facility for hc in HealthReporter.objects.all()]
    
    
    for facility in facilities:
        
        fac={}
        fac['title']=facility.name
        fac['lat']=str(facility.latitude)
        fac['lon']=str(facility.longitude)
        fac['desc']=facility.kind.name
        fac['icon']="/Media/img/"+facility.kind.name+".png"
        if facility in facilities_with_reporters:
            fac['icon']="/Media/img/R"+facility.kind.name+".png"
        if zoom>10 and type==1:
            fac['icon']="http://chart.apis.google.com/chart?chst=d_text_outline&chld=FF8888|18|l|000000|_|%s|"%(facility.name)      
        fac['color']=MAP_TYPES['health_facilities'][1]
        facility_list.append(fac)
    return JsonResponse(facility_list)

    
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
    
    death_reports=[]
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

   
    for facility in facilities:
        
        
        try:
            dr=Dreports.filter(reporter__healthreporter__facility=facility)
            if len(dr) !=0:
                death={}
#                import pdb
#                pdb.set_trace()
                death['title']="Facility:" +str(dr[0].reporter.healthreporter.facility.name)
                death['lat']=str(dr[0].reporter.healthreporter.facility.latitude)
                death['lon']=str(dr[0].reporter.healthreporter.facility.longitude)
                total_deaths=dr.count()
                if total_deaths>maxvalue:
                    maxvalue=total_deaths
                death['heat']=total_deaths
                death['desc']="total_deaths: "+str(total_deaths)
                death['icon']="/Media/img/"+MAP_TYPES['deaths'][0]
                death['color']=MAP_TYPES['deaths'][1]
                death_reports.append(death)
               
                
           
            
        except:
            continue
        ##get percentage heat values
    for t in death_reports:
        t['heat']=t['heat']/float(maxvalue)
    return JsonResponse(death_reports)
def births(request):
    try:
        start_date=request.GET.get('start', None)
        end_date=request.GET.get('end',None)
        
    
    except:
        start_date,end_date=None,None
        
        
    breports_dict=[]
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
    
    
    for facility in facilities:
        try:
            btrt=birth_reports.filter(reporter__healthreporter__facility=facility)
            br={}
            br['lat']=str(btrt[0].reporter.healthreporter.facility.latitude)
            br['lon']=str(btrt[0].reporter.healthreporter.facility.longitude)   
            br['title']="Facility: "+str(btrt[0].reporter.healthreporter.facility.name)    
            birth_count=btrt.count()
            if birth_count>maxvalue:
                maxvalue=birth_count
            br['heat']=birth_count
            br['desc']="Birth Reports: "+str(birth_count)
            br['icon']="/Media/img/"+MAP_TYPES['births'][0]
            br['color']=MAP_TYPES['births'][1]
            breports_dict.append(br)
            
        except:
            continue
        ##get percentage heat values
    for t in breports_dict:
        t['heat']=t['heat']/float(maxvalue)
    return JsonResponse(breports_dict)
def malnutrition(request,start_date=None,end_date=None):
    try:
        start_date=request.GET.get('start', None)
        end_date=request.GET.get('end',None)
        
    
    except:
        start_date,end_date=None,None
        
        
    #Month=month_options[month][1]
    
    mauc_reports=[]
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
    for facility in facilities:
        
        try:
            mc=mauc.filter(reporter__healthreporter__facility=facility)
            mr={}
            mr['title']="Facility:"+str(mc[0].reporter.healthreporter.facility.name)
            mr['lat']=str(mc[0].reporter.healthreporter.facility.latitude)
            mr['lon']=str(mc[0].reporter.healthreporter.facility.longitude)
            mauc_count=mc.count()
            if mauc_count>maxvalue:
                maxvalue=mauc_count
            mr['heat']=mauc_count
            mr['desc']="Number Of Cases:"+str(mauc_count)
            mr['icon']="/Media/img/"+MAP_TYPES['malnutrition'][0]
            mr['color']=MAP_TYPES['malnutrition'][1]
            mauc_reports.append(mr)
        except:
            continue
    for t in mauc_reports:
        t['heat']=t['heat']/float(maxvalue)
    
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
   
    
    epi_obs=[]
    if str(start_date)=="undefined" or str(end_date)=="undefined":
        start_date,end_date=None,None
    if start_date==None or end_date==None:
        
        main_query=EpiReport.objects.filter(valid=True,disease=KIND).order_by('message__time')
        
    else:
        start_date=format_date(str(start_date)) 
        end_date=format_date(str(end_date),start=False)   
        main_query=EpiReport.objects.filter(valid=True,disease=KIND).filter(message__time__range=(start_date,end_date)).order_by('message__time')
    facilities=Facility.objects.all()
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
                epi['title']= str(er[0].reporter.healthreporter.facility.name)
                
                epi['lat']=str(er[0].reporter.healthreporter.facility.latitude)
                epi['lon']=str(er[0].reporter.healthreporter.facility.longitude)
                epi['heat']=normalized_value
                epi['desc']="<p>total number of cases: %s</p><p>number of reports: %s</p>"%(sum,count)
                if kind in MAP_TYPES.keys():
                    epi['icon']="/Media/img/"+MAP_TYPES[kind][0]
                    epi['color']=MAP_TYPES[kind][1]
                else:
                    epi['icon']="/marker/25/orange/%s/marker.png"%kind
                epi_obs.append(epi)
                
            
        except:
            continue
    for t in epi_obs:
        t['heat']=t['heat']/float(maxvalue)
    return JsonResponse(epi_obs)
    
def map(request):
    map_key=MAP_KEY
    Map_urls=mark_safe(simplejson.dumps(MAP_URLS))
    map_types=mark_safe(simplejson.dumps(MAP_TYPES))
    minLon,maxLon,minLat,maxLat=mark_safe(min_lat),mark_safe(max_lat),mark_safe(min_lon),mark_safe(max_lon)
    slider_ranges=date_range(start_date,end_date)
    return render_to_response("map.html",locals(),context_instance=RequestContext(request))




