#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.conf import settings
settings.ALLOWED_HOSTS = ['testserver']

c = Client()
r = c.get('/tracking/', HTTP_HOST='testserver')
content = r.content.decode('utf-8')

# Check for key components
checks = {
    'Status 200': r.status_code == 200,
    'Has tracking-map div': 'id="tracking-map"' in content,
    'Has Leaflet CSS link': 'leaflet.css' in content,
    'Has Leaflet JS': 'leaflet.js' in content,
    'Has mechanics data': 'const mechanics' in content,
    'Has initMap function': 'function initMap' in content,
    'Has OpenStreetMap tiles': 'openstreetmap.org' in content,
}

for check, result in checks.items():
    print(f'{"✓" if result else "✗"} {check}')

# Extract the mechanics JSON
import re
match = re.search(r'const mechanics = (\[.*?\]);', content, re.DOTALL)
if match:
    mechanics_str = match.group(1)
    print(f'\n✓ Found mechanics JSON ({len(mechanics_str)} chars)')
    print(f'  Preview: {mechanics_str[:150]}...')
else:
    print('\n✗ Could not find mechanics JSON')
    if '[{' in content:
        idx = content.find('[{')
        print(f'  But found array at position {idx}:')
        print(f'  {content[idx:idx+200]}')

# Save the full HTML to a file for inspection
with open('tracking_map_output.html', 'w') as f:
    f.write(content)
print('\n✓ Full HTML saved to tracking_map_output.html')
