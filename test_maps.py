#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()

# Test mechanic list with map
resp = client.get('/search/', HTTP_HOST='127.0.0.1:8000')
print('GET /search/ status:', resp.status_code)
html = resp.content.decode('utf-8')
has_leaflet = 'leaflet' in html.lower() or 'L.map' in html
has_openstreetmap = 'openstreetmap' in html.lower()
print('Leaflet present?', has_leaflet)
print('OpenStreetMap present?', has_openstreetmap)

# Check mechanic detail page
mech_user = User.objects.filter(username='mech1').first()
if mech_user:
    mech_profile = mech_user.userprofile
    resp2 = client.get(f'/mechanic/{mech_profile.id}/', HTTP_HOST='127.0.0.1:8000')
    print('GET /mechanic/{mech_id}/ status:', resp2.status_code)
    detail_html = resp2.content.decode('utf-8')
    has_detail_map = 'detail-map' in detail_html and 'L.map' in detail_html
    print('Detail page has map?', has_detail_map)
else:
    print('mech1 not found')

print('Done')
