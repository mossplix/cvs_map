
import datetime
#from django.conf import settings
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson

month_options=((),(1,"Jan"),(2,"Feb"),(3,"Mar"),(4,"Apr"),(5,"May"),(6,"Jun"),(7,"Jul"),(8,"Aug"),(9,"Nov"),(10,"oct"),(11,"Nov"),(12,"Dec"))
# FIXME MappableObjectMeta and MappableObject not referenced anywhere,
# remove them!
class MappableObjectMeta(type):
    """meta class of the mappable object"""
    def __init__(cls,name,bases,attrs):
        pass
class MappableObject(object):
    """  takes an object and returns a json list of objects """
    __metaclass__=MappableObjectMeta
    def __init__(self,obj):
        pass
    
    class XmlResponse(HttpResponse):
        """ return xml content type   """
        def __init__(self, obj):
            self.original_obj = obj
            HttpResponse.__init__(self, self.serialize())
            self["Content-Type"] = "application/xml"
    
        def serialize(self):
            return(simplejson.dumps(self.original_obj))
    
   
# FIXME documentation
def date_range(startt,endd):
    month_options=((),(1,"Jan"),(2,"Feb"),(3,"Mar"),(4,"Apr"),(5,"May"),(6,"Jun"),(7,"Jul"),(8,"Aug"),(9,"Nov"),(10,"oct"),(11,"Nov"),(12,"Dec"))
    end_f=datetime.datetime.strptime(endd,'%Y-%m-%d').date()
    start_f=datetime.datetime.strptime(startt,'%Y-%m-%d').date()
    
    
    years=range(start_f.year,end_f.year+1)
    
    
    start_opts="""<fieldset >
            <label for='%s'>%s</label>
            <select name='%s' id='%s' style='display:none;'>"""
    for year in years:
        
        opt_year="<optgroup label='%s'>"%str(year)
        
        start_opts=start_opts+opt_year
        for month in range(1,13):
            option="<option value='%s/%s'>%s-%s</option>"%(str(month),str(year)[-2:],month_options[month][1],str(year))
            start_opts=start_opts+option
        start_opts=start_opts+"</optgroup>"
    start_opts=start_opts+"</select>"
        
    start_html=start_opts%("start","","start","start")
    end_html=start_opts%("end","","end","end")
    return mark_safe(start_html+end_html)

if __name__=="__main__":
    print date_range("2010-06-12","2013-05-13")