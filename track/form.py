__author__ = 'Rahul'
from django.contrib.auth.forms import AuthenticationForm
from track.models import *
from django.contrib.auth.models import User
from django.utils import encoding
from django import forms
#from djng.forms import NgFormValidationMixin






# If you don't do this you cannot use Bootstrap CSS
class UserFullName(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()

class Issueform(forms.ModelForm):
    assign=forms.ModelChoiceField(queryset=UserFullName.objects.all())
    class Meta:
        model=issue
        #assign=userfullname(queryset=User.objects.all())
        fields=['name','status','issue_description','comments','priority','tat','assign']



class projectform(forms.ModelForm):
    class Meta:
        model=project
        fields='__all__'



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))




#class angularform(NgFormValidationMixin,LoginForm):
#    pass
    """def clean_username(self):
        data=self.cleaned_data['username']
        if not data:
            raise forms.ValidationError("Please Enter Username")
        return data
    def clean_password(self):
        data=self.cleaned_data['password']
        if not data:
            raise forms.ValidationError("Please Enter Password")
        return data
    def clean(self):
        #username=self.cleaned_data['username']
        username=self.cleaned_data.get('username',None)
        password=self.cleaned_data.get('password',None)
        #password=self.cleaned_data['password']
        try:
            User.objects.get(username=username,password=password)

        except User.DoesNotExist:
            raise forms.ValidationError("Email or password Incorrect")
        return self.cleaned_data"""
