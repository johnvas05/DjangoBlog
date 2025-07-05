# myblog/account/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's auth views
from . import views # Import your custom views from myblog/account/views.py

app_name = 'account' # Define namespace for account app

urlpatterns = [
    # Custom Dashboard (e.g., http://127.0.0.1:8000/account/)
    path('', views.dashboard, name='dashboard'),

    # Explicit Logout (e.g., http://127.0.0.1:8000/account/logout/)
    # This renders 'registration/logged_out.html' after a successful POST request
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path("register/", views.register, name="register"),

]
