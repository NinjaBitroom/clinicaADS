import base64
from io import BytesIO

from django.db.models import Model
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, ListView
from matplotlib import pyplot
from xhtml2pdf import pisa

from core.models import Paciente, Possui, Consulta, Convenio

_MES = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}


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


class PacientesConvenioView(TemplateView):
    template_name = 'relatorios/pacientesconvenio.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        possui = Possui.objects.all()
        my_dict = {}
        for paconv in possui:
            my_dict[paconv.convenio.nome] = {}
        for paconv in possui:
            my_dict[paconv.convenio.nome][paconv.paciente.nome] = paconv.paciente.idade
        contexto['paconvs'] = my_dict
        return contexto


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


class ConsultasEspecialidadeView(TemplateView):
    template_name = 'relatorios/consultasespecialidade.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        consultas = Consulta.objects.all()
        my_list = [(_MES[i.data.month], i.medico.especialidade) for i in consultas]
        contexto['consultas'] = my_list
        return contexto


class RelatPdfConsultasEspecialidade(PDFView):
    template_name = 'relatorios/pdfconsultasespecialidade.html'
    model = Consulta
    context_object_name = 'consultas'

    def get(self, request):
        objects = self.model.objects.all()
        my_list = [(_MES[i.data.month], i.medico.especialidade) for i in objects]
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


class PacientesEspecialidadeView(TemplateView):
    template_name = 'relatorios/pacientesespecialidade.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        consultas = Consulta.objects.all()
        my_dict = {}
        for consulta in consultas:
            my_dict[(_MES[consulta.data.month], consulta.medico.especialidade)] = 0
        for consulta in consultas:
            my_dict[(_MES[consulta.data.month], consulta.medico.especialidade)] += 1
        contexto['consultas'] = my_dict
        return contexto


class RelatPdfPacientesEspecialidade(PDFView):
    template_name = 'relatorios/pdfpacientesespecialidade.html'
    model = Consulta
    context_object_name = 'consultas'

    def get(self, request):
        objects = self.model.objects.all()
        my_dict = {}
        for consulta in objects:
            my_dict[(_MES[consulta.data.month], consulta.medico.especialidade)] = 0
        for consulta in objects:
            my_dict[(_MES[consulta.data.month], consulta.medico.especialidade)] += 1
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


class ConsConvView(TemplateView):
    template_name = 'graficos/consultasconvenio.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        tabela = Consulta.objects.all().order_by('convenio')
        contexto['tabela'] = tabela
        contexto['grafico'] = self._criar_grafico()
        return contexto

    def _criar_grafico(self):
        convenios = Convenio.objects.all()
        glabels = []
        gvalores = []
        for c in convenios:
            quantidade = Consulta.objects.filter(convenio=c).count()
            if quantidade > 0:
                glabels.append(c.nome)
                gvalores.append(quantidade)
        pyplot.pie(gvalores, labels=glabels)
        buffer = BytesIO()
        pyplot.savefig(buffer, format='png')
        buffer.seek(0)
        imagem = buffer.getvalue()
        grafico = base64.b64encode(imagem)
        grafico = grafico.decode('utf-8')
        buffer.close()
        return grafico
