from django.contrib import admin

from workflow_settings.models import Workflow, File, Labelfunction, Labelfunction_Run


# Register your models here.
@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

# @admin.register(Datapoint)
# class DatapointAdmin(admin.ModelAdmin):
#     pass

@admin.register(Labelfunction)
class LabelfunctionAdmin(admin.ModelAdmin):
    pass

@admin.register(Labelfunction_Run)
class Labelfunction_Run_Admin(admin.ModelAdmin):
    pass