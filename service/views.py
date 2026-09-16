from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, MechanicService, Booking
from .forms import UserRegisterForm, MechanicProfileForm, MechanicServiceForm, BookingForm
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.mail import send_mail


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = MechanicProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_mechanic = False
            profile.save()
            messages.success(request, 'User registered successfully')
            return redirect('service:login')
    else:
        form = UserRegisterForm()
        profile_form = MechanicProfileForm()
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form, 'user_type': 'User'})


def register_mechanic(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = MechanicProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_mechanic = True
            profile.save()
            messages.success(request, 'Mechanic registered successfully')
            return redirect('service:login')
    else:
        form = UserRegisterForm()
        profile_form = MechanicProfileForm()
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form, 'user_type': 'Mechanic'})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            # redirect based on profile
            try:
                if user.userprofile.is_mechanic:
                    return redirect('service:dashboard_mechanic')
            except Exception:
                pass
            return redirect('service:dashboard_user')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('service:login')


@login_required
def dashboard_user(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    bookings = profile.bookings.all()
    # Group bookings by status for user dashboard
    pending_bookings = bookings.filter(status=Booking.STATUS_PENDING).order_by('-booking_date')
    confirmed_bookings = bookings.filter(status=Booking.STATUS_CONFIRMED).order_by('-booking_date')
    rejected_bookings = bookings.filter(status=Booking.STATUS_REJECTED).order_by('-booking_date')
    completed_bookings = bookings.filter(status=Booking.STATUS_COMPLETED).order_by('-booking_date')
    return render(request, 'dashboard_user.html', {
        'profile': profile,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'rejected_bookings': rejected_bookings,
        'completed_bookings': completed_bookings,
    })


@login_required
def dashboard_mechanic(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_mechanic:
        messages.error(request, 'Access denied')
        return redirect('service:dashboard_user')
    services = profile.services.all()
    bookings = profile.received_bookings.all()
    # Group bookings by status for the dashboard
    pending_bookings = bookings.filter(status=Booking.STATUS_PENDING).order_by('-booking_date')
    confirmed_bookings = bookings.filter(status=Booking.STATUS_CONFIRMED).order_by('-booking_date')
    rejected_bookings = bookings.filter(status=Booking.STATUS_REJECTED).order_by('-booking_date')
    completed_bookings = bookings.filter(status=Booking.STATUS_COMPLETED).order_by('-booking_date')
    return render(request, 'dashboard_mechanic.html', {
        'profile': profile,
        'services': services,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'rejected_bookings': rejected_bookings,
        'completed_bookings': completed_bookings,
    })


def index(request):
    """Redirect root URL to mechanic search/list page."""
    return redirect('service:search_mechanic')


def search_mechanic(request):
    query = request.GET.get('q')
    city = request.GET.get('city')
    mechanics = UserProfile.objects.filter(is_mechanic=True)
    if city:
        mechanics = mechanics.filter(city__icontains=city)
    if query:
        # Use Q objects for a clear OR across user fields
        q = Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
        mechanics = mechanics.filter(q)
    return render(request, 'mechanic_list.html', {'mechanics': mechanics})


def mechanic_detail(request, id):
    profile = get_object_or_404(UserProfile, pk=id, is_mechanic=True)
    services = profile.services.all()
    return render(request, 'mechanic_detail.html', {'mechanic': profile, 'services': services})


@login_required
def book_service(request, service_id):
    service = get_object_or_404(MechanicService, pk=service_id)
    mechanic_profile = service.mechanic
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, mechanic=mechanic_profile)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = user_profile
            booking.mechanic = mechanic_profile
            # Debug: verify mechanic is set
            print(f"DEBUG: booking.mechanic = {booking.mechanic}")
            print(f"DEBUG: booking.mechanic_id = {booking.mechanic_id}")
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, 'Booking requested successfully')
                return redirect('service:manage_bookings')
            except Exception as e:
                form.add_error(None, e)
    else:
        form = BookingForm(mechanic=mechanic_profile, initial={'service': service})
    return render(request, 'book_service.html', {'form': form, 'service': service})


@login_required
def manage_bookings(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.is_mechanic:
        bookings = profile.received_bookings.order_by('-booking_date')
    else:
        bookings = profile.bookings.order_by('-booking_date')
    return render(request, 'booking_list.html', {'bookings': bookings, 'profile': profile})


@login_required
def accept_booking(request, booking_id):
    """Allow the mechanic who owns the booking to accept (confirm) it."""
    booking = get_object_or_404(Booking, pk=booking_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_mechanic or booking.mechanic != profile:
        return HttpResponseForbidden('You do not have permission to accept this booking')
    if request.method == 'POST':
        booking.status = Booking.STATUS_CONFIRMED
        booking.save()
        # Notify booking owner via email (console backend in dev)
        try:
            recipient = booking.user.user.email
            if recipient:
                send_mail(
                    subject='Your booking was accepted',
                    message=f'Your booking for {booking.service} on {booking.booking_date} was accepted by the mechanic.',
                    from_email=None,
                    recipient_list=[recipient],
                )
        except Exception:
            pass
        messages.success(request, 'Booking accepted')
    return redirect('service:manage_bookings')


@login_required
def accept_booking_ajax(request, booking_id):
    """AJAX endpoint to accept a booking; returns JSON."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    booking = get_object_or_404(Booking, pk=booking_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_mechanic or booking.mechanic != profile:
        return JsonResponse({'error': 'forbidden'}, status=403)
    booking.status = Booking.STATUS_CONFIRMED
    booking.save()
    # Send notification email
    try:
        recipient = booking.user.user.email
        if recipient:
            send_mail(
                subject='Your booking was accepted',
                message=f'Your booking for {booking.service} on {booking.booking_date} was accepted by the mechanic.',
                from_email=None,
                recipient_list=[recipient],
            )
    except Exception:
        pass
    return JsonResponse({'status': 'confirmed', 'booking_id': booking.pk})


@login_required
def reject_booking(request, booking_id):
    """Allow the mechanic who owns the booking to reject it."""
    booking = get_object_or_404(Booking, pk=booking_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_mechanic or booking.mechanic != profile:
        return HttpResponseForbidden('You do not have permission to reject this booking')
    if request.method == 'POST':
        booking.status = Booking.STATUS_REJECTED
        booking.save()
        try:
            recipient = booking.user.user.email
            if recipient:
                send_mail(
                    subject='Your booking was rejected',
                    message=f'Your booking for {booking.service} on {booking.booking_date} was rejected by the mechanic.',
                    from_email=None,
                    recipient_list=[recipient],
                )
        except Exception:
            pass
        messages.info(request, 'Booking rejected')
    return redirect('service:manage_bookings')


@login_required
def reject_booking_ajax(request, booking_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    booking = get_object_or_404(Booking, pk=booking_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_mechanic or booking.mechanic != profile:
        return JsonResponse({'error': 'forbidden'}, status=403)
    booking.status = Booking.STATUS_REJECTED
    booking.save()
    try:
        recipient = booking.user.user.email
        if recipient:
            send_mail(
                subject='Your booking was rejected',
                message=f'Your booking for {booking.service} on {booking.booking_date} was rejected by the mechanic.',
                from_email=None,
                recipient_list=[recipient],
            )
    except Exception:
        pass
    return JsonResponse({'status': 'rejected', 'booking_id': booking.pk})


@login_required
def service_add(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_mechanic:
        messages.error(request, 'Only mechanics can add services')
        return redirect('service:dashboard_user')
    if request.method == 'POST':
        form = MechanicServiceForm(request.POST)
        if form.is_valid():
            svc = form.save(commit=False)
            svc.mechanic = profile
            svc.save()
            messages.success(request, 'Service added')
            return redirect('service:dashboard_mechanic')
    else:
        form = MechanicServiceForm()
    return render(request, 'service_form.html', {'form': form, 'action': 'Add Service'})


@login_required
def service_edit(request, pk):
    svc = get_object_or_404(MechanicService, pk=pk)
    # ensure owner
    if svc.mechanic.user != request.user:
        return HttpResponseForbidden('You do not have permission to edit this service')
    if request.method == 'POST':
        form = MechanicServiceForm(request.POST, instance=svc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated')
            return redirect('service:dashboard_mechanic')
    else:
        form = MechanicServiceForm(instance=svc)
    return render(request, 'service_form.html', {'form': form, 'action': 'Edit Service'})


@login_required
@require_http_methods(['GET', 'POST'])
def service_delete(request, pk):
    svc = get_object_or_404(MechanicService, pk=pk)
    if svc.mechanic.user != request.user:
        return HttpResponseForbidden('You do not have permission to delete this service')
    if request.method == 'POST':
        svc.delete()
        messages.success(request, 'Service deleted')
        return redirect('service:dashboard_mechanic')
    return render(request, 'service_confirm_delete.html', {'service': svc})


def tracking_map(request):
    """Display a full-page map with all mechanics' locations."""
    import json
    from decimal import Decimal
    
    mechanics = UserProfile.objects.filter(is_mechanic=True)
    # Serialize mechanics to JSON for the map JS
    mechanics_data = []
    for m in mechanics:
        mechanics_data.append({
            'id': m.pk,
            'name': m.user.get_full_name() or m.user.username,
            'city': m.city or 'Unknown',
            'latitude': float(m.latitude) if m.latitude else None,
            'longitude': float(m.longitude) if m.longitude else None,
            'phone': m.phone or 'N/A',
        })
    
    # Use json.dumps with proper encoder for Decimal
    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            return super().default(obj)
    
    mechanics_json = json.dumps(mechanics_data, cls=DecimalEncoder)
    return render(request, 'tracking_map.html', {
        'mechanics': mechanics,
        'mechanics_json': mechanics_json,
    })
