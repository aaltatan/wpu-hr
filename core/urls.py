from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
    # apps
    path('', include('apps.base.urls')),
    path('faculties/', include('apps.faculties.urls')),
    path('specialties/', include('apps.specialties.urls')),
    path('staff/', include('apps.staff.urls')),
] + debug_toolbar_urls()
