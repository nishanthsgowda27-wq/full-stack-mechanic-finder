#!/usr/bin/env python
import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.filter(username='user1').first()
if not user:
    print('No user1 found; aborting')
else:
    client.force_login(user)
    print('Logged in as:', user.username)
    from service.models import MechanicService
    svc = MechanicService.objects.first()
    if not svc:
        print('No service found')
    else:
        url = f'/book/{svc.pk}/'
        print('Requesting', url)
        try:
            resp = client.get(url, HTTP_HOST='127.0.0.1:8000')
            print('Status code:', resp.status_code)
            with open('client_response2.html', 'wb') as f:
                f.write(resp.content)
            print('Saved response to client_response2.html')
        except Exception as e:
            print('Exception during client request:', e)
            traceback.print_exc()
