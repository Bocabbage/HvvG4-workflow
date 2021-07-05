from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('upload/', views.upload, name = 'upload'),
    path('download/', views.download, name='download'),
    path('result_file_download/<int:random_num>', views.result_file_download, name='result_file_download')
]
