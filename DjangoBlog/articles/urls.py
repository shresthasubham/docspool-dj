"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf.urls import url
from django.urls import path
from .import views


app_name = 'article'
urlpatterns = [
    path('create/<str:type>',views.article_create,name='create'),
    path('',views.article_list,name='list'),
    path('export-pdf/<str:export_Format>', views.create_pdf , name="export-pdf"),
    path('export-excel', views.create_excelSheet , name="export-excel"),
    path('export-bibtex', views.create_BibtexSheet , name="export-bibtex"),
    path('bibtexUpload',views.bibtexPopulator, name='bibtex-upload'),
    path('profile',views.ProfilePage, name='profile'),
    path('<str:type>/<str:slug>/edit',views.EditArticle, name="edit-data"),
    path('<str:type>/<str:slug>/delete',views.DeleteArticle, name="delete-data"),
    path('<str:type>/<str:slug>/update',views.UpdateArticle, name = "update_data"),
    url('showArticle/(?P<slug>[\w-]+)',views.article_detail,name='detail'), 
    #name catching block in the url
   
]
