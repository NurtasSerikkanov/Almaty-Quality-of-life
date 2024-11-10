# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdditionalAttributes(models.Model):
    appealid = models.ForeignKey('Appeals', models.DO_NOTHING, db_column='appealid', blank=True, null=True)
    receivedfrom = models.CharField(max_length=255, blank=True, null=True)
    categoryid = models.IntegerField(blank=True, null=True)
    kindofappealid = models.IntegerField(blank=True, null=True)
    budgetaryfundsarerequired = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'additional_attributes'


class Appeals(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    creationdate = models.DateTimeField(blank=True, null=True)
    completiondate = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    processstatus = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    coordx = models.FloatField(blank=True, null=True)
    coordy = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appeals'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExecutionInfo(models.Model):
    appealid = models.ForeignKey(Appeals, models.DO_NOTHING, db_column='appealid', blank=True, null=True)
    executors = models.TextField(blank=True, null=True)
    executorid = models.IntegerField(blank=True, null=True)
    executorstateinstituteid = models.IntegerField(blank=True, null=True)
    callstatus = models.IntegerField(blank=True, null=True)
    processstatus = models.IntegerField(blank=True, null=True)
    currenttaskid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'execution_info'


class Overall(models.Model):
    id = models.IntegerField(primary_key=True)
    discriminator = models.CharField(max_length=100, blank=True, null=True)
    definitionid = models.UUIDField(blank=True, null=True)
    startedat = models.DateTimeField(blank=True, null=True)
    completedat = models.DateTimeField(blank=True, null=True)
    processstatus = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    creationdate = models.DateTimeField(blank=True, null=True)
    completiondate = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    receivedfrom = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    readedby = models.CharField(max_length=255, blank=True, null=True)
    lastchangeddate = models.DateTimeField(blank=True, null=True)
    executors = models.TextField(blank=True, null=True)
    callstatus = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    number = models.CharField(max_length=50, blank=True, null=True)
    creatorid = models.IntegerField(blank=True, null=True)
    kindofappealid = models.IntegerField(blank=True, null=True)
    executorid = models.IntegerField(blank=True, null=True)
    ownerid = models.IntegerField(blank=True, null=True)
    coordx = models.FloatField(blank=True, null=True)
    coordy = models.FloatField(blank=True, null=True)
    executorstateinstituteid = models.IntegerField(blank=True, null=True)
    callcenteruniqueid = models.CharField(max_length=100, blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)
    categoryid = models.IntegerField(blank=True, null=True)
    isclone = models.BooleanField(blank=True, null=True)
    stateinstitutereceivedate = models.DateTimeField(blank=True, null=True)
    answerrating = models.IntegerField(blank=True, null=True)
    currenttaskid = models.IntegerField(blank=True, null=True)
    incedentareaid = models.IntegerField(blank=True, null=True)
    budgetaryfundsarerequired = models.BooleanField(blank=True, null=True)
    answerqualityid = models.IntegerField(blank=True, null=True)
    parliamentarianid = models.IntegerField(blank=True, null=True)
    planneddate = models.DateTimeField(blank=True, null=True)
    signeddata = models.TextField(blank=True, null=True)
    shuno = models.CharField(max_length=100, blank=True, null=True)
    isinteresting = models.BooleanField(blank=True, null=True)
    answerratingfromuserid = models.IntegerField(blank=True, null=True)
    appealaddressid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'overall'


class QualityOfLifeAdditionalattributes(models.Model):
    id = models.BigAutoField(primary_key=True)
    received_from = models.CharField(max_length=255)
    category_id = models.IntegerField()
    kind_of_appeal_id = models.IntegerField()
    budgetary_funds_are_required = models.BooleanField()
    appeal = models.ForeignKey('QualityOfLifeAppeal', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quality_of_life_additionalattributes'


class QualityOfLifeAppeal(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    completion_date = models.DateTimeField()
    status = models.IntegerField()
    process_status = models.IntegerField()
    address = models.TextField()
    coordx = models.FloatField()
    coordy = models.FloatField()

    class Meta:
        managed = False
        db_table = 'quality_of_life_appeal'


class QualityOfLifeExecutioninfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    executors = models.TextField()
    executor_id = models.IntegerField()
    executor_state_institute_id = models.IntegerField()
    call_status = models.IntegerField()
    process_status = models.IntegerField()
    current_task_id = models.IntegerField()
    appeal = models.ForeignKey(QualityOfLifeAppeal, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quality_of_life_executioninfo'


class QualityOfLifeResponseinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    answer = models.TextField()
    answer_rating = models.IntegerField()
    answer_quality_id = models.IntegerField()
    answer_rating_from_user_id = models.IntegerField()
    appeal = models.ForeignKey(QualityOfLifeAppeal, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quality_of_life_responseinfo'


class ResponseInfo(models.Model):
    appealid = models.ForeignKey(Appeals, models.DO_NOTHING, db_column='appealid', blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    answerrating = models.IntegerField(blank=True, null=True)
    answerqualityid = models.IntegerField(blank=True, null=True)
    answerratingfromuserid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'response_info'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'
