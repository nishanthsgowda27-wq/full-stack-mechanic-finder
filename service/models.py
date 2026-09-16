from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_mechanic = models.BooleanField(default=False)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class MechanicService(models.Model):
    mechanic = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.service_name} - {self.mechanic}"


class Booking(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_CONFIRMED = 'Confirmed'
    STATUS_REJECTED = 'Rejected'
    STATUS_COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    mechanic = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_bookings')
    service = models.ForeignKey(MechanicService, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Prevent booking in the past
        if self.booking_date < timezone.now():
            raise ValidationError('Booking date cannot be in the past')

        # Prevent overlapping bookings for the same mechanic at the exact same datetime
        # The mechanic may not yet be set on the instance during form validation
        # (the view often assigns it before saving). Prefer using the instance's
        # mechanic if present; otherwise infer it from the selected service.
        mechanic = getattr(self, 'mechanic', None)
        if mechanic is None and getattr(self, 'service', None):
            # service.mechanic is the UserProfile of the mechanic offering the service
            mechanic = self.service.mechanic

        overlapping = Booking.objects.filter(
            mechanic=mechanic,
            booking_date=self.booking_date
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError('Mechanic already has a booking at this time')

    def __str__(self):
        return f"{self.service} for {self.user} on {self.booking_date}"
