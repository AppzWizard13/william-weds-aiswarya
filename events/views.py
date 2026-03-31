from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
)
from django.urls import reverse_lazy
from .models import Couple, WeddingParty, Event, GalleryImage, RSVP, EventBanner
from .forms import EventForm, RSVPForm, CoupleForm, WeddingPartyForm, GalleryImageForm, EventBannerForm

# Home
from django.utils import timezone
from datetime import datetime

class HomeView(TemplateView):
    template_name = 'events/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'home'
        context['couple'] = Couple.objects.first()
        context['events'] = Event.objects.filter(location_url__isnull=False).order_by('date', 'time')
        context['wedding_party'] = WeddingParty.objects.all()
        context['gallery_images'] = GalleryImage.objects.all()[:6]
        context['banners'] = EventBanner.objects.order_by('series')

        # Get nearest upcoming event
        now = timezone.now()
        upcoming_events = Event.objects.filter(
            date__gte=now.date()
        ).order_by('date', 'time')

        if upcoming_events.exists():
            context['next_event'] = upcoming_events.first()
            next_event_datetime = datetime.combine(
                context['next_event'].date,
                context['next_event'].time
            )
            context['next_event_datetime'] = next_event_datetime
        else:
            context['next_event'] = None
            context['next_event_datetime'] = None

        # Get banner where series = 19 and order = 10
        story_banner = (
            EventBanner.objects
            .filter(series=10)
            .first()
        )
        context['story_image'] = story_banner.image.url if story_banner else ""

        return context
# ===== EVENTS CRUD =====
class EventsListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10
    ordering = ['date', 'time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'events'
        return context

class EventDetailView(DetailView):  # ✅ COMPLETE
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'event_detail'
        context['rsvps'] = self.object.rsvps.all()[:5]  # ✅ Related RSVPs
        context['gallery_images'] = self.object.gallery_images.all()[:12]  # ✅ Related Gallery
        return context

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'event_create'
        context['couples'] = Couple.objects.all()
        return context

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'event_update'
        context['couples'] = Couple.objects.all()
        return context



class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('events:events')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Use the correct field name (title, event_name, etc.)
        event_title = self.object.title  # or self.object.event_name
        self.object.delete()
        
        messages.success(request, f'Event "{event_title}" has been deleted successfully.')
        
        return HttpResponseRedirect(self.get_success_url())

# ===== COUPLE CRUD =====
class CoupleListView(ListView):
    model = Couple
    template_name = 'events/couple_list.html'
    context_object_name = 'couples'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'couple_list'
        return context

class CoupleCreateView(CreateView):
    model = Couple
    form_class = CoupleForm
    template_name = 'events/couple_form.html'
    success_url = reverse_lazy('events:couple_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'couple_create'
        return context

class CoupleUpdateView(UpdateView):
    model = Couple
    form_class = CoupleForm
    template_name = 'events/couple_form.html'
    success_url = reverse_lazy('events:couple_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'couple_update'
        return context

# ===== WEDDING PARTY CRUD =====
class WeddingPartyListView(ListView):
    model = WeddingParty
    template_name = 'events/wedding_party_list.html'
    context_object_name = 'wedding_party'
    ordering = ['role', 'name']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'wedding_party_list'
        context['couples'] = Couple.objects.all()
        return context

class WeddingPartyCreateView(CreateView):
    model = WeddingParty
    form_class = WeddingPartyForm
    template_name = 'events/wedding_party_form.html'
    success_url = reverse_lazy('events:wedding_party_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'wedding_party_create'
        context['couples'] = Couple.objects.all()
        return context

class WeddingPartyUpdateView(UpdateView):
    model = WeddingParty
    form_class = WeddingPartyForm
    template_name = 'events/wedding_party_form.html'
    success_url = reverse_lazy('events:wedding_party_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'wedding_party_update'
        context['couples'] = Couple.objects.all()
        return context

# ===== GALLERY CRUD =====
class GalleryView(ListView):
    model = GalleryImage
    template_name = 'events/gallery_list.html'
    context_object_name = 'gallery_images'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'gallery_list'
        context['events'] = Event.objects.all()
        return context

class GalleryImageCreateView(CreateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'events/gallery_image_form.html'
    success_url = reverse_lazy('events:gallery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'gallery_create'
        context['events'] = Event.objects.all()
        return context

class GalleryImageUpdateView(UpdateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'events/gallery_image_form.html'
    success_url = reverse_lazy('events:gallery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'gallery_update'
        context['events'] = Event.objects.all()
        return context
    
class GalleryImageDeleteView(DeleteView):
    model = GalleryImage
    success_url = reverse_lazy('events:gallery_list')
    template_name = 'events/gallery_image_confirm_delete.html'  # Optional: create this template
    
    def delete(self, request, *args, **kwargs):
        # Optional: Add success message
        messages.success(request, 'Photo deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'gallery_delete'
        context['events'] = Event.objects.all()
        return context

# ===== RSVP =====
class RSVPView(FormView):
    template_name = 'events/rsvp.html'
    form_class = RSVPForm
    success_url = reverse_lazy('rsvp_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'rsvp'
        return context
    
    def form_valid(self, form):
        form.instance.event = Event.objects.first()  # Default event
        form.save()
        return super().form_valid(form)

class RSVPSuccessView(TemplateView):
    template_name = 'events/rsvp_success.html'

class RegistryView(TemplateView):
    template_name = 'events/registry.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'registry'
        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.conf import settings

from .models import EventBanner


class EventBannerListView(LoginRequiredMixin, ListView):
    model = EventBanner
    template_name = 'admin_panel/event_banner_list.html'
    context_object_name = 'banners'

    def get_template_names(self):
        """Logic for switching templates belongs here."""
        admin_mode = getattr(settings, 'ADMIN_PANEL_MODE', 'basic').lower()
        if admin_mode == 'advanced':
            return ['advadmin/event_banner_list.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        """Logic for adding extra variables to the template."""
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'event_banner_list'
        return context


class EventBannerCreateView(LoginRequiredMixin, CreateView):
    model = EventBanner
    form_class = EventBannerForm
    template_name = 'admin_panel/event_banner_form.html.html'
    success_url = reverse_lazy('events:event_banner_list')

    def form_valid(self, form):
        messages.success(self.request, "EventBanner added successfully!")
        return super().form_valid(form)

    def get_template_names(self):
        admin_mode = getattr(settings, 'ADMIN_PANEL_MODE', 'basic').lower()
        if admin_mode == 'advanced':
            return ['advadmin/event_banner_form.html']
        return ['admin_panel/event_banner_form.html']

    def form_invalid(self, form):
        messages.error(self.request, "There was an error adding the banner. Please check the form.")
        return super().form_invalid(form)


class EventBannerDetailView(LoginRequiredMixin, DetailView):
    model = EventBanner
    template_name = 'admin_panel/banner_detail.html'
    context_object_name = 'event_banner_list'

    def get_template_names(self):
        admin_mode = getattr(settings, 'ADMIN_PANEL_MODE', 'basic').lower()
        if admin_mode == 'advanced':
            return ['advadmin/event_banner_form.html']
        return ['admin_panel/event_banner_form.html']


class EventBannerUpdateView(LoginRequiredMixin, UpdateView):
    model = EventBanner
    form_class = EventBannerForm
    template_name = 'admin_panel/event_banner_form.html'
    success_url = reverse_lazy('events:event_banner_list')

    def form_valid(self, form):
        messages.success(self.request, "EventBanner updated successfully!")
        return super().form_valid(form)

    def get_template_names(self):
        admin_mode = getattr(settings, 'ADMIN_PANEL_MODE', 'basic').lower()
        if admin_mode == 'advanced':
            return ['advadmin/event_banner_form.html']
        return ['admin_panel/event_banner_form.html']

    def form_invalid(self, form):
        messages.error(self.request, "Error updating banner. Please check the form.")
        return super().form_invalid(form)


class EventBannerDeleteView(LoginRequiredMixin, DeleteView):
    model = EventBanner
    success_url = reverse_lazy('events:event_banner_list')
    template_name = None

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "EventBanner deleted successfully!")
        return super().delete(request, *args, **kwargs)