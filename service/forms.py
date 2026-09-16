from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, MechanicService, Booking


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists')
        return username


class MechanicProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['is_mechanic', 'phone', 'address', 'city', 'latitude', 'longitude', 'profile_picture']


class MechanicServiceForm(forms.ModelForm):
    class Meta:
        model = MechanicService
        fields = ['service_name', 'price', 'description']


class BookingForm(forms.ModelForm):
    booking_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ['service', 'booking_date']
        # Only expose service and booking_date on the form; mechanic/user/status/created_at
        # are managed in the view or by the form.save override below.

    def __init__(self, *args, **kwargs):
        mechanic = kwargs.pop('mechanic', None)
        super().__init__(*args, **kwargs)
        self.mechanic = mechanic
        if mechanic:
            self.fields['service'].queryset = MechanicService.objects.filter(mechanic=mechanic)

    def save(self, commit=True):
        """Ensure mechanic (and any other auto-managed fields) are set when saving.

        The view typically sets booking.user and booking.mechanic before calling
        save(), but sometimes the form may be responsible for the mechanic when
        one was passed in via the constructor. This method sets the mechanic if
        it is available on the form instance and not already present on the
        model instance.
        """
        booking = super().save(commit=False)
        # If the mechanic was provided to the form and the instance doesn't
        # already have one, set it here.
        if getattr(self, 'mechanic', None) and not getattr(booking, 'mechanic_id', None):
            booking.mechanic = self.mechanic
        if commit:
            booking.save()
        return booking
