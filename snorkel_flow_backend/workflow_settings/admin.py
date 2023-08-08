from django.contrib import admin

from workflow_settings.models import Workflow, File, Datapoint, Labelfunction


# Register your models here.
@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(Datapoint)
class DatapointAdmin(admin.ModelAdmin):
    pass

@admin.register(Labelfunction)
class LabelfunctionAdmin(admin.ModelAdmin):
    pass