"""paginaPrincipal URL Configuration

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
from django.contrib import admin
from django.urls import path
from paginaPrincipal.views import homeView, formPacienteView, exportDatos
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', homeView.login, name='login'),
    path('', views.LoginView.as_view(template_name='log.html'), name='login'),
    path('home/', homeView.index, name='home'),
    path('home2/<str:cod_doc>', homeView.index, name='home2'),
    path('home3/<str:cod_pac>', homeView.index2, name='home3'),
    path('registrarPaciente/<str:cod_doc>', formPacienteView.addpag, name='agregarPaciente'),
    path('registrarPaciente2/<str:cod_doc>', formPacienteView.addpag2, name='agregarPaciente2'),
    path('registrarPaciente3/<str:cod_doc>/<str:cod_pac>', formPacienteView.addpag3, name='agregarPaciente3'),
    path('registrarPaciente4/<str:cod_doc>/<str:cod_pac>', formPacienteView.addpag4, name='agregarPaciente4'),
    path('pacienteGuardado/<str:cod_doc>/<str:cod_pac>', formPacienteView.procForm, name='pacienteGuardado'),
    path('editarPaciente/<str:cod_pac>', formPacienteView.edit, name='editarPaciente'),
    path('editarPaciente2/<str:cod_pac>', formPacienteView.edit2, name='editarPaciente2'),
    path('editarPaciente3/<str:cod_pac>', formPacienteView.edit3, name='editarPaciente3'),
    path('editarPaciente4/<str:cod_pac>', formPacienteView.edit4, name='editarPaciente4'),
    path('pacienteActualizado/<str:cod_pac>', formPacienteView.actForm, name='pacienteActualizado'),
    path('descargarDatosExcel/', exportDatos.exportar_excel, name='descargar_excel'),
    path('eliminar/<str:cod_pac>/<str:cod_doc>', formPacienteView.eliminarPac, name='eliminar'),
]
