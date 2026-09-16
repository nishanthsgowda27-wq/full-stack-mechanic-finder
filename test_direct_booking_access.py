#!/usr/bin/env python
import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from service.views import book_service
from service.models import MechanicService

# Get the first service
try:
    service = MechanicService.objects.first()
    print(f"Service: {service}")
    print(f"Service ID: {service.pk}")
    
    # Create a request
    factory = RequestFactory()
    request = factory.get(f'/book/{service.pk}/')
    
    # Add user
    user = User.objects.filter(username='user1').first()
    if user:
        request.user = user
        print(f"User: {user}")
        
        # Call the view
        print("\nCalling view...")
        try:
            response = book_service(request, service.pk)
            print(f"Response status: {response.status_code}")
            print("View executed successfully!")
        except Exception as e:
            print(f"Exception in view: {e}")
            print("\nFull traceback:")
            traceback.print_exc()
    else:
        print("No user1 found")
        
except Exception as e:
    print(f"Setup error: {e}")
    traceback.print_exc()
