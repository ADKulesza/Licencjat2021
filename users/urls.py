from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('password/', views.PasswordsChangeView.as_view(template_name='users/change-password.html'), name='change_password'),
]

