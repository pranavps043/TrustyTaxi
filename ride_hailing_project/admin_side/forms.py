from django import forms
from .models import Driver, Ride


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'email', 'phone', 'license_number', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter driver full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
                'required': True
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter license number',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required')
        
        # Check if email already exists (for new drivers or when email is changed)
        if self.instance.pk is None:  # New driver
            if Driver.objects.filter(email=email).exists():
                raise forms.ValidationError('A driver with this email already exists.')
        else:  # Existing driver
            if Driver.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('A driver with this email already exists.')
                
        return email
        
    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if not license_number:
            raise forms.ValidationError('License number is required')
            
        # Check if license number already exists
        if self.instance.pk is None:  # New driver
            if Driver.objects.filter(license_number=license_number).exists():
                raise forms.ValidationError('A driver with this license number already exists.')
        else:  # Existing driver
            if Driver.objects.filter(license_number=license_number).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This license number is already in use by another driver.')
                
        return license_number

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pickup', 'dropoff', 'ride_type', 'status']
        widgets = {
            'pickup': forms.TextInput(attrs={'class': 'form-control'}),
            'dropoff': forms.TextInput(attrs={'class': 'form-control'}),
            'ride_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
