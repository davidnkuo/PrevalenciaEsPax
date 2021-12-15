from django.shortcuts import render

from tablasPacientes.forms import FormPaciente
from .models import datosPaciente, datosEsPax, datosHistorial, datosEstudios
from django.http import HttpRequest
