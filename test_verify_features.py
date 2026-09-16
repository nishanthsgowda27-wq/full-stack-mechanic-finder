#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()
mech = User.objects.filter(username='mech1').first()
if not mech:
    print('mech1 not found; please run create_demo_data')
    raise SystemExit(1)

client.force_login(mech)
# Fetch bookings page
resp = client.get('/bookings/', HTTP_HOST='127.0.0.1:8000')
print('GET /bookings/ status:', resp.status_code)
content = resp.content.decode('utf-8')
has_accept = 'Accept' in content and '/booking/' in content and 'reject' in content.lower() or 'Reject' in content
print('Accept/Reject present in bookings page?', has_accept)

# Fetch search page
resp2 = client.get('/search/', HTTP_HOST='127.0.0.1:8000')
print('GET /search/ status:', resp2.status_code)
search_html = resp2.content.decode('utf-8')
has_search_inputs = 'name="q"' in search_html and 'name="city"' in search_html
print('Search inputs present?', has_search_inputs)

# Check register mechanic path exists (GET)
resp3 = client.get('/register/mechanic/', HTTP_HOST='127.0.0.1:8000')
print('GET /register/mechanic/ status:', resp3.status_code)
print('Done')
