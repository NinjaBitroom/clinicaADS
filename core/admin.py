from django.contrib import admin
from core import models


@admin.register(models.Ambulatorio)
class AmbulatorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numleitos', 'andar')


class MedicoConvenioInline(admin.TabularInline):
    model = models.Atende
    extra = 1
    # raw_id_fields = ['convenio']


@admin.register(models.Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('crm', 'nome', 'telefone', 'salario', 'ambulatorio')
    inlines = [MedicoConvenioInline]


class PacienteConvenioInline(admin.TabularInline):
    model = models.Possui
    extra = 1
    # raw_id_fields = ['convenio']


@admin.register(models.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'cidade', 'ambulatorio')
    inlines = [PacienteConvenioInline]
