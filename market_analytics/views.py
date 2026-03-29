import os
from django.conf import settings
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from fyers_apiv3 import fyersModel

class TerminalView(LoginRequiredMixin, TemplateView):
    template_name = 'market_analytics/terminal.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('fyers_access_token'):
            return render(request, 'market_analytics/login.html', {'page_name': 'market_analytics'})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'market_analytics'
        context['fyers_access_token'] = self.request.session.get('fyers_access_token')
        context['csrf_token'] = self.request.csrf_token  # For AJAX
        return context



class FyersLoginView(LoginRequiredMixin, RedirectView):
    """Initiates OAuth using app_id and secret_id from the User model"""
    
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        
        # Fetching credentials from your CustomUser model
        client_id = user.app_id
        secret_key = user.secret_id  # EncryptedCharField decrypts automatically on access
        
        if not client_id or not secret_key:
            messages.error(self.request, "Please update your App ID and Secret ID in your profile first.")
            return reverse('market_analytics:terminal')

        # Construct the exact URL using your .env base
        callback_path = reverse('market_analytics:fyers_callback')
        redirect_uri = f"{settings.NGROK_URL.rstrip('/')}{callback_path}"
        
        # DEBUG: Print this to your terminal to verify it matches Fyers Dashboard exactly
        print(f"DEBUG: Redirect URI being sent: {redirect_uri}")
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_uri=redirect_uri,
            response_type='code',
            grant_type='authorization_code'
        )
        
        return session.generate_authcode()

class FyersCallbackView(LoginRequiredMixin, TemplateView):
    """Handles callback and generates token using User model credentials"""
    
    def get(self, request, *args, **kwargs):
        # 1. Capture the authorization code from Fyers redirect
        auth_code = request.GET.get('auth_code')
        user = request.user

        if not auth_code:
            messages.error(request, "Fyers Login Failed: No auth code received.")
            return redirect('market_analytics:terminal')

        try:
            # 2. Prepare credentials
            client_id = user.app_id
            secret_key = user.secret_id
            # Ensure this matches exactly what is in your Fyers Dashboard
            redirect_uri = request.build_absolute_uri(reverse('market_analytics:fyers_callback'))

            # 3. Initialize SessionModel with V3 requirements
            session = fyersModel.SessionModel(
                client_id=client_id,
                secret_key=secret_key,
                redirect_uri=redirect_uri,
                response_type='code',        # Mandatory for V3
                grant_type='authorization_code'
            )
            
            # 4. Set the received auth_code
            session.set_token(auth_code)
            
            # 5. Exchange code for access token (Correct V3 method)
            response = session.generate_token()
            
            # 6. Verify and store the token
            if response.get('s') == 'ok':
                request.session['fyers_access_token'] = response.get('access_token')
                messages.success(request, "Fyers Connected Successfully!")
            else:
                error_msg = response.get('message', 'Unknown API Error')
                messages.error(request, f"Fyers API Error: {error_msg}")
            
        except Exception as e:
            messages.error(request, f"Token Generation Error: {str(e)}")

        return redirect('market_analytics:terminal')