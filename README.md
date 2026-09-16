# Mechanic Finder

This is a Django project named `mechanic_finder` with an app `service` that allows users to find mechanics, view profiles, book services, and manage bookings.

Team Members:
1. A S Nishanth - 4MC23IS001
2. Chethan H R - 4MC23IS024
3. Harish H R - 4MC23IS038
4. Jeevan H K - 4MC23IS049
5. Varun K M - 4MC23IS130

Steps on how to set up and run the project
1. Create and activate a virtualenv

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run migrations and create a superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

3. Create demo data

```powershell
python manage.py create_demo_data
```

4. Run the dev server

```powershell
python manage.py runserver
```

Default demo accounts created by `create_demo_data`:
- Mechanics: `mech1` / `password123`, `mech2` / `password123`, `mech3` / `password123`, `mech4` / `password123`
- Users: `user1` / `password123`, `user2` / `password123`

Notes:
- Mechanic service CRUD: mechanics can add/edit/delete their services at `/service/add/`, `/service/<id>/edit/`, and `/service/<id>/delete/` (links available in mechanic dashboard).
- Leaflet maps: the mechanic list and mechanic detail pages include interactive maps using OpenStreetMap/Leaflet. Make sure mechanics have latitude/longitude filled in their profiles to show markers.
- Add Google Maps/OpenStreetMap integration by adding JS to `mechanic_detail.html` and using `latitude` and `longitude` fields.
- The project uses SQLite as requested.
## Quick Start

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows PowerShell, may need: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create demo data:**
   ```bash
   python manage.py create_demo_data
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the app:**
   - Open http://127.0.0.1:8000 in your browser
   - Register as a user or mechanic at /register/
   - Login and explore features

## Demo Credentials
After running `create_demo_data`, use:
- **User:** user1 / password123 or user2 / password123
- **Mechanic:** mech1 / password123, mech2 / password123, mech3 / password123, or mech4 / password123

## Navigation Menu
The navbar includes the following links (visible based on authentication and role):
- **Search**: Browse and search for mechanics by name or city
- **Map / Tracking**: View the mechanic map and locations
- **Services** (mechanics only): Add, edit, or delete your services
- **Bookings**: View all bookings (as user or mechanic)
- **Dashboard**: Role-aware dashboard to manage services, bookings, and profile
- **Register / Login**: Unauthenticated users can register or log in
- **Register as Mechanic**: Link for new mechanics to create an account

## Running Tests
Run the full test suite to verify demo data, map presence, and accept/reject booking flows:

```powershell
python manage.py test service
```

This will:
- Create a test database
- Run `DemoDataCommandTest` to verify demo mechanics and users are created
- Run `MapPresenceTests` to verify Leaflet and OpenStreetMap JS is present on search and mechanic detail pages
- Run `BookingAcceptRejectTests` to verify mechanics can accept/reject bookings via JSON endpoints and non-mechanics are forbidden
- Report overall test results (all 7 tests should pass)

## Features Implemented
- ✅ User and Mechanic registration with profile creation
- ✅ Role-based dashboards (User vs. Mechanic)
- ✅ Mechanic search and filtering by city
- ✅ Mechanic service CRUD (add, edit, delete services)
- ✅ Service booking with availability validation
- ✅ Booking management: view, accept, reject, and complete bookings
- ✅ AJAX JSON endpoints for accept/reject with console email notifications
- ✅ Leaflet/OpenStreetMap integration for mechanic locations and tracking
- ✅ Responsive Bootstrap navbar with role-aware menu options
- ✅ Django test suite (unit + integration tests)
- ✅ Bootstrap responsive UI with messages framework
- ✅ Admin interface for model management
- ✅ SQLite database with demo data

## Note on Template Rendering
Crispy forms functionality is installed but standard Django form rendering (`form.as_p`) is used in templates for compatibility. If you prefer crispy-styled forms, install a crispy template pack (e.g., `crispy-bootstrap4`) and add `{% load crispy_forms_tags %}` + `|crispy` filters to the templates.

## Architecture Notes
- **Booking Validation**: The `Booking.clean()` method defensively infers the mechanic from the selected service if not explicitly set, avoiding `RelatedObjectDoesNotExist` errors during form validation.
- **Booking Form**: `BookingForm.save()` explicitly sets the booking mechanic if the form was initialized with one, ensuring proper model state.
- **Console Email Backend**: In development, the email backend is configured to print to console rather than send actual emails. Change `EMAIL_BACKEND` in settings for production.
- **Map Integration**: Leaflet + OpenStreetMap tiles are included in all pages via `base.html`. Mechanics must have `latitude` and `longitude` set in their profile to display markers on the map.
