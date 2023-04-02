from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/', include('users.urls')),
    path('api/', include('api.urls')),
]
