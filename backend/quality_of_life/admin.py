from django.contrib import admin
from .models import Appeal, ExecutionInfo, ResponseInfo, AdditionalAttributes

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creation_date', 'completion_date', 'status', 'address')

@admin.register(ExecutionInfo)
class ExecutionInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'appeal', 'executors', 'executor_id', 'call_status', 'process_status')

@admin.register(ResponseInfo)
class ResponseInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'appeal', 'answer', 'answer_rating', 'answer_quality_id')

@admin.register(AdditionalAttributes)
class AdditionalAttributesAdmin(admin.ModelAdmin):
    list_display = ('id', 'appeal', 'received_from', 'category_id', 'kind_of_appeal_id')
