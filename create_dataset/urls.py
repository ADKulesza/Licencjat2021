from django.urls import path
from .views import create_dataset_page1, create_dataset_page3, create_dataset_page2, confirm_dataset
from . import views

urlpatterns = [
    path('', views.create_dataset, name='create-dataset'),
    path('create-dataset/page1/', create_dataset_page1,
         name='create-dataset-page1'),
    path('create-dataset/page2/', create_dataset_page2,
         name='create-dataset-page2'),
    path('create-dataset/page3/', create_dataset_page3,
         name='create-dataset-page3'),
    path('create-dataset/confirm-dataset/', confirm_dataset,
         name='confirm_dataset'),
]