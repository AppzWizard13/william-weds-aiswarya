from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # ===== EVENTS =====
    path('events/', views.EventsListView.as_view(), name='events'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/add/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    # ===== COUPLE =====
    path('couple/', views.CoupleListView.as_view(), name='couple_list'),
    path('couple/add/', views.CoupleCreateView.as_view(), name='couple_create'),
    path('couple/<int:pk>/update/', views.CoupleUpdateView.as_view(), name='couple_update'),

    # ===== WEDDING PARTY =====
    path('wedding-party/', views.WeddingPartyListView.as_view(), name='wedding_party_list'),
    path('wedding-party/add/', views.WeddingPartyCreateView.as_view(), name='wedding_party_create'),
    path('wedding-party/<int:pk>/update/', views.WeddingPartyUpdateView.as_view(), name='wedding_party_update'),

    # ===== GALLERY =====
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('gallery/add/', views.GalleryImageCreateView.as_view(), name='gallery_create'),
    path('gallery/<int:pk>/update/', views.GalleryImageUpdateView.as_view(), name='gallery_update'),

    # ===== RSVP =====
    path('rsvp/', views.RSVPView.as_view(), name='rsvp'),
    path('rsvp/success/', views.RSVPSuccessView.as_view(), name='rsvp_success'),

    # ===== REGISTRY =====
    path('registry/', views.RegistryView.as_view(), name='registry'),

    # ===== EVENT BANNERS =====
    path('event_banners/', views.EventBannerListView.as_view(), name='banner_list'),
    path('event_banners/add/', views.EventBannerCreateView.as_view(), name='banner_create'),
    path('event_banners/<int:pk>/', views.EventBannerDetailView.as_view(), name='banner_detail'),
    path('event_banners/<int:pk>/update/', views.EventBannerUpdateView.as_view(), name='banner_update'),
    path('event_banners/<int:pk>/delete/', views.EventBannerDeleteView.as_view(), name='banner_delete'),
]