from django import forms
from django.forms import widgets
import tablasPacientes.models as tabs
from django.utils.translation import gettext_lazy as _

class FormPaciente(forms.ModelForm):
    class Meta:
        model = tabs.datosPaciente
        exclude = ('cod_doc', 'hayVacios')
        labels = {'cod_pac': _('Código del Paciente'), 'apellidoYNombre': _('Apellido y Nombre'), 'fechaDeRegistro': _('Fecha Actual'),
                'dni': _('D.N.I'), 'fechaDeNacimiento': _('Fecha de Nacimiento'), 'estadoCivil': _('Estado Civil'),
                'idProvincia': _('Provincia'), 'idArea': _('Area')}
        widgets = {'fechaDeNacimiento': forms.DateInput(attrs={'type': 'date'}),
                    'fechaDeRegistro': forms.DateInput(attrs={'type': 'date'})}

class FormEsPax(forms.ModelForm):
    class Meta:
        model = tabs.datosEsPax
        exclude = ('cod_pac', 'cumpleCriterioASAS', 'cumpleCriterioEANY', 'tipo')
        labels = {'anioInicioEsPax': _('Año de Inicio de Síntomas'), 'anioDiagnostico': _('Año de Diagnóstico'), 'subTipo': _('Subtipo')}

class FormHistoria(forms.ModelForm):
    class Meta:
        model = tabs.datosHistorial
        exclude = ('cod_pac',)
        labels = {'artitrisPeriferica': _('Artritis periférica'), 'eii': _('Enfermedad inflamatoria intestinal (EII)'),
                'uveitis': _('Uveítis'), 'buenaRespAINE': _('Buena respuesta a AINEs'),
                'hisFamConEsP': _('Historia familiar de Espondiloartritis (EsP)'), 'portCReactiva': _('Proteína C reactiva (PCR) elevada'),
                'dolorLumbInflam': _('Dolor Lumbar Inflamatorio')}

class FormEstudios(forms.ModelForm):
    class Meta:
        model = tabs.datosEstudios
        exclude = ('cod_pac', 'resultHLAB27', 'cumpleSIporRMsegunASAS', 'radioArtSacroiliacas')
        labels = {'resultHLAB27': _('Resultado HLA-B27'), 'radioArtSacroiliacas': _('Radiografía de articulaciones sacroilíacas (SI)'),
                'resultRadioArtSacroiliacas': _('Resultado radiografías sacroilíacas'), 'cumpleSIporRMsegunASAS': _('Cumple SI por RM según criterios ASAS')}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance.HLAB27 == 0:
                self.fields['resultHLAB27'].widget.attrs.update({'disabled': True})
            
            if self.instance.radioArtSacroiliacas == 0:
                self.fields['resultRadioArtSacroiliacas'].widget.attrs.update({'disabled': True})
            
            if self.instance.RMSI == 0:
                self.fields['cumpleSIporRMsegunASAS'].widget.attrs.update({'disabled': True})

