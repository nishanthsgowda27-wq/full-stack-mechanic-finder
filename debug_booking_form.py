#!/usr/bin/env python
"""Debug booking form rendering issue."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from service.models import MechanicService, Booking
from service.forms import BookingForm
from datetime import datetime, timedelta

print("Debugging Booking Form Rendering")
print("=" * 60)

# Get a service
service = MechanicService.objects.filter().first()
if not service:
    print("❌ No service found")
    exit(1)

print(f"✓ Found service: {service}")
print(f"✓ Service mechanic: {service.mechanic}")

# Try to create a form
print("\nCreating BookingForm with mechanic...")
try:
    future_date = datetime.now() + timedelta(days=1)
    form = BookingForm(
        mechanic=service.mechanic,
        initial={'service': service}
    )
    print("✓ Form created successfully")
    
    # Try to render the form
    print("\nTrying to render form fields...")
    for field_name, field in form.fields.items():
        print(f"  - {field_name}: {field}")
    
    # Try form.as_p()
    print("\nTrying form.as_p()...")
    html = form.as_p()
    print("✓ form.as_p() rendered successfully")
    print(f"  HTML length: {len(html)} characters")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
