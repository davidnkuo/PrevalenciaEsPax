from unittest import skip
from django.db.models.fields import NullBooleanField
from django.forms.widgets import DateTimeBaseInput
from django.http import HttpResponse, request, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from tablasPacientes.forms import *
from tablasPacientes.models import datosPaciente, datosEsPax, datosHistorial, datosEstudios
import xlwt

class homeView(): # Tiene las funciones que llaman a las pantallas de login y la principal.

### VISTA DE LA PÁGINA PRINCIPAL
    
    def login(self):
        """
            Plantilla para la pantalla de login
        """
        plantilla = get_template('log.html')
        return HttpResponse(plantilla.render())
    
    def index(request, cod_doc=''):
        """
            Plantalla para la pantalla principal, una vez que se inicia seción.
            Tiene el nombre del doctor/institución, su código, y los pacientes ingresados.
        """
        if cod_doc=='': 
            # En un primer momento, al primer login, si no hay código de doctor, lo tomo del usuario
            usuario = request.POST['usuario']
        else:
            usuario=cod_doc
        return render(request, "home.html", {
            "datosPaciente": datosPaciente.objects.all(),
            "datosEsPax": datosEsPax.objects.all(),
            "datosHistorial": datosHistorial.objects.all(),
            "datosEstudios": datosEstudios.objects.all(),
            'cod_doc': usuario
        })
    
    def index2(request, cod_pac):
        """
            Es igual a la función index, pero teniendo ya el código del doctor.
        """
        usuario = datosPaciente.objects.filter(cod_pac = cod_pac).values_list('cod_doc', flat=True).first()
        return render(request, "home.html", {
            "datosPaciente": datosPaciente.objects.all(),
            "datosEsPax": datosEsPax.objects.all(),
            "datosHistorial": datosHistorial.objects.all(),
            "datosEstudios": datosEstudios.objects.all(),
            'cod_doc': usuario
        })

class formPacienteView(HttpRequest):

### CREACIÓN DE PACIENTES

    def addpag(request, cod_doc):
        """
            Lleva a la primer pantalla para agregar datos, los datos del paciente.
        """
        paciente = FormPaciente()
        return render(request, "agregarPaciente.html", {'form':paciente, 'cod_doc':cod_doc})

    def addpag2(request, cod_doc):
        """
            Se fija que el formulario de los datos del paciente sea válido.
            Si no lo fuera, recarga la página.
            Si lo fuese, genera el código del paciente y lo guarda.
            Y devuelve la segunda página de formulario.
        """
        paciente = FormPaciente(request.POST)
        esPax = FormEsPax()
        
        if paciente.is_valid():
            post = paciente.save(commit=False)         # Dejo el form listo para guardar, pero no lo hago.

            """
            if post.nombre and post.apellido and post.dni:
                cod_pac = datosPaciente.cod_paciente(request.POST['nombre'], request.POST['apellido'], request.POST['dni'])
            else:
                post.nombre   = ""
                post.apellido = ""
                post.dni = ""
            
            if not post.cod_pac:
                try:
                    post.cod_pac = cod_pac             # Primero le guardo el código del paciente,
                except:
                    paciente = FormPaciente()
                    error = True
                    return render(request, "agregarPaciente.html", {'form': paciente, 'cod_doc':cod_doc, 'error':error})
            """

            cod_pac = post.cod_pac
            post.cod_doc = cod_doc                     # el código del doctor,
            formPacienteView.changeNullBlank(paciente)                  # cambia los NULL que hayan quedado por espacios vacíos
            paciente.save()                            # y finalmente guardo.
            paciente = FormPaciente()
            return render(request, "agregarPaciente2.html", {'form':esPax, 'cod_doc':cod_doc, 'cod_pac':cod_pac})
        paciente = FormPaciente()              # Si el formulario no es válido, borro lo completado
        error = True
        return render(request, "agregarPaciente.html", {'form': paciente, 'cod_doc':cod_doc, 'error':error})

    def addpag3(request, cod_doc, cod_pac):
        """
            Se fija que el formulario de los datos del segundo fomrulario sea válido.
            Si no lo fuera, recarga la página.
            Si lo fuese, devuelve la tercera página de formulario.
        """
        esPax = FormEsPax(request.POST)
        histo = FormHistoria()
        if esPax.is_valid():
            post = esPax.save(commit=False)    # Dejo el form listo para guardar, pero no lo hago.
            post.cod_pac_id = cod_pac          # Le guardo el código del paciente,
            formPacienteView.changeNullBlank(esPax)          # cambia los NULL que hayan quedado por espacios vacíos
            esPax.save()                       # Y después lo guardo.
            esPax = FormPaciente()
            return render(request, "agregarPaciente3.html", {'form':histo, 'cod_doc':cod_doc, 'cod_pac':cod_pac})
        esPax = FormPaciente()                 # Si el formulario no es válido, borro lo completado
        error = True
        return render(request, "agregarPaciente2.html", {'form': esPax, 'cod_doc':cod_doc, 'error':error})

    def addpag4(request, cod_doc, cod_pac):
        """
            Se fija que el formulario de los datos del tercer fomrulario sea válido.
            Si no lo fuera, recarga la página.
            Si lo fuese, se fija si hay elementos vacíos para redefinir el booleano hayVacios,
            Y devuelve la cuarta página de formulario.
        """
        histo = FormHistoria(request.POST)
        estud = FormEstudios()
        if histo.is_valid():
            # Acá se chequea si hay vacíos y se le pone el valor pertinente a la variable booleana.
            formPacienteView.buscar_vacios(histo, cod_pac)
            post = histo.save(commit=False)
            post.cod_pac_id = cod_pac
            formPacienteView.changeNullBlank(histo)                  # cambia los NULL que hayan quedado por espacios vacíos
            histo.save()
            histo = FormPaciente()
            return render(request, "agregarPaciente4.html", {'form':estud, 'cod_doc':cod_doc, 'cod_pac':cod_pac})
        histo = FormPaciente()
        error = True
        return render(request, "agregarPaciente3.html", {'form': histo, 'cod_doc':cod_doc, 'cod_pac':cod_pac, 'error':error}) 
    
    def procForm(request, cod_doc, cod_pac):
        """
            Se fija que el formulario de los datos del cuarto fomrulario sea válido.
            Si no lo fuera, recarga la página.
            Si lo fuese, procesa todo y devuelve un mensaje de que se completó correctamente.
        """
        estud = FormEstudios(request.POST)
        if estud.is_valid():
            formPacienteView.buscar_vacios(estud, cod_pac)
            post = estud.save(commit=False)
            post.cod_pac_id = cod_pac
            
            if post.HLAB27 == '1':
                post.resultHLAB27 = '1'
            elif post.HLAB27 == '2':
                post.HLAB27 = '1'
                post.resultHLAB27 = '0'
            else:
                post.HLAB27 = '1'
                post.resultHLAB27 = ''
            
            if post.RMSI == '1':
                post.cumpleSIporRMsegunASAS = '1'
            elif post.RMSI == '2':
                post.RMSI = '1'
                post.cumpleSIporRMsegunASAS = '0'
            else:
                post.RMSI = '1'
                post.cumpleSIporRMsegunASAS = ''
            
            if post.resultRadioArtSacroiliacas == '9':
                post.radioArtSacroiliacas = '0'
                post.resultRadioArtSacroiliacas = ''
            else:
                post.radioArtSacroiliacas = '1'
            
            formPacienteView.changeNullBlank(estud)                  # cambia los NULL que hayan quedado por espacios vacíos
            estud.save()
            estud = FormEstudios()

            if formPacienteView.criterio_ASAS(cod_pac): 
                esPax = datosEsPax.objects.filter(cod_pac_id = cod_pac).first()
                form_espax = FormEsPax(instance=esPax)
                form_espax = form_espax.save(commit=False)
                form_espax.cumpleCriterioASAS = '1'
                

                if formPacienteView.criterio_NY(cod_pac):
                    form_espax.cumpleCriterioEANY = '1'
                    form_espax.tipo = '2'
                
                else:
                    form_espax.tipo = '1'

                form_espax.save()
            

            return render(request, "datosGuardados.html", {'cod_doc': cod_doc})
        estud = FormEstudios()
        error = True
        return render(request, "agregarPaciente4.html", {'form': estud, 'cod_doc':cod_doc, 'cod_pac':cod_pac, 'error': error})

    def buscar_vacios(form, cod_pac):
        """
            Dado un formulario, se fija si quedaron cosas en blanco, sin completar.
            De ser así, cambia la variable hayVacios del primer form a True.
            Y devuelve la cantidad de elementos que si completaron.

            El form debe ser
        """
        contador = 0
        for elem in form:
            if elem.value() == '':
                paciente = datosPaciente.objects.filter(cod_pac = cod_pac).first()
                form = FormPaciente(instance=paciente)
                form = form.save(commit=False)
                form.hayVacios = True
                form.save()
            else:
                contador += 1
        return contador

    def criterio_NY(cod_pac):
        estud = list(datosEstudios.objects.filter(cod_pac_id = cod_pac).values())

        return (estud[0]['resultRadioArtSacroiliacas'] == '5' or estud[0]['resultRadioArtSacroiliacas'] == '7' or
                estud[0]['resultRadioArtSacroiliacas'] == '4')
    
    def criterio_ASAS(cod_pac):
        estud = list(datosEstudios.objects.filter(cod_pac_id = cod_pac).values())[0]
        histo = list(datosHistorial.objects.filter(cod_pac_id = cod_pac).values())[0]
        
        B27 = ( estud.get('resultHLAB27') == '1' )

        RM_pos = ( estud.get('cumpleSIporRMsegunASAS') == '1' )
        
        cantidad_criterios = 0

        for elem in histo:
            if histo[elem] == '1':
                cantidad_criterios += 1
        
        return ( (B27 and cantidad_criterios >= 1) or (RM_pos and cantidad_criterios >= 2) )

    def changeNullBlank(form):
        for elem in form:
            if elem.value() == None:
                elem = ''       

### EDICIÓN DE PACIENTES

    def edit(request, cod_pac):
        paciente = datosPaciente.objects.filter(cod_pac = cod_pac).first()
        form_pac = FormPaciente(instance=paciente)
        return render(request, "editarPaciente.html", {'form': form_pac, 'cod_pac':cod_pac})

    def edit2(request, cod_pac):
        paciente = datosPaciente.objects.filter(cod_pac = cod_pac).first()
        form_pac = FormPaciente(request.POST, instance = paciente)
        if form_pac.is_valid():
            formulario_pac = form_pac.save(commit=False)
            if formulario_pac.cod_pac != cod_pac: 
                esPax = datosEsPax.objects.filter(cod_pac_id = cod_pac).first()
                form_espax = FormEsPax(instance=esPax)
                formulario_espax = form_espax.save(commit=False)
                formulario_espax.cod_pac_id = formulario_pac.cod_pac
                form_espax.save()

                histo = datosHistorial.objects.filter(cod_pac_id = cod_pac).first()
                form_histo = FormHistoria(instance=histo)
                formulario_histo = form_histo.save(commit=False)
                formulario_histo.cod_pac_id = formulario_pac.cod_pac
                form_histo.save()

                estud = datosEstudios.objects.filter(cod_pac_id = cod_pac).first()
                form_estud = FormEstudios(instance=estud)
                formulario_estud = form_estud.save(commit=False)
                formulario_estud.cod_pac_id = formulario_pac.cod_pac
                form_estud.save()

            cod_pac = formulario_pac.cod_pac
            form_pac.save()
            
            esPax = datosEsPax.objects.filter(cod_pac = cod_pac).first()
            form_es_pax = FormEsPax(instance=esPax)
            return render(request, "editarPaciente2.html", {'form': form_es_pax, 'cod_pac': cod_pac})
        form_pac = FormPaciente(request.POST, instance = paciente)
        error = True
        return render(request, "editarPaciente.html", {'form': form_pac, 'cod_pac': cod_pac, 'error':error})

    def edit3(request, cod_pac):
        esPax = datosEsPax.objects.filter(cod_pac = cod_pac).first()
        form_es_pax = FormEsPax(request.POST, instance = esPax)
        if form_es_pax.is_valid():
            form_es_pax.save()
            hist = datosHistorial.objects.filter(cod_pac = cod_pac).first()
            form_hist = FormHistoria(instance=hist)
            return render(request, "editarPaciente3.html", {'form': form_hist, 'cod_pac': cod_pac})
        form_es_pax = FormEsPax(request.POST, instance = esPax)
        error = True
        return render(request, "editarPaciente2.html", {'form': form_es_pax, 'cod_pac': cod_pac, 'error':error})

    def edit4(request, cod_pac):
        hist = datosHistorial.objects.filter(cod_pac = cod_pac).first()
        form_hist = FormHistoria(request.POST, instance = hist)
        if form_hist.is_valid():
            form_hist.save()
            estud = datosEstudios.objects.filter(cod_pac = cod_pac).first()
            form_estud = FormEstudios(instance=estud)
            return render(request, "editarPaciente4.html", {'form': form_estud, 'cod_pac': cod_pac})
        form_hist = FormHistoria(request.POST, instance = hist)
        error = True
        return render(request, "editarPaciente3.html", {'form': form_hist, 'cod_pac': cod_pac, 'error':error})
        
    def actForm(request, cod_pac):
        estud = datosEstudios.objects.filter(cod_pac = cod_pac).first()
        form_estud = FormEstudios(request.POST, instance=estud)
        if form_estud.is_valid():
            form_estud.save()
            return render(request, "datosActualizados.html", {'cod_pac': cod_pac})
        form_estud = FormEstudios(request.POST, instance=estud)
        error = True
        return render(request, "agregarPaciente4.html", {'form': form_estud, 'cod_pac': cod_pac, 'error':error})

### ELIMINAR PACIENTES
    def eliminarPac(request, cod_pac, cod_doc):
        paciente = datosPaciente.objects.get(pk = cod_pac)
        esPax = datosEsPax.objects.get(cod_pac_id = cod_pac)
        histo = datosHistorial.objects.get(cod_pac_id = cod_pac)
        estud = datosEstudios.objects.get(cod_pac_id = cod_pac)
        paciente.delete()
        esPax.delete()
        histo.delete()
        estud.delete()

        return render(request, "home.html", {
            "datosPaciente": datosPaciente.objects.all(),
            "datosEsPax": datosEsPax.objects.all(),
            "datosHistorial": datosHistorial.objects.all(),
            "datosEstudios": datosEstudios.objects.all(),
            'cod_doc': cod_doc
        })


class exportDatos():

### CREACIÓN DE ARCHIVO EXCEL
  
    def exportar_excel(request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename= Ficha Prevalencia diagnóstica de EsPax en Argentina.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Datos')

        index = 0
        offset_row = 4
        offset_col = 1

        tablas = [datosPaciente, datosEsPax, datosHistorial, datosEstudios]

        for tabla in tablas:
            ws, index = exportDatos.exportar_tabla(tabla, ws, index, offset_row, offset_col)
            offset_row = 2
            offset_col = 2
            

        """
            OTRA FORMA, TABLA POR TABLA

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            ws, index = exportDatos.exportar_tabla_1(ws, font_style, index)
            ws, index = exportDatos.exportar_tabla_2(ws, font_style, index)
            ws, index = exportDatos.exportar_tabla_3(ws, font_style, index)
            ws, index = exportDatos.exportar_tabla_4(ws, font_style, index)

        """

        wb.save(response)

        return response   

    def exportar_tabla(tabla, ws, index, offset_row, offset_col):
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        fields = tabla._meta.get_fields()
        columns = [field.get_attname_column()[1] for field in fields[offset_row:]]
        row_num = 0

        for col_num in range(len(columns)):
            ws.write(row_num, col_num+index, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = tabla.objects.values_list()
        
        for row in rows:
            row_num += 1

            if type(row) == str:
                try:
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num+index, int(str(row[col_num+offset_col])), font_style)
                except:
                    for col_num in range(len(columns)):
                        ws.write(row_num, col_num+index, str(row[col_num+offset_col]), font_style)
            
            else:
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num+index, row[col_num+offset_col], font_style)

        return(ws, index + len(columns))

"""
        
        def exportar_tabla_1(ws, font_style, index):
            fields = datosPaciente._meta.get_fields()
            columns = [field.get_attname_column()[1] for field in fields[3:]]
            row_num = 0

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            font_style = xlwt.XFStyle()

            rows = datosPaciente.objects.values_list()
            
            for row in rows:
                row_num += 1

                for col_num in range(index, len(columns)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)

            return(ws, index + len(columns))

        def exportar_tabla_2(ws, font_style, index):
            fields = datosEsPax._meta.get_fields()
            columns = [field.get_attname_column()[1] for field in fields[2:]]
            row_num = 0

            for col_num in range(len(columns)):
                ws.write(row_num, col_num+index, columns[col_num], font_style)

            font_style = xlwt.XFStyle()

            rows = datosEsPax.objects.values_list()
            
            for row in rows:
                row_num += 1

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num+index, str(row[col_num+2]), font_style)

            return(ws, index + len(columns))
            
        def exportar_tabla_3(ws, font_style, index):
            fields = datosHistorial._meta.get_fields()
            columns = [field.get_attname_column()[1] for field in fields[2:]]
            row_num = 0

            for col_num in range(len(columns)):
                ws.write(row_num, col_num+index, columns[col_num], font_style)

            font_style = xlwt.XFStyle()

            rows = datosHistorial.objects.values_list()
            
            for row in rows:
                row_num += 1

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num+index, str(row[col_num+2]), font_style)

            return(ws, index + len(columns))

        def exportar_tabla_4(ws, font_style, index):
            fields = datosEstudios._meta.get_fields()
            columns = [field.get_attname_column()[1] for field in fields[2:]]
            row_num = 0

            for col_num in range(len(columns)):
                ws.write(row_num, col_num+index, columns[col_num], font_style)

            font_style = xlwt.XFStyle()

            rows = datosEstudios.objects.values_list()
            
            for row in rows:
                row_num += 1

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num+index, str(row[col_num+2]), font_style)    

            return(ws, index + len(columns)) 
        
"""

#class autiamizacionCampos():
    # Según lo que complete, se decide si cumple los criterios los criterios y el tipo

    # Criterio ASAS







    
