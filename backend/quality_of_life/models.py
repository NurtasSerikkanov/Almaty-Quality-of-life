from django.db import models
from django.contrib.gis.db import models

class Appeal(models.Model):
    title = models.TextField(db_column='title')
    description = models.TextField(db_column='description', blank=True, null=True)
    creation_date = models.DateTimeField(db_column='creation_date')
    completion_date = models.DateTimeField(db_column='completion_date', null=True, blank=True)
    status = models.IntegerField(db_column='status')
    process_status = models.IntegerField(db_column='process_status')
    address = models.TextField(db_column='address')
    coord_x = models.FloatField(db_column='coord_x')
    coord_y = models.FloatField(db_column='coord_y')
    location = models.PointField(srid=4326, geography=True, spatial_index=True, null=True)
    hexagon_id = models.IntegerField(blank=True, null=True, db_column='hexagon_id')
    boundary_coords = models.JSONField(blank=True, null=True, db_column='boundary_coords')
    district_name = models.TextField(blank=True, null=True, db_column='district_name')
    district_boundary = models.PolygonField(srid=4326, geography=True, spatial_index=True, blank=True, null=True,
                                            db_column='district_boundary')

    class Meta:
        db_table = 'appeals'


class ExecutionInfo(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="executions", db_column='appeal_id')
    executors = models.TextField(db_column='executors', null=True, blank=True)  # Разрешаем null
    executor_id = models.IntegerField(db_column='executor_id', null=True, blank=True)
    executor_state_institute_id = models.IntegerField(db_column='executor_state_institute_id', null=True, blank=True)
    call_status = models.IntegerField(db_column='call_status', null=True, blank=True)
    process_status = models.IntegerField(db_column='process_status', null=True, blank=True)
    current_task_id = models.IntegerField(db_column='current_task_id', null=True, blank=True)

    class Meta:
        db_table = 'execution_info'

class ResponseInfo(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="responses", db_column='appeal_id')
    answer = models.TextField(db_column='answer', null=True, blank=True)  # Разрешаем null
    answer_rating = models.IntegerField(db_column='answer_rating', null=True, blank=True)
    answer_quality_id = models.IntegerField(db_column='answer_quality_id', null=True, blank=True)
    answer_rating_from_user_id = models.IntegerField(db_column='answer_rating_from_user_id', null=True, blank=True)

    class Meta:
        db_table = 'response_info'

class AdditionalAttributes(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="attributes", db_column='appeal_id')
    received_from = models.CharField(max_length=255, db_column='received_from', null=True, blank=True)
    category_id = models.IntegerField(db_column='category_id', null=True, blank=True)  # Разрешаем null
    kind_of_appeal_id = models.ForeignKey('KindOfAppeal', on_delete=models.SET_NULL, null=True, db_column='kind_of_appeal_id', default=None)
    budgetary_funds_are_required = models.BooleanField(db_column='budgetary_funds_are_required', null=True, blank=True)

    class Meta:
        db_table = 'additional_attributes'

class KindOfAppeal(models.Model):
    kind_of_appeal_id = models.IntegerField(unique=True, db_column='kind_of_appeal_id')
    name_en = models.CharField(max_length=255, db_column='name_en')
    name_ru = models.CharField(max_length=255, db_column='name_ru')
    name_kk = models.CharField(max_length=255, db_column='name_kk')
    is_active = models.BooleanField(db_column='is_active')

    class Meta:
        db_table = 'kind_of_appeal'
        managed = False