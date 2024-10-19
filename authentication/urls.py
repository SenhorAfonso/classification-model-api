from django.urls import path
from . import views

urlpatterns = [
    path('google-sso', views.make_sso_login, name='make_sso_login'),
    path('get-emails', views.get_all_emails, name='get_all_emails'),
    path('get-single-emails/<message_id>', views.get_single_email, name='get_single_email'),
    path('login-google', views.login_with_google, name='login_with_google'),
]
