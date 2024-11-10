from django.db import models

class Appeal(models.Model):
    title = models.TextField(db_column='title')
    description = models.TextField(blank=True, null=True, db_column='description')
    creation_date = models.DateTimeField(db_column='creation_date')
    completion_date = models.DateTimeField(db_column='completion_date')
    status = models.IntegerField(db_column='status')
    process_status = models.IntegerField(db_column='process_status')
    address = models.TextField(db_column='address')
    coord_x = models.FloatField(db_column='coord_x')
    coord_y = models.FloatField(db_column='coord_y')

    class Meta:
        db_table = 'appeals'

class ExecutionInfo(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="executions", db_column='appeal_id')
    executors = models.TextField(db_column='executors')
    executor_id = models.IntegerField(db_column='executor_id')
    executor_state_institute_id = models.IntegerField(db_column='executor_state_institute_id')
    call_status = models.IntegerField(db_column='call_status')
    process_status = models.IntegerField(db_column='process_status')
    current_task_id = models.IntegerField(db_column='current_task_id')

    class Meta:
        db_table = 'execution_info'

class ResponseInfo(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="responses", db_column='appeal_id')
    answer = models.TextField(db_column='answer')
    answer_rating = models.IntegerField(db_column='answer_rating')
    answer_quality_id = models.IntegerField(db_column='answer_quality_id')
    answer_rating_from_user_id = models.IntegerField(db_column='answer_rating_from_user_id')

    class Meta:
        db_table = 'response_info'

class AdditionalAttributes(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="attributes", db_column='appeal_id')
    received_from = models.CharField(max_length=255, db_column='received_from')
    category_id = models.IntegerField(db_column='category_id')
    kind_of_appea_id = models.IntegerField(db_column='kind_of_appea_id')
    budgetary_funds_are_required = models.BooleanField(db_column='budgetary_funds_are_required')

    class Meta:
        db_table = 'additional_attributes'
