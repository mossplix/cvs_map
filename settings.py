#!/usr/bin/python
# -*- coding: utf-8 -*-

start_date = '2010-05-01'
end_date = '2010-12-31'

##set the overlay data urls
MAP_URLS = (
    ('Health Facilities', '/health_facilities'),
    ('Deaths', '/deaths'),
    ('Births', '/births'),
    ('Malnutrition', '/malnutrition'),
    ('Malaria', '/epi/ma'),
    ('Dysentry', '/epi/bd'),
    ('Tuberclosis', '/epi/tb'),
    ('Other Diseases', '/epi/other'),
    )

## set the overlay colors and icons 
MAP_TYPES = {
    'health_facilities': ['army.png', '#14740a'],
    'deaths': ['black.png', '#121703'],
    'births': ['white.png', '#ff99ff'],
    'malnutrition': ['yellow.png', '#dfea28'],
    'ma': ['green.png', '#2dea28'],
    'bd': ['br.png', '#ff0000'],
    'tb': ['orange.png', '#b75600'],
    'other': ['orange.png', '#df7890'],
    }

#base layer of the map
BASE_LAYER = \
    '/health_facilities?start=undefined&end=undefined&maxLat=3.88875&maxLon=33.80176&minLat=2.1444&minLon=31.198&zoom=8'

#map bounding box
min_lat = '31.19800'
max_lat = '33.80176'
min_lon = '2.1444'
max_lon = '3.88875'

##google maps api key
MAP_KEY = \
    'ABQIAAAAYimH_excdTjwGjM6LcP-DhTX43PO8-sEH-jeG6rM560fvsomnhQ4fvBin-y4dRWztAXXs1ap0AwfdQ'

