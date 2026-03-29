from django.db import models
from django.conf import settings

class BusinessDetails(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    
    # Company Information
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_tagline = models.CharField(max_length=255, null=True, blank=True)
    company_logo = models.ImageField(upload_to='company/', null=True, blank=True)
    company_favicon = models.ImageField(upload_to='company/', null=True, blank=True)
    company_logo_svg = models.FileField(upload_to='company/', null=True, blank=True)
    breadcrumb_image = models.FileField(upload_to='company/', null=True, blank=True)
    about_page_image = models.FileField(upload_to='company/', null=True, blank=True)
    
    # Location Information
    offline_address = models.TextField(null=True, blank=True)
    map_location = models.URLField(help_text="Google Maps embed URL", null=True, blank=True)
    
    # Contact Information
    info_mobile = models.CharField(max_length=20, null=True, blank=True)
    info_email = models.EmailField(null=True, blank=True)
    complaint_mobile = models.CharField(max_length=20, null=True, blank=True)
    complaint_email = models.EmailField(null=True, blank=True)
    sales_mobile = models.CharField(max_length=20, null=True, blank=True)
    sales_email = models.EmailField(null=True, blank=True)
    gstn = models.CharField(max_length=20, null=True, blank=True)
    
    # Social Media
    company_instagram = models.URLField(null=True, blank=True)
    company_facebook = models.URLField(null=True, blank=True)
    company_email_ceo = models.EmailField(null=True, blank=True)
    
    # Business Hours (same for all days)
    opening_time = models.TimeField(default='09:00:00', null=True, blank=True)
    closing_time = models.TimeField(default='17:00:00', null=True, blank=True)
    
    # Days closed (store as comma-separated day codes, e.g. "Sun,Mon")
    closed_days = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Comma-separated days (e.g. Sun,Mon)"
    )

    def __str__(self):
        return self.company_name or "Business Details"

    def get_business_hours(self):
        hours = []
        closed_days = [d.strip() for d in self.closed_days.split(',')] if self.closed_days else []
        
        for day_code, day_name in self.DAY_CHOICES:
            if day_code in closed_days:
                hours.append(f"{day_name}: Closed")
            else:
                if self.opening_time and self.closing_time:
                    hours.append(
                        f"{day_name}: {self.opening_time.strftime('%I:%M %p')} - "
                        f"{self.closing_time.strftime('%I:%M %p')}"
                    )
                else:
                    hours.append(f"{day_name}: Hours not set")
        return hours

    def is_day_closed(self, day_code):
        if not self.closed_days:
            return False
        return day_code in [d.strip() for d in self.closed_days.split(',')]

    class Meta:
        verbose_name = "Business Detail"
        verbose_name_plural = "Business Details"

class Configuration(models.Model):
    config = models.CharField(max_length=255, unique=True, verbose_name="Configuration Key")
    value = models.CharField(max_length=255, verbose_name="Configuration Value")
    
    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"
        ordering = ['config']
    
    def __str__(self):
        return f"{self.config}: {self.value}"