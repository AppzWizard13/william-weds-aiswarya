from django.db import models

class Couple(models.Model):
    # Groom fields
    groom_name = models.CharField(max_length=100, default="James Smith")
    groom_image = models.ImageField(upload_to='couple/', blank=True, null=True)
    groom_bio_line1 = models.TextField(blank=True, null=True, help_text="First line of groom's biography")
    groom_bio_line2 = models.TextField(blank=True, null=True, help_text="Second line of groom's biography")
    groom_bio_line3 = models.TextField(blank=True, null=True, help_text="Third line of groom's biography")
    
    # Bride fields
    bride_name = models.CharField(max_length=100, default="Jane Doe")
    bride_image = models.ImageField(upload_to='couple/', blank=True, null=True)
    bride_bio_line1 = models.TextField(blank=True, null=True, help_text="First line of bride's biography")
    bride_bio_line2 = models.TextField(blank=True, null=True, help_text="Second line of bride's biography")
    bride_bio_line3 = models.TextField(blank=True, null=True, help_text="Third line of bride's biography")
    
    # Wedding details (ADDED FIELDS)
    wedding_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    story = models.TextField(blank=True, null=True, help_text="Love story")
    
    def __str__(self):
        return f"{self.groom_name} & {self.bride_name}"


class WeddingParty(models.Model):
    ROLE_CHOICES = [
        ('best_man', 'Best Man'),
        ('maid_honor', 'Maid of Honor'),
        ('groomsman', 'Groomsman'),
        ('bridesmaid', 'Bridesmaid'),
        ('flower_girl', 'Flower Girl'),
        ('ring_bearer', 'Ring Bearer'),
    ]
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='party_members')  # ✅ FK Added
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='wedding_party/', blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class Event(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='events')  # ✅ FK Added
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    location_url = models.CharField(max_length=520)

    description = models.TextField(blank=True)  # ✅ Made blank=True
    icon = models.CharField(max_length=50, choices=[
        ('fas fa-church', 'Ceremony'),
        ('fas fa-cocktail', 'Cocktail'),
        ('fas fa-utensils', 'Reception'),
        ('fas fa-glass-cheers', 'Party'),
        ('fas fa-calendar-alt', 'Event'),
    ], default='fas fa-calendar-alt')  # ✅ Choices added
    
    # ✅ NEW: Event image field
    event_image = models.ImageField(upload_to='events/', blank=True, null=True, help_text="Upload an image for this event")
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gallery_images', blank=True, null=True)  # ✅ FK Added
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')  # ✅ FK Added
    ATTENDING_CHOICES = [
        (True, 'Yes, Attending'),
        (False, 'No, Regretfully Declining'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    attending = models.BooleanField(choices=ATTENDING_CHOICES)
    guests = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_attending_display()}"


class EventBanner(models.Model):
    name = models.CharField(max_length=255)
    series = models.IntegerField()
    image = models.ImageField(upload_to='event/banners/')

    # New fields for text content
    tagline = models.CharField(max_length=255, blank=True, help_text="E.g. SHAPE YOUR BODY or We're Getting Married")
    title_main = models.CharField(max_length=255, blank=True, null=True, help_text="E.g. BE or James")
    title_highlight = models.CharField(max_length=255, blank=True, null=True, help_text="E.g. STRONG or Jane")
    subtitle = models.CharField(max_length=255, blank=True, null=True, help_text="E.g. TRAINING HARD or wedding description")
    button_text = models.CharField(max_length=100, blank=True, default='Get Info')
    
    # Additional fields for wedding hero section
    pre_title = models.CharField(max_length=255, blank=True, null=True, help_text="Small text above title (e.g., We're Getting Married)")
    description = models.TextField(blank=True, null=True, help_text="Hero description text")
    rsvp_link = models.CharField(max_length=500, blank=True, null=True, default="#rsvp")
    details_link = models.CharField(max_length=500, blank=True, null=True, default="#details")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'series']

    def __str__(self):
        return self.name