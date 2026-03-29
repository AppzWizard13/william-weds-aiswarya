from django import forms
from .models import BusinessDetails
from datetime import datetime

class BusinessDetailsForm(forms.ModelForm):
    # Customizing time fields to use time picker
    opening_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control md-field'}),
        required=False,
        help_text="Opening time (same for all working days)",
        input_formats=['%H:%M', '%H:%M:%S', '%I:%M %p']  # Add supported formats
    )
    closing_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control md-field'}),
        required=False,
        help_text="Closing time (same for all working days)",
        input_formats=['%H:%M', '%H:%M:%S', '%I:%M %p']  # Add supported formats
    )
    
    # Changed closed_days to CharField with max_length=20
    closed_days = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Sunday, Monday or Sun, Mon',
            'class': 'form-control md-field'
        }),
        help_text="Enter closed days (max 20 characters)"
    )
    
    class Meta:
        model = BusinessDetails
        fields = '__all__'
        widgets = {
            'offline_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control md-field'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': 'Enter company name'}),
            'company_tagline': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': 'Your company tagline'}),
            'gstn': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': 'xxxxxxxxxxxxxxx'}),
            'company_instagram': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': 'https://instagram.com/...'}),
            'company_facebook': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': 'https://facebook.com/...'}),
            'company_email_ceo': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': 'ceo@company.com'}),
            'info_mobile': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': '+1234567890'}),
            'info_email': forms.EmailInput(attrs={'class': 'form-control md-field', 'placeholder': 'info@company.com'}),
            'complaint_mobile': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': '+1234567890'}),
            'complaint_email': forms.EmailInput(attrs={'class': 'form-control md-field', 'placeholder': 'complaint@company.com'}),
            'sales_mobile': forms.TextInput(attrs={'class': 'form-control md-field', 'placeholder': '+1234567890'}),
            'sales_email': forms.EmailInput(attrs={'class': 'form-control md-field', 'placeholder': 'sales@company.com'}),
            'map_location': forms.URLInput(attrs={'class': 'form-control md-field', 'placeholder': 'https://maps.google.com/...'}),
            'company_logo': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control md-field'}),
            'company_logo_svg': forms.FileInput(attrs={'accept': 'image/svg+xml', 'class': 'form-control md-field'}),
            'company_favicon': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control md-field'}),
            'breadcrumb_image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control md-field'}),
            'about_page_image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control md-field'}),
        }
        help_texts = {
            'company_logo_svg': 'Upload SVG version of your logo for better quality',
            'company_favicon': 'Recommended size: 32x32 or 16x16 pixels (ICO/PNG format)',
            'map_location': 'Embed URL from Google Maps',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial values for time fields
        if self.instance and self.instance.pk:
            # Opening time
            if self.instance.opening_time:
                self.fields['opening_time'].initial = self.instance.opening_time.strftime('%H:%M')
            
            # Closing time
            if self.instance.closing_time:
                self.fields['closing_time'].initial = self.instance.closing_time.strftime('%H:%M')
        else:
            # Set default values for new instances
            self.fields['opening_time'].initial = '09:00'
            self.fields['closing_time'].initial = '17:00'
        
        # Make all fields optional (since model has null=True, blank=True)
        for field_name, field in self.fields.items():
            field.required = False

    def clean(self):
        cleaned_data = super().clean()
        
        # Get time values (they should already be time objects from forms.TimeField)
        opening_time = cleaned_data.get('opening_time')
        closing_time = cleaned_data.get('closing_time')
        
        # Debug print to see what we're getting
        print(f"Opening time: {opening_time} (type: {type(opening_time)})")
        print(f"Closing time: {closing_time} (type: {type(closing_time)})")
        
        # Validate that closing time is after opening time (only if both are provided)
        if opening_time and closing_time:
            if opening_time >= closing_time:
                raise forms.ValidationError(
                    "Closing time must be after opening time"
                )
        
        return cleaned_data
    
    # def clean_closed_days(self):
    #     closed_days = self.cleaned_data.get('closed_days', '')
    #     if closed_days and len(closed_days) > 20:
    #         raise forms.ValidationError(
    #             "Closed days must be 20 characters or less"
    #         )
    #     return closed_days
    

from django import forms
from .models import Configuration

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ['config', 'value']
        widgets = {
            'config': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }