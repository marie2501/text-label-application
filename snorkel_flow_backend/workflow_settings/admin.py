from django.contrib import admin

from workflow_settings.models import Workflow, File, Labelfunctions


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

@admin.register(Labelfunctions)
class LabelfunctionAdmin(admin.ModelAdmin):
    pass