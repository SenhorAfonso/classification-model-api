from django.urls import path
from . import views

urlpatterns = [
    path('google-sso', views.make_sso_login, name='make_sso_login'),
    path('get-emails', views.list_email_messages, name='get_google_token'),
    path('get-single-emails/<message_id>', views.get_email_message, name='get_google_token'),
]