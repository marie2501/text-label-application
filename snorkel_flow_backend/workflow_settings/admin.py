from django.contrib import admin

from workflow_settings.models import Workflow, File, Labelfunction, Run, Feature, LabelSummary


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

@admin.register(Run)
class Labelfunction_Run_Admin(admin.ModelAdmin):
    pass

@admin.register(Feature)
class Feature_Admin(admin.ModelAdmin):
    pass

@admin.register(LabelSummary)
class LabelSummary_Admin(admin.ModelAdmin):
    pass