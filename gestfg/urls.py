"""gestfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from controller.ws import alumnos, profesores, upload_file_tfgs, login
from gestion_tfgs import views as views_tfg

urlpatterns = [
    url(r'^', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^alumnos/$', alumnos.alumnos, name='alumnos'),
    url(r'^logueo/$', login.login, name='login'),
    url(r'^alumnos/update_alumno/$', alumnos.update_alumno, name='update_alumno'),
    url(r'^alumnos/delete_alumno/$', alumnos.delete_alumno, name='delete_alumno'),
    url(r'^profesores/$', profesores.profesores, name='profesores'),
    url(r'^profesores/update_profesor/$', profesores.update_profesor, name='update_profesor'),
    url(r'^profesores/delete_profesor/$', profesores.delete_profesor, name='delete_profesor'),
    url(r'^tfgs/$', views_tfg.tfgs, name='tfg'),
    url(r'^tfgs/update_tfg/$', views_tfg.update_tfg, name='update_tfg'),
    url(r'^tfgs/delete_tfg/$', views_tfg.delete_tfg, name='delete_tfg'),
    url(r'^asig_tfg/$', views_tfg.asig_tfg, name='asig_tfg'),
    url(r'^asig_tfg/remove/$', views_tfg.remove_asig_tfg, name='remove_asig_tfg'),
    url(r'^upload_file_tfgs/$', upload_file_tfgs.upload_file, name='upload_file_tfgs'),
]
