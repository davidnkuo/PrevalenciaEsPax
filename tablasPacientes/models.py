from django.db import models
from .choices import * 

# Create your models here.
class datosPaciente(models.Model):
    hayVacios = models.BooleanField(default=False)
    cod_pac = models.CharField(primary_key=True, max_length=64, help_text="Primera letra del nombre + primera letra del apellido + últimos 3 dígitos del dni.")
    cod_doc = models.CharField(max_length=64)
    apellidoYNombre = models.CharField(max_length=64, blank=True, help_text="Apellido y nombre del paciente. No es obligatorio")
    fechaDeRegistro = models.CharField(max_length=64)
    dni = models.CharField(blank=True, max_length=9)
    nacionalidad = models.CharField(max_length=64)
    fechaDeNacimiento = models.CharField(max_length=64)
    sexo = models.IntegerField(choices=SEXO)
    estadoCivil = models.IntegerField(choices=ESTADO_CIVIL)
    escolaridad = models.IntegerField()
    idProvincia = models.IntegerField(choices=PROVINCIAS)
    idArea = models.IntegerField(choices=AREA)
    etnia = models.IntegerField(choices=ETNIA)

    @classmethod

    def cod_paciente(cod_pac, nombre, apellido, dni):
        cod_pac = f"{nombre[0]}{apellido[0]}{dni[-3:]}"

        return cod_pac

    def cod_doctor(cod_doc):
        cod_doctor = cod_doc
        return cod_doc

    def consulta_cod_doc(self):
        return self.cod_doc

    def __str__(self):
        return f"{self.cod_pac}" 


class datosEsPax(models.Model):
    cod_pac = models.ForeignKey(datosPaciente, on_delete=models.CASCADE)
    anioInicioEsPax = models.IntegerField()
    anioDiagnostico = models.IntegerField()
    cumpleCriterioASAS = models.CharField(choices=CUMPLE_CRITERIO, max_length=10, blank=True, default='')
    cumpleCriterioEANY = models.CharField(choices=CUMPLE_CRITERIO, max_length=10, blank=True, default='')
    subTipo = models.IntegerField(choices=SUBTIPO)
    tipo = models.CharField(choices=TIPO, max_length=10, blank=True, default='')

class datosHistorial(models.Model):
    cod_pac = models.ForeignKey(datosPaciente, on_delete=models.CASCADE, blank=True, null=True)
    artitrisPeriferica = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    entesitis = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    dactilitis = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    Psoriasis = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    eii = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    uveitis = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    buenaRespAINE = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    hisFamConEsP = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    portCReactiva = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)
    dolorLumbInflam = models.CharField(choices=CUMPLE_CRITERIO, blank=True, default='', max_length=10)

class datosEstudios(models.Model):
    cod_pac = models.ForeignKey(datosPaciente, on_delete=models.CASCADE)
    HLAB27 = models.CharField(choices=ESTUD_Y_RESULT, blank=True, default='', max_length=10)
    resultHLAB27 = models.CharField(choices=CRITERIO_POS_NEG_BLANK, blank=True, default='', max_length=10)
    radioArtSacroiliacas = models.CharField(choices=RESULT_RADIOGRAFIA, blank=True, default='', max_length=10)
    resultRadioArtSacroiliacas = models.CharField(choices=RESULT_RADIOGRAFIA, blank=True, default='', max_length=10)
    RMSI = models.CharField(choices=ESTUD_Y_RESULT, blank=True, default='', max_length=10)
    cumpleSIporRMsegunASAS = models.CharField(choices=CRITERIO_POS_NEG_BLANK, blank=True, default='', max_length=10)