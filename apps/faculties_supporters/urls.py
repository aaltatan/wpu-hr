from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='supporters-index'),
    path('add/', view=views.add_supporter, name='add-supporter'),
    path('delete/<int:id>/', view=views.delete_supporter, name='delete-supporter'),
    path('update/<int:id>/', view=views.update_supporter, name='update-supporter'),
    path('get-add-form/', view=views.get_add_form, name='get-add-form'),
    path('get-update-form/<int:id>/', view=views.get_update_form, name='get-update-form'),
]