from django.urls import path
from . import views

urlpatterns = [
    path('', views.search),
    path('search', views.search),
    path('books/', views.by_book),
    path('read', views.read),
    path('about', views.about)
]
