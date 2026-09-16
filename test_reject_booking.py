#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from service.models import UserProfile, MechanicService, Booking

mech_user = User.objects.filter(username='mech1').first()
user1 = User.objects.filter(username='user1').first()
if not mech_user or not user1:
    print('mech1 or user1 not found; run create_demo_data first')
    raise SystemExit(1)

mech_profile = UserProfile.objects.get(user=mech_user)
user_profile = UserProfile.objects.get(user=user1)
service = MechanicService.objects.filter(mechanic=mech_profile).first()
if not service:
    print('No service for mech1')
    raise SystemExit(1)

# Create a pending booking
dt = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
booking = Booking.objects.create(user=user_profile, mechanic=mech_profile, service=service, booking_date=dt)
print('Created booking:', booking.pk, 'status=', booking.status)

# Use test client to POST reject as mechanic
client = Client()
client.force_login(mech_user)
resp = client.post(f'/booking/{booking.pk}/reject/', {}, HTTP_HOST='127.0.0.1:8000')
print('POST response status:', resp.status_code)

# Refresh booking
booking.refresh_from_db()
print('After reject: status=', booking.status)

# Cleanup - delete booking
booking.delete()
print('Deleted booking')
