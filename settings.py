 ##minimum date and maximum  date for the slider
##in the form '%Y-%m-%d'
start_date="2010-05-01"
end_date="2011-01-01"
####



MAP_URLS=(('Health Facilities','/health_facilities'),
          ('Deaths','/deaths'),
          ('Births','/births'),
          ('Malnutrition','/malnutrition'),
          ('Malaria','/epi/ma'),
          ('Measles','/epi/me'),
          ('Dysentry','/epi/bd'),
          ('Animal Bites','/epi/ab'),
          ('Polio','/epi/af'),
          ('Yellow Fever','/epi/yf'),
          ('Cholera','/epi/ch'),
          ('Tuberclosis','/epi/tb'),
          ('Guinea Worm','/epi/gw'),
          ('Meningitis','/epi/mg'),
          ('Neonatal Tetanus','/epi/nt'),
          ('Plague','/epi/pl'),
          ('Rabies','/epi/rb'),
            
          )
##map types
MAP_TYPES={
           'health_facilities':['army.png','#14740a'],
           'deaths':['black.png','#121703'],
           'births':['white.png','#ffffff'],
           'malnutrition':['yellow.png','#dfea28'],
           'ma':['green.png','#2dea28'],
           'me':['pinky.png','#c160b7'],
           'bd':['br.png','#ff0000'],
           'ab':['white.png','#ffffff'],
           'af':['green.png','#2dea28'],
           'yf':['blue.png','#28442e'],
           'ch':['red.png','#8b252a'],
           'tb':['orange.png','#b75600'],
           'gw':['rl.png','#8a737d'],
           'mg':['navy.png','#00052f'],
           'nt':['lime.png','#e8e0d9'],
           'pl':['dbrown.png','#663300'],
           'rb':['brown.png','#cc9933'],
           'ma':['cy.png','#9999ff'],
           
           
           
            }
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
MAP_KEY="ABQIAAAAYimH_excdTjwGjM6LcP-DhTwM0brOpm-All5BF6PoaKBxRWWERT9OyCpc3hGVZ8kB3Z6S8RK5WKM1g"