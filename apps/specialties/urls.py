from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='specialties-index'),
    path('add/', view=views.add_specialty, name='add-specialty'),
    path('delete/<int:id>/', view=views.delete_specialty, name='delete-specialty'),
    path('update/<int:id>/', view=views.update_specialty, name='update-specialty'),
    path('get-add-form/', view=views.get_add_form, name='get-add-specialty-form'),
    path('get-update-form/<int:id>/', view=views.get_update_form, name='get-update-specialty-form'),
]