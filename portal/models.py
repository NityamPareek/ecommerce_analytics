# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
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


class Customers(models.Model):
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    customer_unique_id = models.CharField(max_length=255, blank=True, null=False, primary_key=True)
    customer_zip_code_prefix = models.IntegerField(blank=True, null=True)
    customer_city = models.CharField(max_length=255, blank=True, null=True)
    customer_state = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


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


# class Geolocation(models.Model):
#     geolocation_zip_code_prefix = models.IntegerField(blank=True, null=True)
#     geolocation_lat = models.FloatField(blank=True, null=True)
#     geolocation_lng = models.FloatField(blank=True, null=True)
#     geolocation_city = models.CharField(max_length=255, blank=True, null=True)
#     geolocation_state = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'geolocation'


class OrderItems(models.Model):
    order_id = models.CharField(max_length=255, blank=True, null=False, primary_key=True)
    order_item_id = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    seller_id = models.CharField(max_length=255, blank=True, null=True)
    shipping_limit_date = models.DateTimeField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    freight_value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_items'


class OrderPayments(models.Model):
    order_id = models.CharField(max_length=255, blank=True, null=False, primary_key=True)
    payment_sequential = models.IntegerField(blank=True, null=True)
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    payment_installments = models.IntegerField(blank=True, null=True)
    payment_value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_payments'


class OrderReviews(models.Model):
    review_id = models.CharField(max_length=255, blank=True, null=False, primary_key=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    review_score = models.IntegerField(blank=True, null=True)
    review_comment_title = models.TextField(blank=True, null=True)
    review_comment_message = models.TextField(blank=True, null=True)
    review_creation_date = models.DateTimeField(blank=True, null=True)
    review_answer_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_reviews'


class Orders(models.Model):
    order_id = models.CharField(max_length=255, blank=True, null=False, primary_key=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    order_status = models.CharField(max_length=255, blank=True, null=True)
    order_purchase_timestamp = models.DateTimeField(blank=True, null=True)
    order_approved_at = models.DateTimeField(blank=True, null=True)
    order_delivered_carrier_date = models.DateTimeField(blank=True, null=True)
    order_delivered_customer_date = models.DateTimeField(blank=True, null=True)
    order_estimated_delivery_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Product(models.Model):
    id = models.IntegerField(blank=False, null=False, primary_key=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_category_name = models.CharField(max_length=255, blank=True, null=True)
    product_name_length = models.IntegerField(blank=True, null=True)
    product_description_length = models.IntegerField(blank=True, null=True)
    product_photos_qty = models.IntegerField(blank=True, null=True)
    product_weight_g = models.FloatField(blank=True, null=True)
    product_length_cm = models.FloatField(blank=True, null=True)
    product_height_cm = models.FloatField(blank=True, null=True)
    product_width_cm = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Sellers(models.Model):
    seller_id = models.CharField(max_length=255, blank=True, null=False, primary_key=True)
    seller_zip_code_prefix = models.IntegerField(blank=True, null=True)
    seller_city = models.CharField(max_length=255, blank=True, null=True)
    seller_state = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sellers'
