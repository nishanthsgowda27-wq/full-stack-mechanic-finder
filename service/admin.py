from django.contrib import admin
from .models import UserProfile, MechanicService, Booking


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_mechanic', 'city', 'phone')


@admin.register(MechanicService)
class MechanicServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'mechanic', 'price')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'mechanic', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
