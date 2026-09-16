#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client

client = Client()
print('GET /search/ (no params)')
resp = client.get('/search/', HTTP_HOST='127.0.0.1:8000')
print('Status', resp.status_code)
print('Length', len(resp.content))

print('\nGET /search/?q=mech3')
resp2 = client.get('/search/', {'q':'mech3'}, HTTP_HOST='127.0.0.1:8000')
print('Status', resp2.status_code)
print('Content length', len(resp2.content))
# save responses
open('search_out.html','wb').write(resp.content)
open('search_out_q.html','wb').write(resp2.content)
print('Saved search_out.html and search_out_q.html')

# Quick model check
from service.models import UserProfile
print('\nMechanics count in DB:', UserProfile.objects.filter(is_mechanic=True).count())
print('Mechanics with q=mech3:', list(UserProfile.objects.filter(is_mechanic=True, user__username__icontains='mech3').values_list('user__username', flat=True)))
