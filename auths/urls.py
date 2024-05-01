from django.urls import path, include

from auths.views import KakaoLogin, GoogleLogin, google_login, google_callback
from allauth.socialaccount.providers.google import views as google_view

app_name = 'auths'

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('kakao/login/', KakaoLogin.as_view(), name='kakao_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('google/login/', google_login, name='google_redirect_login'),
    path('google/login/callback/',google_callback, name='google_callback' )
]