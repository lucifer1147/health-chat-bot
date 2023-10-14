from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('<int:step>', views.home, name='form'),
    path('<str:instance>/', views.instance, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:instance>/', views.getMessages, name='getMessages'),
]
