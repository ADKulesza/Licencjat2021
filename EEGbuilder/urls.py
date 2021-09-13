"""EEGbuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from home_menu import views as home_views
from create_dataset import views as create_dataset_views
from users import views as user_views
from files_manager import views as files_manager_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home-menu'),
    path('about/', home_views.AboutView.as_view(template_name='home_menu/about.html')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('delete_dataset/<sett_id>', user_views.delete_dataset_setting, name='delete-sett'),
    path('edit_dataset/<sett_id>', user_views.edit_dataset_setting, name='edit-sett'),
    path('edit-profile/', user_views.edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('create-dataset/', create_dataset_views.create_dataset, name='create_dataset'),
    path('download-dataset/', files_manager_views.download_dataset, name='download_dataset'),
    path('upload-dataset/', files_manager_views.upload_dataset_info, name='upload_dataset'),
    path('upload-dataset-files/',
         files_manager_views.upload_dataset_files.as_view(template_name='files_manager/upload_dataset_files.html'),
         name='upload_dataset_files'),
    path('upload-extra-files/',
         files_manager_views.UploadMetricInfo.as_view(template_name='files_manager/upload_additional_files.html'),
         name='upload_extra_files'),
    path('download-eeglab-data/<sett_id>', files_manager_views.download, name='download_data'),
    path('upload-check/', files_manager_views.upload_view, name='upload_check'),
    path('build_dataset/<sett_id>', create_dataset_views.build_dataset_view, name='build_sett'),

    path('', include('create_dataset.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
