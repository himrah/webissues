__author__ = 'rahul'
from track.models import *
from rest_framework import serializers
from track.form import UserFullName
from django.contrib.auth.models import User,Group
from django import forms
assign=forms.ModelChoiceField(queryset=UserFullName.objects.all())

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email')

class IssueSerializer(serializers.ModelSerializer):
    #created_by=UserSerializer()
    assign=forms.ModelChoiceField(queryset=UserFullName.objects.all())
    class Meta:
        model = issue
        fields=('id','name','created_date','created_by','status','comment','modify_by','priority','tat','assign','project_id')

class ProjectSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = project
        fields=('id','name','issue_set','description')