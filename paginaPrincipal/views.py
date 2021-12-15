from django.forms.widgets import DateTimeBaseInput
from django.http import HttpResponse, request, HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from tablasPacientes.forms import *
from tablasPacientes.models import datosPaciente, datosEsPax, datosHistorial, datosEstudios
import xlwt

class homeView():

### VISTA DE LA PÁGINA PRINCIPAL
    
    def login(self):
        plantilla = get_template('log.html')
        return HttpResponse(plantilla.render())
    
    def index(request, cod_doc=''):
        if cod_doc=='':
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
        paciente = FormPaciente()
        return render(request, "agregarPaciente.html", {'form':paciente, 'cod_doc':cod_doc})

    def addpag2(request, cod_doc):
        paciente = FormPaciente(request.POST)
        esPax = FormEsPax()
        cod_pac = datosPaciente.cod_paciente(request.POST['nombre'], request.POST['apellido'], request.POST['dni'])
        #cod_doc = datosPaciente.cod_doctor(cod_doc)
        if paciente.is_valid():
            post = paciente.save(commit=False)
            post.cod_pac = cod_pac
            post.cod_doc = cod_doc
            paciente.save()
            paciente = FormPaciente()
            return render(request, "agregarPaciente2.html", {'form':esPax, 'cod_doc':cod_doc, 'cod_pac':cod_pac})
        paciente = FormPaciente()
        return render(request, "agregarPaciente.html", {'form': paciente, 'cod_doc':cod_doc})

    def addpag3(request, cod_doc, cod_pac):
        esPax = FormEsPax(request.POST)
        histo = FormHistoria()
        if esPax.is_valid():
            post = esPax.save(commit=False)
            post.cod_pac_id = cod_pac
            esPax.save()
            esPax = FormPaciente()
            return render(request, "agregarPaciente3.html", {'form':histo, 'cod_doc':cod_doc, 'cod_pac':cod_pac})
        esPax = FormPaciente()
        return render(request, "agregarPaciente2.html", {'form': esPax, 'cod_doc':cod_doc})

    def addpag4(request, cod_doc, cod_pac):
        histo = FormHistoria(request.POST)
        estud = FormEstudios()
        if histo.is_valid():
            post = histo.save(commit=False)
            post.cod_pac_id = cod_pac
            histo.save()
            histo = FormPaciente()
            return render(request, "agregarPaciente4.html", {'form':estud, 'cod_doc':cod_doc, 'cod_pac':cod_pac})
        histo = FormPaciente()
        return render(request, "agregarPaciente3.html", {'form': histo, 'cod_doc':cod_doc, 'cod_pac':cod_pac}) 
    
    def procForm(request, cod_doc, cod_pac):
        estud = FormEstudios(request.POST)
        if estud.is_valid():
            post = estud.save(commit=False)
            post.cod_pac_id = cod_pac
            estud.save()
            estud = FormEstudios()
            return render(request, "datosGuardados.html", {'cod_doc': cod_doc})
        estud = FormEstudios()
        return render(request, "agregarPaciente4.html", {'form': estud, 'cod_doc':cod_doc, 'cod_pac':cod_pac})


### EDICIÓN DE PACIENTES

    def edit(request, cod_pac):
        paciente = datosPaciente.objects.filter(cod_pac = cod_pac).first()
        form_pac = FormPaciente(instance=paciente)
        return render(request, "editarPaciente.html", {'form': form_pac, 'cod_pac':cod_pac})

    def edit2(request, cod_pac):
        paciente = datosPaciente.objects.filter(cod_pac = cod_pac).first()
        form_pac = FormPaciente(request.POST, instance = paciente)
        if form_pac.is_valid():
            form_pac.save()
            esPax = datosEsPax.objects.filter(cod_pac = cod_pac).first()
            form_es_pax = FormEsPax(instance=esPax)
            return render(request, "editarPaciente2.html", {'form': form_es_pax, 'cod_pac': cod_pac})
        return render(request, "editarPaciente.html", {'form': form_pac, 'cod_pac': cod_pac})

    def edit3(request, cod_pac):
        esPax = datosEsPax.objects.filter(cod_pac = cod_pac).first()
        form_es_pax = FormEsPax(request.POST, instance = esPax)
        if form_es_pax.is_valid():
            form_es_pax.save()
            hist = datosHistorial.objects.filter(cod_pac = cod_pac).first()
            form_hist = FormHistoria(instance=hist)
            return render(request, "editarPaciente3.html", {'form': form_hist, 'cod_pac': cod_pac})
        return render(request, "editarPaciente2.html", {'form': form_es_pax, 'cod_pac': cod_pac})

    def edit4(request, cod_pac):
        hist = datosHistorial.objects.filter(cod_pac = cod_pac).first()
        form_hist = FormHistoria(request.POST, instance = hist)
        if form_hist.is_valid():
            form_hist.save()
            estud = datosEstudios.objects.filter(cod_pac = cod_pac).first()
            form_estud = FormEstudios(instance=estud)
            return render(request, "editarPaciente4.html", {'form': form_estud, 'cod_pac': cod_pac})
        return render(request, "editarPaciente3.html", {'form': form_hist, 'cod_pac': cod_pac})
        
    def actForm(request, cod_pac):
        estud = datosEstudios.objects.filter(cod_pac = cod_pac).first()
        form_estud = FormEstudios(request.POST, instance=estud)
        if form_estud.is_valid():
            form_estud.save()
            return render(request, "datosActualizados.html", {'cod_pac': cod_pac})
        return render(request, "agregarPaciente4.html", {'form': form_estud, 'cod_pac': cod_pac})

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
        offset_row = 3
        offset_col = 0

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

            for col_num in range(len(columns)):
                ws.write(row_num, col_num+index, str(row[col_num+offset_col]), font_style)

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
