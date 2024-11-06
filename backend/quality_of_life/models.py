from django.db import models

class Appeal(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    completion_date = models.DateTimeField()
    status = models.IntegerField()
    process_status = models.IntegerField()
    address = models.TextField()
    coordx = models.FloatField()
    coordy = models.FloatField()

class ExecutionInfo(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="executions")
    executors = models.TextField()
    executor_id = models.IntegerField()
    executor_state_institute_id = models.IntegerField()
    call_status = models.IntegerField()
    process_status = models.IntegerField()
    current_task_id = models.IntegerField()

class ResponseInfo(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="responses")
    answer = models.TextField()
    answer_rating = models.IntegerField()
    answer_quality_id = models.IntegerField()
    answer_rating_from_user_id = models.IntegerField()

class AdditionalAttributes(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="attributes")
    received_from = models.CharField(max_length=255)
    category_id = models.IntegerField()
    kind_of_appeal_id = models.IntegerField()
    budgetary_funds_are_required = models.BooleanField()
