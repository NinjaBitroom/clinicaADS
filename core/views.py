from io import BytesIO

from django.db.models import Model
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, ListView
from xhtml2pdf import pisa

from core.models import Paciente, Possui, Consulta


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


class RelatPdfPacientes(PDFView):
    template_name = 'relatorios/pdfpacientes.html'
    model = Paciente
    context_object_name = 'pacientes'


# Crie os relatórios abaixo relacionados em pdf, utilizando a biblioteca xhtml2pdf.
# Deve haver links para geração dos relatórios.
# Os relatórios são os seguintes:
# 1 - Relatório nomes e idades de pacientes por convênio.


class RelatPdfPacientesConvenio(PDFView):
    template_name = 'relatorios/pdfpacientesconvenio.html'
    model = Possui
    context_object_name = 'paconvs'

    def get(self, request):
        objects = self.model.objects.all()
        my_dict = {}
        for paconv in objects:
            my_dict[paconv.convenio.nome] = {}
        for paconv in objects:
            my_dict[paconv.convenio.nome][paconv.paciente.nome] = paconv.paciente.idade
        data = {self.context_object_name: my_dict}
        template = get_template(self.template_name)
        html = template.render(data)
        result = BytesIO()
        try:
            pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
            return None


# 2- Relatório de consultas por especialidade e por mês.


class RelatPdfConsultasEspecialidade(PDFView):
    template_name = 'relatorios/pdfconsultasespecialidade.html'
    model = Consulta
    context_object_name = 'consultas'

    def get(self, request):
        objects = self.model.objects.all()
        my_list = [(i.data.month, i.medico.especialidade) for i in objects]
        data = {self.context_object_name: my_list}
        template = get_template(self.template_name)
        html = template.render(data)
        result = BytesIO()
        try:
            pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
            return None


# 3- Relatório de quantidade de pacientes atendidos por especialidade e por mês.


class RelatPdfPacientesEspecialidade(PDFView):
    template_name = 'relatorios/pdfpacientesespecialidade.html'
    model = Consulta
    context_object_name = 'consultas'

    def get(self, request):
        objects = self.model.objects.all()
        my_dict = {}
        for consulta in objects:
            my_dict[(consulta.data.month, consulta.medico.especialidade)] = 0
        for consulta in objects:
            my_dict[(consulta.data.month, consulta.medico.especialidade)] += 1
        data = {self.context_object_name: my_dict}
        template = get_template(self.template_name)
        html = template.render(data)
        result = BytesIO()
        try:
            pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
            return None
