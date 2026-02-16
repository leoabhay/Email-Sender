from django.urls import path
from .views import send_email, email_sent

urlpatterns = [
    path('', send_email, name='send_email'),
    path('sent/', email_sent, name='email_sent'),
]