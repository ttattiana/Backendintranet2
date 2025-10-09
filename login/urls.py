from django.urls import path
from .views import login_view, verify_otp, register_view

urlpatterns = [
    path('login', login_view),
    path('verify-otp', verify_otp),
    path('register', register_view, name='register'),
]
