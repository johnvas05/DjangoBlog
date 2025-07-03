from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),


    path('account/', include([
        path('', include('account.urls', namespace='account')), # Your custom account app URLs
        path('', include('django.contrib.auth.urls')),          # Django's built-in auth URLs
    ])),
]