from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='faculties-index'),
    path('add/', view=views.add_faculty, name='add-faculty'),
    path('delete/<int:id>/', view=views.delete_faculty, name='delete-faculty'),
    path('update/<int:id>/', view=views.update_faculty, name='update-faculty'),
    path('get-add-form/', view=views.get_add_form, name='get-add-form'),
    path('get-update-form/<int:id>/', view=views.get_update_form, name='get-update-form'),
]