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
    logged_in = client.force_login(user)  # returns None
    print('Logged in as:', user.username)
    from service.models import MechanicService
    svc = MechanicService.objects.first()
    if not svc:
        print('No service found')
    else:
        url = f'/book/{svc.pk}/'
        print('Requesting', url)
        try:
            resp = client.get(url)
            print('Status code:', resp.status_code)
            print('Response content length:', len(resp.content))
            # write content to temp file
            with open('client_response.html', 'wb') as f:
                f.write(resp.content)
            print('Saved response to client_response.html')
        except Exception as e:
            print('Exception during client request:', e)
            traceback.print_exc()
