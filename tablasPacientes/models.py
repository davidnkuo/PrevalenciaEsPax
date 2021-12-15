from django.db import models
from .choices import * 

# Create your models here.
class datosPaciente(models.Model):
    cod_pac = models.CharField(primary_key=True, max_length=64)
    cod_doc = models.CharField(max_length=64)
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    fechaDeRegistro = models.CharField(max_length=64)
    dni = models.IntegerField()
    nacionalidad = models.CharField(max_length=64)
    fechaDeNacimiento = models.CharField(max_length=64)
    sexo = models.CharField(max_length=64, choices=SEXO)
    estadoCivil = models.CharField(max_length=64, choices=ESTADO_CIVIL)
    escolaridad = models.IntegerField()
    idProvincia = models.CharField(max_length=64, choices=PROVINCIAS)
    idArea = models.CharField(max_length=64, choices=AREA)
    etnia = models.CharField(max_length=64, choices=ETNIA)

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
    cumpleCriterioASAS = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    cumpleCriterioEANY = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    subTipo = models.CharField(max_length=64, choices=SUBTIPO)
    tipo = models.CharField(max_length=64, choices=TIPO)

class datosHistorial(models.Model):
    cod_pac = models.ForeignKey(datosPaciente, on_delete=models.CASCADE)
    artitrisPeriferica = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    entesitis = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    dactilitis = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    Psoriasis = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    eii = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    uveitis = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    buenaRespAINE = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    hisFamConEsP = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    portCReactiva = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)

class datosEstudios(models.Model):
    cod_pac = models.ForeignKey(datosPaciente, on_delete=models.CASCADE)
    HLAB27 = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    resultHLAB27 = models.CharField(max_length=64, choices=CRITERIO_POS_NEG_BLANK)
    radioArtSacroiliacas = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    resultRadioArtSacroiliacas = models.CharField(max_length=64, choices=CRITERIO_POS_NEG_BLANK)
    RMSI = models.CharField(max_length=64, choices=CUMPLE_CRITERIO)
    cumpleSIporRMsegunASAS = models.CharField(max_length=64, choices=CRITERIO_POS_NEG_BLANK)