from django.urls import path

from core import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('relatorios/pacientes', views.PacientesListView.as_view(), name='relat_pacientes'),
    path('relatorios/pdfpacientes', views.RelatPdfPacientes.as_view(), name='pdf_pacientes'),
    path('relatorios/pdfpacientesconvenio', views.RelatPdfPacientesConvenio.as_view(), name='pdf_pacientes_convenio'),
    path('relatorios/pdfconsultas', views.RelatPdfConsultasEspecialidade.as_view(), name='pdf_consultas'),
    path('relatorios/pdfconsultasmedico', views.RelatPdfPacientesEspecialidade.as_view(), name='pdf_consultas_medico'),
]
