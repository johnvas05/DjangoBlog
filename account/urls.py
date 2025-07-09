# account/urls.py
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    LoginView,

)
from . import views
from .views import (
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    CustomPasswordResetView,
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
path(
      'password_reset/',
      CustomPasswordResetView.as_view(),
      name='password_reset'
    ),

    # “check your inbox” page
    path(
      'password_reset/done/',
      CustomPasswordResetDoneView.as_view(),
      name='password_reset_done'
    ),

    # the link you click in the email
    path(
      'reset/<uidb64>/<token>/',
      CustomPasswordResetConfirmView.as_view(),
      name='password_reset_confirm'
    ),

    # final “your password’s been set” page
    path(
      'reset/done/',
      CustomPasswordResetCompleteView.as_view(),
      name='password_reset_complete'
    ),

    # —– the rest of Django’s auth URLs (reset, etc.) —–
    path('', include('django.contrib.auth.urls')),

    # —– custom views —–
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]
