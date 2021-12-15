from django import forms
from django.forms import widgets
import tablasPacientes.models as tabs
from django.utils.translation import gettext_lazy as _

class FormPaciente(forms.ModelForm):
    class Meta:
        model = tabs.datosPaciente
        exclude = ('cod_doc', 'cod_pac')
        labels = {'cod_pac': _('Código del Paciente'), 'fechaDeRegistro': _('Fecha Actual'),
                'dni': _('D.N.I'), 'fechaDeNacimiento': _('Fecha de Nacimiento'), 'estadoCivil': _('Estado Civil'),
                'idProvincia': _('Provincia'), 'idArea': _('Area')}
        widgets = {'fechaDeNacimiento': forms.DateInput(attrs={'type': 'date'}),
                    'fechaDeRegistro': forms.DateInput(attrs={'type': 'date'})}

class FormEsPax(forms.ModelForm):
    class Meta:
        model = tabs.datosEsPax
        exclude = ('cod_pac',)
        labels = {'anioInicioEsPax': _('Año de Inicio de Síntomas'), 'anioDiagnostico': _('Año de Diagnóstico'),
                'cumpleCriterioASAS': _('Cumple criterios EsPax ASAS 2009'), 'cumpleCriterioEANY': _('Cumple criterios EA New York m'),
                'subTipo': _('Subtipo')}

class FormHistoria(forms.ModelForm):
    class Meta:
        model = tabs.datosHistorial
        exclude = ('cod_pac',)
        labels = {'artitrisPeriferica': _('Artritis periférica'), 'eii': _('Enfermedad inflamatoria intestinal (EII)'),
                'uveitis': _('Uveítis'), 'buenaRespAINE': _('Buena respuesta a AINEs'),
                'hisFamConEsP': _('Historia familiar de Espondiloartritis (EsP)'), 'portCReactiva': _('Proteína C reactiva (PCR) elevada')}

class FormEstudios(forms.ModelForm):
    class Meta:
        model = tabs.datosEstudios
        exclude = ('cod_pac',)
        labels = {'resultHLAB27': _('Resultado HLA-B27'), 'radioArtSacroiliacas': _('Radiografía de articulaciones sacroilíacas (SI)'),
                'resultRadioArtSacroiliacas': _('Resultado radiografías sacroilíacas'), 'cumpleSIporRMsegunASAS': _('Cumple SI por RM según criterios ASAS')}

