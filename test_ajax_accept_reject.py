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
    print('mech1 or user1 not found; please run create_demo_data')
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

client = Client()
client.force_login(mech_user)
# Accept via AJAX endpoint
resp = client.post(f'/booking/{booking.pk}/accept/json/', {}, HTTP_HOST='127.0.0.1:8000')
print('Accept JSON status:', resp.status_code, 'content:', resp.content)
booking.refresh_from_db()
print('After accept:', booking.status)

# Create another booking to test reject
booking2 = Booking.objects.create(user=user_profile, mechanic=mech_profile, service=service, booking_date=(dt+timedelta(hours=1)))
print('Created booking2:', booking2.pk, 'status=', booking2.status)
resp2 = client.post(f'/booking/{booking2.pk}/reject/json/', {}, HTTP_HOST='127.0.0.1:8000')
print('Reject JSON status:', resp2.status_code, 'content:', resp2.content)
booking2.refresh_from_db()
print('After reject:', booking2.status)

# Cleanup
booking.delete()
booking2.delete()
print('Cleaned up')
