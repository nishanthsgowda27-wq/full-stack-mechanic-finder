#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.conf import settings

# Temporarily allow testserver
settings.ALLOWED_HOSTS = ['testserver', '127.0.0.1', 'localhost']

client = Client()
response = client.get('/tracking/', HTTP_HOST='testserver')

print(f"Status: {response.status_code}")
print(f"Content length: {len(response.content)}")

# Check if mechanics data is in the response
if 'mechanics_geojson' in response.content.decode('utf-8'):
    print("✓ mechanics_geojson found in template context")

# Check for key map elements
content = response.content.decode('utf-8')
if 'L.map' in content:
    print("✓ Leaflet L.map found")
if 'L.marker' in content:
    print("✓ Leaflet L.marker found")
if 'OpenStreetMap' in content or 'openstreetmap' in content:
    print("✓ OpenStreetMap attribution found")

# Look for the JSON data in the page
import re
matches = re.findall(r'const mechanics = ({.*?});', content, re.DOTALL)
if matches:
    print(f"✓ Found mechanics JSON data")
    print(f"  JSON preview: {matches[0][:200]}...")
else:
    print("✗ Could not find mechanics JSON data in page")
    # Try to find it with a simpler pattern
    if '{"id"' in content or '"latitude"' in content:
        print("  But found JSON-like content in page")
        # Extract a sample
        idx = content.find('{"id"')
        if idx > 0:
            print(f"  Sample: {content[idx:idx+200]}")

# Check for demo mechanics in response
for mech in ['mech1', 'mech2', 'mech3', 'mech4']:
    if mech in content:
        print(f"✓ {mech} found in page")

print("\nDone!")
