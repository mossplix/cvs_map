from decimal import Decimal

from django.shortcuts import  render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils import simplejson

from mapping.lib.utils import *
from mapping.lib.marker import *
from mapping.settings import start_date, end_date, MAP_URLS, min_lat, max_lat,\
 min_lon, max_lon, MAP_TYPES, MAP_KEY,BASE_LAYER
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


def health_facilities(request):
    
    """
      get json dump of health facilities .<name>,<lat>,<lon>,<level>
    """
    from cvs.models import Facility, HealthReporter
    try:
        zoom = int(request.GET.get('zoom', 8))
        type = int(request.GET.get('type', 0))
        minlat = request.GET.get('minLat', None)
        maxlat = request.GET.get('maxLat', None)
        minlon = request.GET.get('minLon', None)
        maxlon = request.GET.get('maxLon', None)
       
    
    except:
        zoom = 8
        type = 0
    
    facility_list = []
    if minlat is not None:
        facilities = Facility.objects.filter(latitude__gte=Decimal(str(minlat)),
                                            latitude__lte=Decimal(str(maxlat)),
                                            longitude__gte=Decimal(str(minlon)),
                                            longitude__lte=Decimal(str(maxlon))).order_by('name')
        
        facilities_with_reporters = [hc.facility for hc in HealthReporter.\
                                     objects.filter(facility__latitude__gte=Decimal(str(minlat)),
                                                    facility__latitude__lte=Decimal(str(maxlat)),
                                                    facility__longitude__gte=Decimal(str(minlon)),
                                                    facility__longitude__lte=Decimal(str(maxlon))).all()]
    else:
        facilities = Facility.objects.all()
        facilities_with_reporters = [hc.facility for hc in HealthReporter.objects.all()]

    for facility in facilities:
        
        fac = {}
        fac['title'] = facility.name
        fac['lat'] = str(facility.latitude)
        fac['lon'] = str(facility.longitude)
        fac['desc'] = facility.kind.name
        fac['icon'] = "/Media/img/" + facility.kind.name + ".png"
        if facility in facilities_with_reporters:
            fac['icon'] = "/Media/img/R" + facility.kind.name + ".png"
        if zoom > 10 and type == 1:
            fac['icon'] = "http://chart.apis.google.com/chart?chst=d_text_outline&chld=000000|12|l|ffffff|_|%s|" % (facility.name)      
        fac['color'] = MAP_TYPES['health_facilities'][1]
        facility_list.append(fac)
    return JsonResponse(facility_list)

    
month_opts = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sept":9, "oct":10, "Nov":11, "Dec":12} 

      
def format_date(date, start=True):
    
    """ format the date into a python datetime object"""
    import datetime
    month, year = date.split("-")
    month = month_opts[month]
    return datetime.datetime.strptime(year + "-" + str(month) + "-01", '%Y-%m-%d')
    if start == False:
        month = (int(month) + 1) % 12
        if month == 0:
            month = 1
            year = year + 1
        return datetime.datetime.strptime(year + "-" + str(month) + "-01", '%Y-%m-%d')
    
          
def deaths(request):
    
    """
    export death reports as json with lat and lon
    """
    
    try:
        start_date = request.GET.get('start', None)
        end_date = request.GET.get('end', None)
        minlat = request.GET.get('minLat', None)
        maxlat = request.GET.get('maxLat', None)
        minlon = request.GET.get('minLon', None)
        maxlon = request.GET.get('maxLon', None)
        
    
    except:
        start_date, end_date = None, None
        
        
    #Month=month_options[month][1]
    
    death_reports = []
    if str(start_date) == "undefined" or str(end_date) == "undefined":
        start_date, end_date = None, None
    if start_date == None or end_date == None:

        deathreport = DeathReport.objects.order_by('message__time').filter(valid=True)
    else:
        start_date = format_date(str(start_date)) 
        end_date = format_date(str(end_date), start=False)   
        deathreport = DeathReport.objects.filter(valid=True).order_by('message__time').\
        filter(message__time__range=(start_date, end_date))
    
        
    try:
        facilities = Facility.objects.filter(latitude__gte=Decimal(str(minlat)),
                                                latitude__lte=Decimal(str(maxlat)),
                                                longitude__gte=Decimal(str(minlon)),
                                                longitude__lte=Decimal(str(maxlon))).order_by('name')
    except:
         facilities = Facility.objects.all()
    
    maxvalue = 0
    for facility in facilities:
     
        try:
            dr = deathreport.filter(reporter__healthreporter__facility=facility)
            if len(dr) != 0:
                death = {}
#                import pdb
#                pdb.set_trace()
                death['title'] = "Facility:" + str(dr[0].reporter.healthreporter.facility.name)
                death['lat'] = str(dr[0].reporter.healthreporter.facility.latitude)
                death['lon'] = str(dr[0].reporter.healthreporter.facility.longitude)
                total_deaths = dr.count()
                if total_deaths > maxvalue:
                    maxvalue = total_deaths
                death['heat'] = total_deaths
                death['desc'] = "<p><b>Deaths</b></p>total_deaths: " + str(total_deaths)
                death['icon'] = "/Media/img/" + MAP_TYPES['deaths'][0]
                death['color'] = MAP_TYPES['deaths'][1]
                death_reports.append(death)
               
                
           
            
        except:
            continue
        ##get percentage heat values
    for t in death_reports:
        t['heat'] = t['heat'] / float(maxvalue)
    return JsonResponse(death_reports)


def births(request):
    
    """
    export birth reports as json
    """
    
    try:
        start_date = request.GET.get('start', None)
        end_date = request.GET.get('end', None)
        minlat = request.GET.get('minLat', None)
        maxlat = request.GET.get('maxLat', None)
        minlon = request.GET.get('minLon', None)
        maxlon = request.GET.get('maxLon', None)
        
    
    except:
        start_date, end_date = None, None
        
        
    breports_dict = []
    if str(start_date) == "undefined" or str(end_date) == "undefined":
        start_date, end_date = None, None
    if start_date == None or end_date == None:
        birth_reports = NewBirthReport.objects.filter(valid=True).order_by('message__time')
    else:
        start_date = format_date(str(start_date)) 
        end_date = format_date(str(end_date), start=False)   
        birth_reports = NewBirthReport.objects.filter(valid=True).filter(\
                                                message__time__range=(start_date, end_date)).order_by('message__time')
        
    try:
        facilities = Facility.objects.filter(latitude__gte=Decimal(str(minlat)),
                                                latitude__lte=Decimal(str(maxlat)),
                                                longitude__gte=Decimal(str(minlon)),
                                                longitude__lte=Decimal(str(maxlon))).order_by('name')
    except:
        facilities = Facility.objects.all()
    maxvalue = 0
    
    
    for facility in facilities:
        try:
            btrt = birth_reports.filter(reporter__healthreporter__facility=facility)
            br = {}
            br['lat'] = str(btrt[0].reporter.healthreporter.facility.latitude)
            br['lon'] = str(btrt[0].reporter.healthreporter.facility.longitude)   
            br['title'] = "Facility: " + str(btrt[0].reporter.healthreporter.facility.name)    
            birth_count = btrt.count()
            if birth_count > maxvalue:
                maxvalue = birth_count
            br['heat'] = birth_count
            br['desc'] = "<p><b>Births</b></p>Birth Reports: " + str(birth_count)
            br['icon'] = "/Media/img/" + MAP_TYPES['births'][0]
            br['color'] = MAP_TYPES['births'][1]
            breports_dict.append(br)
            
        except:
            continue
        ##get percentage heat values
    for t in breports_dict:
        t['heat'] = t['heat'] / float(maxvalue)
    return JsonResponse(breports_dict)


def malnutrition(request, start_date=None, end_date=None):
    
    """
    export muac reports as json
    """
    
    try:
        start_date = request.GET.get('start', None)
        end_date = request.GET.get('end', None)
        minlat = request.GET.get('minLat', None)
        maxlat = request.GET.get('maxLat', None)
        minlon = request.GET.get('minLon', None)
        maxlon = request.GET.get('maxLon', None)
        
    
    except:
        start_date, end_date = None, None
        
        
    #Month=month_options[month][1]
    
    mauc_reports = []
    if str(start_date) == "undefined" or str(end_date) == "undefined":
        start_date, end_date = None, None
    if start_date == None or end_date == None:
        mauc = MuacReport.objects.filter(valid=True).order_by('message__time')
        
    else:
        start_date = format_date(str(start_date)) 
        end_date = format_date(str(end_date), start=False)   
        mauc = MuacReport.objects.filter(valid=True).filter(message__time__range=(
                                                                                  start_date,
                                                                                   end_date)).\
                                                                                   order_by('message__time')
    try:
        facilities = Facility.objects.filter(latitude__gte=Decimal(str(minlat)),
                                                latitude__lte=Decimal(str(maxlat)),
                                                longitude__gte=Decimal(str(minlon)),
                                                longitude__lte=Decimal(str(maxlon))).order_by('name')
    except:
        facilities = Facility.objects.all()
    maxvalue = 0
    for facility in facilities:
        
        try:
            mc = mauc.filter(reporter__healthreporter__facility=facility)
            mr = {}
            mr['title'] = "Facility:" + str(mc[0].reporter.healthreporter.facility.name)
            mr['lat'] = str(mc[0].reporter.healthreporter.facility.latitude)
            mr['lon'] = str(mc[0].reporter.healthreporter.facility.longitude)
            mauc_count = mc.count()
            if mauc_count > maxvalue:
                maxvalue = mauc_count
            mr['heat'] = mauc_count
            mr['desc'] = "<p><b>Malnutrition</b></p>Number Of Cases:" + str(mauc_count)
            mr['icon'] = "/Media/img/" + MAP_TYPES['malnutrition'][0]
            mr['color'] = MAP_TYPES['malnutrition'][1]
            mauc_reports.append(mr)
        except:
            continue
    for t in mauc_reports:
        t['heat'] = t['heat'] / float(maxvalue)
    
    return JsonResponse(mauc_reports)
        

def epi_kind(request, kind, start=None, end=None):
    
    """
      export epi reports .kind is the epi kind eg <ma> for malaria
    """
    
    from django.db.models import Sum, Count
    from cvs.models import DISEASE_CHOICES
    dc = dict(DISEASE_CHOICES)
    KIND = str(kind)
    try:
        start_date = request.GET.get('start', None)
        end_date = request.GET.get('end', None)
        minlat = request.GET.get('minLat', None)
        maxlat = request.GET.get('maxLat', None)
        minlon = request.GET.get('minLon', None)
        maxlon = request.GET.get('maxLon', None)

    except:
        start_date, end_date = None, None 
    #Month=month_options[month][1]
    epi_obs = []
    other = ['me', 'ab', 'af', 'yf', 'ch', 'gw', 'mg', 'nt', 'pl', 'rb']
    if str(start_date) == "undefined" or str(end_date) == "undefined":
        start_date, end_date = None, None
    if start_date == None or end_date == None:
        if KIND == "other":
            main_query = EpiReport.objects.filter(valid=True, disease__in=other).order_by('message__time')
        else:
            main_query = EpiReport.objects.filter(valid=True, disease=KIND).order_by('message__time')
              
    else:
        start_date = format_date(str(start_date)) 
        end_date = format_date(str(end_date), start=False)
        if KIND == "other":   
            main_query = EpiReport.objects.filter(valid=True, disease__in=other).\
            filter(message__time__range=(start_date, end_date)).order_by('message__time')
        else:
            main_query = EpiReport.objects.filter(valid=True, disease=KIND).\
            filter(message__time__range=(start_date, end_date)).order_by('message__time')
            
    try:
        facilities = Facility.objects.filter(latitude__gte=Decimal(str(minlat)),
                                                latitude__lte=Decimal(str(maxlat)),
                                                longitude__gte=Decimal(str(minlon)),
                                                longitude__lte=Decimal(str(maxlon))).order_by('name')
    except:
        facilities = Facility.objects.all()
    maxvalue = 0
    for facility  in facilities:
        try:
            er = main_query.filter(reporter__healthreporter__facility=facility)
           
            if len(er) != 0:
                epi = {}
                result = er.aggregate(Sum('value'), Count('value'))
                sum, count = int(result.get('value__sum')), int(result.get('value__count'))
                normalized_value = sum / count
                if normalized_value > maxvalue:
                    maxvalue = normalized_value
                epi['title'] = str(er[0].reporter.healthreporter.facility.name)
                epi['lat'] = str(er[0].reporter.healthreporter.facility.latitude)
                epi['lon'] = str(er[0].reporter.healthreporter.facility.longitude)
                epi['heat'] = normalized_value
                epi['color'] = MAP_TYPES[kind][1]
                if kind in MAP_TYPES.keys():
                    epi['icon'] = "/Media/img/" + MAP_TYPES[kind][0]
                    
                else:
                    epi['icon'] = "/marker/25/orange/%s/marker.png" % kind

                if KIND == "other":
                    desc = []
                    for k in other:
                        result = er.filter(disease=k).aggregate(Sum('value'), Count('value'))
                        try:
                            sum, count = int(result.get('value__sum')), int(result.get('value__count'))
                        except:
                            sum, count = 0, 0
                        if count > 0:
                            d = "<p><b>%s</b></p><p>total number of cases:%s</p><p>number of reports: %s</p>" % (dc[k], sum, count)
                            desc.append(d)
                   
                    desc_s = " ".join(desc)
                    epi['desc'] = desc_s
                    
        
                else:
                    epi['desc'] = "<p><b>%s</b></p><p>total number of cases:%s</p><p>number of reports: %s</p>" % (dc[kind], sum, count)
                    
                
                epi_obs.append(epi)
                
            
        except:
            continue
    try:
        for t in epi_obs:
            t['heat'] = t['heat'] / float(maxvalue)
    except:
        pass
    return JsonResponse(epi_obs)

    
def map(request):
    
    """
    main view to display map
    """
    map_key = MAP_KEY
    Map_urls = mark_safe(simplejson.dumps(MAP_URLS))
    map_types = mark_safe(simplejson.dumps(MAP_TYPES))
    minLon, maxLon, minLat, maxLat = mark_safe(min_lat), mark_safe(max_lat), \
    mark_safe(min_lon), mark_safe(max_lon)
    slider_ranges = date_range(start_date, end_date)
    base_layer=BASE_LAYER
    return render_to_response("map.html", locals(), context_instance=RequestContext(request))


def timeMap(request):
    
    """
    a time map is a time slider that dynamically gets messages and maps them depending on their source
    """
    map_key = MAP_KEY
    minLon, maxLon, minLat, maxLat = mark_safe(min_lat), mark_safe(max_lat), mark_safe(min_lon), mark_safe(max_lon)
    return render_to_response("messages_time_map.html", locals(), context_instance=RequestContext(request))


def getMessages(request):
    
    """
      get all messages for time map...
      filtered on the visible date range
    """
    
    from djangosms.core.models import Incoming
    import datetime
    today = datetime.datetime.now()
    back = today - datetime.timedelta(days=40)
    min_date = request.GET.get('min', back)
    max_date = request.GET.get('max', today)
    
    messages = Incoming.objects.filter(time__lte=max_date, \
        time__gte=min_date)
    message_dict = {}
    message_dict['dateTimeFormat'] = 'iso8601'
    events = []
    for message in messages:
        try:
            reporter = Reporter.objects.get(connections__uri=message.uri)
        except Reporter.DoesNotExist:
            reporter = None

        if reporter is not None and reporter.name != u"" :
            try:
                msg = {}
                msg['start'] = str(message.time)
                msg['lat'] = str(reporter.healthreporter.facility.latitude)
                msg['lng'] = str(reporter.healthreporter.facility.longitude)
                msg['title'] = reporter.name
                msg['description'] = message.text
                msg['link'] = ""
        #        msg['icon']=""
        #        msg['image']=""
                msg['color'] = "#8b252a"
                msg['textcolor'] = "#8b252a"
                events.append(msg)
            except:
                continue
           
    message_dict['events'] = events
    
    return JsonResponse(message_dict)
        
        
        
        

