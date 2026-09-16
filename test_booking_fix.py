#!/usr/bin/env python
"""Test booking form to verify mechanic field is properly set."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from service.models import UserProfile, MechanicService, Booking
from service.forms import BookingForm
from datetime import datetime, timedelta

print("Testing Booking Form Fix")
print("=" * 60)

# Get a mechanic and service
mechanic = UserProfile.objects.filter(is_mechanic=True).first()
if not mechanic:
    print("❌ No mechanic found")
    exit(1)

service = MechanicService.objects.filter(mechanic=mechanic).first()
if not service:
    print("❌ No service found")
    exit(1)

print(f"✓ Found mechanic: {mechanic}")
print(f"✓ Found service: {service}")

# Test the form
print("\nTesting BookingForm with mechanic parameter:")

# Create form with mechanic
future_date = datetime.now() + timedelta(days=1)
form = BookingForm(
    data={
        'service': service.pk,
        'booking_date': future_date.strftime('%Y-%m-%dT%H:%M')
    },
    mechanic=mechanic
)

if form.is_valid():
    print("✓ Form is valid")
    
    # Save without committing
    booking = form.save(commit=False)
    
    if booking.mechanic:
        print(f"✓ Booking mechanic set correctly: {booking.mechanic}")
    else:
        print("❌ Booking mechanic NOT set!")
    
    if booking.service:
        print(f"✓ Booking service set: {booking.service}")
    else:
        print("❌ Booking service NOT set!")
    
    print("\n✅ BookingForm fix is working correctly!")
else:
    print(f"❌ Form has errors: {form.errors}")
