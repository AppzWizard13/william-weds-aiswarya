from django.urls import path
from . import views

app_name = 'market_analytics'

urlpatterns = [
    path('terminal/', views.TerminalView.as_view(), name='terminal'),
    path('fyers-login/', views.FyersLoginView.as_view(), name='fyers_login'),
    path('fyers-callback/', views.FyersCallbackView.as_view(), name='fyers_callback'),
]
