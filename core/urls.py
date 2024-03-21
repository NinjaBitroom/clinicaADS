from django.urls import path

from core import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('relatorios/pacientes', views.PacientesListView.as_view(), name='relat_pacientes'),
    path('relatorios/pdfpacientes', views.RelatPdfPacientes.as_view(), name='pdf_pacientes'),
    path('relatorios/pacientesconvenio', views.PacientesConvenioView.as_view(), name='relat_pacientes_convenio'),
    path('relatorios/pdfpacientesconvenio', views.RelatPdfPacientesConvenio.as_view(), name='pdf_pacientes_convenio'),
    path('relatorios/consultas', views.ConsultasEspecialidadeView.as_view(), name='relat_consultas'),
    path('relatorios/pdfconsultas', views.RelatPdfConsultasEspecialidade.as_view(), name='pdf_consultas'),
    path(
        'relatorios/pacientesespecialidades',
        views.PacientesEspecialidadeView.as_view(),
        name='relat_pacientes_especialidade'
    ),
    path(
        'relatorios/pdfpacientesespecialidades',
        views.RelatPdfPacientesEspecialidade.as_view(),
        name='pdf_pacientes_especialidade'
    ),
    path('graficos/consultasconvenio', views.ConsConvView.as_view(), name='graf_cons_conv'),
    path('graficos/paconvenio', views.PacientePorConvenioListView.as_view(), name='graf_pac_conv'),
]
