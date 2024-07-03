from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.base.urls')),
    path('faculties/', include('apps.faculties.urls')),
    path('faculties-supporters/', include('apps.faculties_supporters.urls')),
    path('staff/', include('apps.staff.urls')),
]
