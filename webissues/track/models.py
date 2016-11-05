from django.db import models
from datetime import datetime
from track.full import *
from django.contrib.auth.models import User
# Create your models here.

class project(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField()
    def __str__(self):
        return self.name


class issue(models.Model):
    nothing = '----'
    new ='New'
    inprocess='In Process'
    complete='Complete'
    choices=(
        (new , 'New'),
        (inprocess,'In Process'),
        (complete,'Complete'),
    )

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    created_date=models.DateTimeField(default=datetime.now,blank=True)
    #created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_by=models.CharField(max_length=20,blank=True)
    status=models.CharField(max_length=10,choices=choices,default=nothing,blank=True)
    comment=models.TextField(blank=True)
    modify_by=models.CharField(max_length=20,blank=True)
    #assigned_to=models.ForeignKey(User)
    #assigned_to=models.OneToOneField(User,on_delete=models.CASCADE)
    #assigned_to=models.OneToOneField(User,on_delete=models.CASCADE)
    priority=models.IntegerField(null=True)
    tat=models.IntegerField(null=True)
    assign=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    project_id=models.ForeignKey(project,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.id)+' '+self.name



