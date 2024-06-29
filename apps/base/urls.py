from django.urls import path
from . import views


urlpatterns = [
    path('', view=views.index, name='index'),
    path('/messages', view=views.get_messages, name='messages'),
]