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
from rest_framework_nested import routers

from gestfg.views import IndexView, DashboardView
from authentication.views import AlumnosViewSet, LoginView, LogoutView, ProfesoresViewSet, PermissionsView, \
    UsuariosViewSet
from tfgs.views import Tfg_asigView, TfgViewSet
from eventos.views import EventosViewSet
from upload_files.views import Upload_fileView

router = routers.SimpleRouter()
router.register(r'alumnos', AlumnosViewSet)
router.register(r'profesores', ProfesoresViewSet)
router.register(r'usuarios', UsuariosViewSet)
router.register(r'tfgs', TfgViewSet)
router.register(r'events', EventosViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/auth/permisos/$', PermissionsView.as_view(), name='permisos'),
    url(r'^api/v1/tfgs_asig/$', Tfg_asigView.as_view(), name='tfg_asig'),
    url(r'^api/v1/upload_file_tfgs/$', Upload_fileView.as_view(), name='upload_file_tfgs'),
    # url(r'^alumnos/$', authentication_views.AlumnosViewSet.alumnos, name='alumnos'),
    # url(r'^logueo/$', login.login, name='login'),
    # url(r'^alumnos/update_alumno/$', alumnos.update_alumno, name='update_alumno'),
    # url(r'^alumnos/delete_alumno/$', alumnos.delete_alumno, name='delete_alumno'),
    # url(r'^profesores/$', profesores.profesores, name='profesores'),
    # url(r'^profesores/update_profesor/$', profesores.update_profesor, name='update_profesor'),
    # url(r'^profesores/delete_profesor/$', profesores.delete_profesor, name='delete_profesor'),
    # url(r'^tfgs/$', views_tfg.tfgs, name='tfg'),
    # url(r'^tfgs/update_tfg/$', views_tfg.update_tfg, name='update_tfg'),
    # url(r'^tfgs/delete_tfg/$', views_tfg.delete_tfg, name='delete_tfg'),
    # url(r'^asig_tfg/$', views_tfg.asig_tfg, name='asig_tfg'),
    # url(r'^asig_tfg/remove/$', views_tfg.remove_asig_tfg, name='remove_asig_tfg'),
    url('^dashboard.*', DashboardView.as_view(), name='dashboard'),
    url('^/?$', IndexView.as_view(), name='index'),
]
