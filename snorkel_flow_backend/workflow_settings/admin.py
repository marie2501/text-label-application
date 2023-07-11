from django.contrib import admin

from workflow_settings.models import Workflow


# Register your models here.
@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass