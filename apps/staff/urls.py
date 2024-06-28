from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='staff-index'),
    path('add/', view=views.add_staff, name='add-staff'),
    path('get-add-form/', view=views.get_add_form, name='get-add-staff-form'),
    path('update/<int:id>/', view=views.update_staff, name='update-staff'),
    path('toggle-countable/<int:id>/', view=views.toggle_countable, name='toggle-countable-staff'),
    path('get-update-form/<int:id>/', view=views.get_update_form, name='get-update-staff-form'),
    path('delete/<int:id>/', view=views.delete_staff, name='delete-staff'),
]