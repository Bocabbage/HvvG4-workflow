from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('upload/', views.upload, name = 'upload'),
    path(r'^download/(?P<filename>.+)$', views.download, name='download'),
]