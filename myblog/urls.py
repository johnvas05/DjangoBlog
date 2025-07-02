from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')), # Add this line for your account app
    path('blog/', include('blog.urls', namespace='blog')),
]