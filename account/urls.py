# account/urls.py
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from . import views
from .views import (
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
)

app_name = 'account'

urlpatterns = [
    # —– login / logout overrides —–
    path(
        'login/',
        LoginView.as_view(template_name='register/login.html'),
        name='login'
    ),
    path(
        'logout/',
        CustomLogoutView.as_view(),
        name='logout'
    ),

    # —– password-change form —–
    path(
        'password_change/',
        CustomPasswordChangeView.as_view(),
        name='password_change'
    ),

    # —– “done” landing page —–
    path(
        'password_change/done/',
        CustomPasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    # —– the rest of Django’s auth URLs (reset, etc.) —–
    path('', include('django.contrib.auth.urls')),

    # —– your own views —–
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]
