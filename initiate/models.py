from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# -------------------------new added----------------------------
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Image(models.Model):
 photo = models.ImageField(upload_to="myimage")
#  date = models.DateTimeField(auto_now_add=True) 

# -------------------------new added----------------------------
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


class StatictickerConfigfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    json_data = models.TextField()

    class Meta:
        managed = False
        db_table = 'staticticker_configfile'


class StatictickerStaticticker(models.Model):
    id = models.BigAutoField(primary_key=True)
    ticker_enabler = models.IntegerField()
    background_color = models.CharField(max_length=18)
    ticker_logo = models.CharField(max_length=100, blank=True, null=True)
    ticker_msg = models.CharField(max_length=200)
    text_color = models.CharField(max_length=40)
    font_size = models.CharField(max_length=20)
    font_type = models.CharField(max_length=40)
    ticker_display_time = models.IntegerField()
    position_box = models.CharField(max_length=12)
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'staticticker_staticticker'


class TickerDetails(models.Model):
    ticker_id = models.AutoField(primary_key=True)
    ticker_type = models.CharField(max_length=40)
    # dated_on = models.DateTimeField()
    ticker_json = models.TextField(blank=True)
    created_for = models.CharField(max_length=300, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField()
    modified_by = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField()
    is_active = models.PositiveIntegerField()
    is_deleted = models.PositiveIntegerField()
    deleted_on = models.DateTimeField(blank=True, null=True)
    reason_for_delete = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticker_details'


class TickerHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    ticker_id = models.PositiveIntegerField()
    ticker_type = models.CharField(max_length=40)
    ticker_json = models.TextField(blank=True)
    created_for = models.CharField(max_length=300)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField()
    modified_by = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    is_active = models.PositiveIntegerField()
    is_deleted = models.PositiveIntegerField()
    deleted_on = models.DateTimeField(blank=True, null=True)
    reason_for_delete = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticker_history'


# ----------------------------------new added-------------------------------
'''
#Command in the  shell to create Blog ' Post

import random
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from faker import Factory
fake = Factory.create()
s = ' '

user = User.objects.first()
for item in range(1,40):
    author = fake.name()
    title = s.join(fake.words(random.randint(4,16)))
    slug = slugify(title)
    #slugify the title
    status = 'published'
    body = s.join(fake.paragraphs(random.randint(2,10)))
    book = Post.objects.create(title=title, author=user, status=status, body=body, slug=slug )
    print(author)
    book.save()
'''

# Create your models here.

class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('published', 'Published'),
            )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    objects = models.Manager()
    published = PublishedManager()


    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, 
            self.publish.strftime('%m'),
            self.publish.strftime('%d'),
            self.slug])

