from django.conf.urls import url
from . import views

urlpatterns = [
    url('/send_sms', views.send_sms),
    url('/register',views.register),
]
