from django.urls import path
from . import views

urlpatterns = [
    path('create_form/', views.create_form, name='create_form'),

    path('get_response/', views.get_response, name='get_response'),

    path('send_sms_notification/', views.send_sms_notification, name='send_sms_notification'),
]