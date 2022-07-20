from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class SetUp(models.Model):
    FQDN=models.CharField(max_length=60)
    Dvs_Token=models.CharField(max_length=150,null=True)
    Rundeck_Token=models.CharField(max_length=150,null=True)
    Rundeck_Api_Version=models.IntegerField(default=-1)
    Rundeck_Start_Job=models.CharField(max_length=150,null=True)
    Rundeck_Stop_Job=models.CharField(max_length=150,null=True)
    Apache_server_url=models.CharField(max_length=150,null=True)
    Ticker_FQDN=models.CharField(max_length=150,null=True)

class RundeckLog(models.Model):
    rundeck_id=models.IntegerField(primary_key=True)
    ticker_id=models.IntegerField(null=True)
    ticker_title=models.CharField(max_length=150,null=True)
    execution= models.CharField(max_length=150,null=True,default="Pending")
    successfull_nodes= models.TextField(blank=True,null=True,default="None")
    failed_nodes= models.TextField(blank=True,null=True,default="None")
    tv_status=models.CharField(max_length=150,null=True,default="None")
    iPad_status=models.CharField(max_length=150,null=True,default="None")
   
   
class TickerDetails(models.Model):
    ticker_id = models.AutoField(primary_key=True)
    ticker_type = models.CharField(max_length=60)
    ticker_title = models.CharField(max_length=50,default='Not Specific')
    # dated_on = models.DateTimeField()
    ticker_json = models.TextField(blank=True)
    ticker_start_time =models.DateTimeField(null=True)
    ticker_end_time =models.DateTimeField(null=True)
    wings = models.CharField(max_length=300, null=True)
    floors = models.CharField(max_length=300, null=True)
    rooms = models.CharField(max_length=300, null=True)
    roomTypeSelection=models.CharField(max_length=300,null=True)
    frequency = models.CharField(max_length=30,null=True)
    occuring_days = models.CharField(max_length=500,null=True)
    ticker_priority= models.CharField(max_length=10,default='Not Specific')
    created_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField()
    modified_by = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField()
    is_active = models.PositiveIntegerField()
    is_deleted = models.PositiveIntegerField()
    deleted_on = models.DateTimeField(blank=True, null=True)
    rundeckid = models.PositiveIntegerField(null=True)
    # reason_for_delete = models.CharField(max_length=300, blank=True, null=True)
    # photo = models.ImageField(upload_to="myimage")

    def __str__(self):
        return " Ticker Title : "+self.ticker_title+ ",     Id : (" + str(self.ticker_id)+")"


class TickerHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    ticker_id = models.PositiveIntegerField()
    ticker_type = models.CharField(max_length=40)
    ticker_title = models.CharField(max_length=50,default='Not Specific')
    ticker_json = models.TextField(blank=True)
    ticker_start_time =models.DateTimeField(null=True)
    ticker_end_time =models.DateTimeField(null=True)
    wings = models.CharField(max_length=300, null=True)
    floors = models.CharField(max_length=300, null=True)
    rooms = models.CharField(max_length=300, null=True)
    frequency = models.CharField(max_length=30,null=True)
    occuring_days = models.CharField(max_length=50,null=True)
    ticker_priority= models.CharField(max_length=10,default='Not Specific')
    created_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField()
    modified_by = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    is_active = models.PositiveIntegerField()
    is_deleted = models.PositiveIntegerField()
    deleted_on = models.DateTimeField(blank=True, null=True)
    rundeckid = models.PositiveIntegerField(null=True)
    # reason_for_delete = models.CharField(max_length=300, blank=True, null=True)


class Task(models.Model):
    tv_condition_before = models.CharField(max_length=200)
    tv_condition_after = models.CharField(max_length=200)
    room_no = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    ipad_condition_before = models.CharField(max_length=200)
    ipad_condition_after = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    ip = models.CharField(max_length=200)
            
   


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

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


