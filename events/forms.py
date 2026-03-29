from django import forms
from .models import Event, RSVP, Couple, WeddingParty, GalleryImage, EventBanner

# Event Form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['couple', 'title', 'date', 'time', 'location','location_url',  'description', 'icon', 'event_image']  # ✅ Added event_image
        widgets = {
            'couple': forms.Select(attrs={'class': 'form-select md-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control md-input', 'placeholder': 'Event Title'}),
            'date': forms.DateInput(attrs={'class': 'form-control md-input', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control md-input', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control md-input', 'placeholder': 'Venue'}),
            'location_url': forms.TextInput(attrs={'class': 'form-control md-input', 'placeholder': 'Venue'}),
            'description': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 4}),
            'icon': forms.Select(attrs={'class': 'form-select md-input'}),
            'event_image': forms.ClearableFileInput(attrs={'class': 'form-control md-input', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icon'].choices = [
            ('fas fa-church', 'Ceremony'),
            ('fas fa-cocktail', 'Cocktail'), 
            ('fas fa-utensils', 'Reception'),
            ('fas fa-glass-cheers', 'After Party'),
            ('fas fa-calendar-alt', 'General'),
        ]
        # Make event_image optional
        self.fields['event_image'].required = False
        self.fields['event_image'].help_text = "Upload an image for this event (optional)"

# RSVP Form  
class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['name', 'email', 'attending', 'guests', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control md-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control md-input'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control md-input', 'min': 1, 'max': 10}),
            'message': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 4}),
        }

# Couple Form (unchanged)
# Couple Form
class CoupleForm(forms.ModelForm):
    class Meta:
        model = Couple
        fields = ['groom_name', 'bride_name', 'wedding_date', 'location', 'story', 'groom_image', 'bride_image', 
                  'groom_bio_line1', 'groom_bio_line2', 'groom_bio_line3', 
                  'bride_bio_line1', 'bride_bio_line2', 'bride_bio_line3']
        widgets = {
            'groom_name': forms.TextInput(attrs={'class': 'form-control md-input'}),
            'bride_name': forms.TextInput(attrs={'class': 'form-control md-input'}),
            'wedding_date': forms.DateInput(attrs={'class': 'form-control md-input', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control md-input'}),
            'story': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 6}),
            'groom_bio_line1': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 2}),
            'groom_bio_line2': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 2}),
            'groom_bio_line3': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 2}),
            'bride_bio_line1': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 2}),
            'bride_bio_line2': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 2}),
            'bride_bio_line3': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 2}),
        }

# WeddingParty Form
class WeddingPartyForm(forms.ModelForm):
    class Meta:
        model = WeddingParty
        fields = ['couple', 'name', 'role', 'image']  # ✅ couple added
        widgets = {
            'couple': forms.Select(attrs={'class': 'form-select md-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control md-input'}),
            'role': forms.Select(attrs={'class': 'form-select md-input'}),
        }

# GalleryImage Form
class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['event', 'title', 'image', 'description']  # ✅ event added
        widgets = {
            'event': forms.Select(attrs={'class': 'form-select md-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control md-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control md-input', 'rows': 3}),
        }


class EventBannerForm(forms.ModelForm):
    """Form for creating and editing EventBanners"""
    
    class Meta:
        model = EventBanner
        fields = [
            'name', 'series', 'image',
            'tagline', 'title_main', 'title_highlight',
            'subtitle', 'button_text',
            'pre_title', 'description', 'rsvp_link', 'details_link', 'is_active', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'series': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'title_main': forms.TextInput(attrs={'class': 'form-control'}),
            'title_highlight': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'pre_title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rsvp_link': forms.TextInput(attrs={'class': 'form-control'}),
            'details_link': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventBannerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':  # Skip checkbox to preserve its class
                field.widget.attrs['class'] = 'form-control'