# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BankAccount(models.Model):
    acc_id = models.AutoField(primary_key=True)
    acc_owner = models.CharField(max_length=75)
    acc_number = models.CharField(unique=True, max_length=20)
    acc_routing_number = models.CharField(max_length=20)
    acc_type = models.CharField(max_length=11)
    acc_balance = models.FloatField()

    class Meta:
        managed = False
        db_table = 'bank_account'


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_symbol = models.CharField(max_length=50)
    company_name = models.CharField(max_length=1000)
    company_description = models.CharField(max_length=2500)
    company_employees = models.CharField(max_length=50)
    company_address = models.CharField(max_length=75)
    company_zip = models.CharField(max_length=10)
    company_country = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'company'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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


class Queue(models.Model):
    queue_no = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    company_symbol = models.CharField(max_length=10)
    total_amount = models.FloatField()
    stock_price = models.FloatField()
    stocks_count = models.IntegerField()
    tr_account = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'queue'


class RecurringBuy(models.Model):
    rec_id = models.AutoField(primary_key=True)
    rec_user_id = models.CharField(max_length=50)
    rec_symbol = models.CharField(max_length=50)
    rec_count = models.IntegerField()
    rec_interval = models.CharField(max_length=50)
    rec_start_timestamp = models.CharField(max_length=50)
    rec_schedule = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'recurring_buy'


class Stocks(models.Model):
    stock_id = models.AutoField(primary_key=True)
    stock_user = models.CharField(max_length=50)
    stock_symbol = models.CharField(max_length=50)
    stock_buy_price = models.FloatField()
    stock_buy_timestamp = models.CharField(max_length=50)
    stock_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stocks'


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_user = models.CharField(max_length=50)
    transaction_timestamp = models.CharField(max_length=50)
    transaction_account = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=20)
    transaction_symbol = models.CharField(max_length=50)
    transaction_price = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'transaction'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_fname = models.CharField(max_length=50)
    user_lname = models.CharField(max_length=50)
    user_ssn = models.TextField()
    user_address = models.CharField(max_length=75)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_phone = models.TextField()
    user_token = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'user'
