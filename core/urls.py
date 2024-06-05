from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()


from apps.base import views as base_views
from apps.staff import views as staff_views

router.register('faculties', base_views.FacultyViewSet)
router.register('staff', staff_views.StaffViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('', include('apps.base.urls')),
]
