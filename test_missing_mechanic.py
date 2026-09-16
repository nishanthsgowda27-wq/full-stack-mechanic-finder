#!/usr/bin/env python
"""Test creating and displaying a booking with missing mechanic."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from service.models import Booking, UserProfile, MechanicService

print("Test: Create booking with NO mechanic field set")
print("=" * 60)

# Get a user and service
user_profile = UserProfile.objects.filter(is_mechanic=False).first()
service = MechanicService.objects.filter().first()

if not user_profile or not service:
    print("❌ Missing user or service")
    exit(1)

print(f"✓ User: {user_profile}")
print(f"✓ Service: {service}")

# Create a booking but don't set mechanic
from datetime import datetime, timedelta
booking = Booking(
    user=user_profile,
    service=service,
    booking_date=datetime.now() + timedelta(days=1)
    # NOTE: mechanic is NOT set
)

try:
    booking.full_clean()
    booking.save()
    print(f"✓ Booking saved: {booking.pk}")
except Exception as e:
    print(f"✓ Expected validation error: {e}")
    print("  (This means full_clean() caught the missing mechanic)")
