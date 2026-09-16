#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from service.models import Booking, MechanicService

client = Client()
user = User.objects.filter(username='user1').first()
if not user:
    print('No user1 found; aborting')
else:
    client.force_login(user)
    svc = MechanicService.objects.first()
    url = f'/book/{svc.pk}/'
    # prepare booking_date (localtime naive) - use UTC offset depending on TIME_ZONE; tests use naive
    dt = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
    # datetime-local expects 'YYYY-MM-DDTHH:MM'
    dt_str = dt.isoformat(timespec='minutes')
    data = {
        'service': str(svc.pk),
        'booking_date': dt_str,
    }
    print('Posting to', url, 'data=', data)
    resp = client.post(url, data, HTTP_HOST='127.0.0.1:8000')
    print('Status', resp.status_code)
    # Check if booking created
    b = Booking.objects.filter(user__user__username='user1').order_by('-created_at').first()
    if b:
        print('Booking created:', b.pk, 'mechanic_id=', b.mechanic_id, 'service_id=', b.service_id, 'date=', b.booking_date)
    else:
        print('No booking created')
