##minimum date and maximum  date for the slider
##in the form '%Y-%m-%d'
start_date="2009-06-01"
end_date="2010-08-01"
####
##a tuple of layers and their particular handlers
#from mapping.views.main import health_facilities
#layers=(("HealthCenters"))

MAP_URLS={'health facilities':'/health_facilities/',
          'epidemological diseases':'/epi'}

#map bounding box
min_lat="31.19800"
max_lat="33.80176"
min_lon="2.1444"
max_lon="3.88875"