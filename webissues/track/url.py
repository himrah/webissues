from django.conf.urls import include, url
from rest_framework import serializers
from django.contrib.auth.models import *

class UserSet(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="track:user-detail")
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','groups')
