from django.urls import path, include # Make sure 'include' is imported
from . import views # You might add custom views later, but for now, we're mostly including Django's auth views

app_name = 'account' # It's a good practice to define an app_name for namespacing

urlpatterns = [
    # Django authentication URLs
    path("", include("django.contrib.auth.urls")),
]