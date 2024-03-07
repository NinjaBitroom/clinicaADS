from io import BytesIO

from django.db.models import Model
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, ListView
from xhtml2pdf import pisa

from core.models import Paciente, Medico


class PDFView(View):
    template_name: str
    model: Model
    context_object_name: str

    def get(self, request):
        objects = self.model.objects.all()
        data = {
            self.context_object_name: objects
        }
        template = get_template(self.template_name)
        html = template.render(data)
        result = BytesIO()
        try:
            pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
            return None


class HomeTemplateView(TemplateView):
    template_name = 'index.html'


class PacientesListView(ListView):
    template_name = 'relatorios/pacientes.html'
    model = Paciente
    context_object_name = 'pacientes'


# class RelatPdfPacientes(View):
#     def get(self, request):
#         pacientes = Paciente.objects.all()
#         data = {
#             'pacientes': pacientes,
#         }
#         template = get_template('relatorios/pdfpacientes.html')
#         html = template.render(data)
#         result = BytesIO()
#         try:
#             pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
#             return HttpResponse(result.getvalue(), content_type='application/pdf')
#         except Exception as e:
#             print(e)
#             return None


class RelatPdfPacientes(PDFView):
    template_name = 'relatorios/pdfpacientes.html'
    model = Paciente
    context_object_name = 'pacientes'


class RelatPdfMedicos(PDFView):
    template_name = 'relatorios/pdfmedicos.html'
    model = Medico
    context_object_name = 'medicos'
