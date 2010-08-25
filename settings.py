 ##minimum date and maximum  date for the slider
##in the form '%Y-%m-%d'
start_date="2010-05-01"
end_date="2010-12-31"
####



MAP_URLS=(('Health Facilities','/health_facilities'),
          ('Deaths','/deaths'),
          ('Births','/births'),
          ('Malnutrition','/malnutrition'),
          ('Malaria','/epi/ma'),
          ('Dysentry','/epi/bd'),
          ('Tuberclosis','/epi/tb'),
          ('Other Diseases','/epi/other'),
#          ('Measles','/epi/me'),
#          
#          ('Animal Bites','/epi/ab'),
#          ('Polio','/epi/af'),
#          ('Yellow Fever','/epi/yf'),
#          ('Cholera','/epi/ch'),
#          
#          ('Guinea Worm','/epi/gw'),
#          ('Meningitis','/epi/mg'),
#          ('Neonatal Tetanus','/epi/nt'),
#          ('Plague','/epi/pl'),
#          ('Rabies','/epi/rb'),
            
          )
##map types
MAP_TYPES={
           'health_facilities':['army.png','#14740a'],
           'deaths':['black.png','#121703'],
           'births':['white.png','#ff99ff'],
           'malnutrition':['yellow.png','#dfea28'],
           'ma':['green.png','#2dea28'],
           'bd':['br.png','#ff0000'],
           'tb':['orange.png','#b75600'],
           'other': ['orange.png','#df7890']} 
                     
                      
                      
                      
                      
#                      { 'me':['pinky.png','#c160b7'],
#                               'ab':['white.png','#ffffff'],
#                               'af':['green.png','#2dea28'],
#                               'yf':['blue.png','#28442e'],
#                               'ch':['red.png','#8b252a'],
#                               'gw':['rl.png','#8a737d'],
#                               'mg':['navy.png','#00052f'],
#                               'nt':['lime.png','#e8e0d9'],
#                               'pl':['dbrown.png','#663300'],
#                               'rb':['brown.png','#cc9933'],
#                               'ma':['cy.png','#9999ff']
#                       }]
#           
#           
#           
#           
#            }
##base urls
# url minzoom maxzoom
BASE_LAYERS=(('/healthfacilities/?label=true',8),)
#from djangosms.stats.models import ObservationKind
#observation_kinds=ObservationKind.objects.filter(slug__startswith="epidemiological_observation").distinct().values('slug','name')
#for kind in observation_kinds:
#    MAP_URLS[(kind['name'].rsplit(" ")[-1])]="/epi/%s" %(kind['slug'].rsplit("_")[-1])

#map bounding box
min_lat="31.19800"
max_lat="33.80176"
min_lon="2.1444"
max_lon="3.88875"

##localhost:8080 key. you will probably need to get one for your host
MAP_KEY="ABQIAAAAYimH_excdTjwGjM6LcP-DhTX43PO8-sEH-jeG6rM560fvsomnhQ4fvBin-y4dRWztAXXs1ap0AwfdQ"