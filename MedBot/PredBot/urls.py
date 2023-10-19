from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('<int:step>', views.home, name='form'),
]
