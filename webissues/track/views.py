from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from track.models import *
from track.form import *
from django.contrib.auth import REDIRECT_FIELD_NAME,get_user_model,login as auth_login, authenticate
from django.core.context_processors import csrf
from django.contrib import auth
from track.serlierlizer import *
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.http.response import HttpResponseRedirect,HttpResponse
from rest_framework import viewsets
# Create your views here.


class IssueSet(viewsets.ModelViewSet):
    queryset = issue.objects.all()
    serializer_class = IssueSerializer

class ProjectSet(viewsets.ModelViewSet):
    queryset = project.objects.all()
    serializer_class = ProjectSeralizer

class UserSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



def projectis_issue(request,pk):
    temp=project.objects.get(id=pk)
    query=temp.issue_set.all()
    proj=project.objects.all()
    #prj_name=temp.name
    name=request.user

    args={'query':query,
          'user':name,
          'project':proj,
          'project_name':temp
          }
    return render_to_response('dashboard.html',args)


@login_required(login_url='/accounts/login/')
def index(request):
    query=issue.objects.all()
    proj=project.objects.all()
    name=request.user
    prj_name="All Project"
    template_name='dashboard.html'
    args={'query':query,
      'user':name,
      'project':proj,
      'project_name':prj_name
      }
    return render_to_response('dashboard.html',args)


from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:
        #return auth_view(request)
        form=LoginForm(request.POST)
        c={'form':form,'error':False}
        c.update(csrf(request))
        return render(request,'registration/login.html',c)


def edit(request,pk=None):
    task=get_object_or_404(issue,id=pk)
    form=Issueform(request.POST or None,instance=task)
    user=request.user
    if request.POST and form.is_valid():
        name=request.user.first_name+" "+request.user.last_name
        task.modify_by=name
        task.save()
        form.save()
        #redirect_url=reverse('/index/')
        return HttpResponseRedirect('/index/')
    return render(request,'edit_issue.html',{'form':form,'task':task,'user':user})


def projectupdate(request,pk):
    temp=get_object_or_404(project,id=pk)
    updateproject=True
    form=projectform(request.POST or None, instance=temp)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/totalproject')
    return render(request,'edit_issue.html',{'form':form,'updateproject':updateproject,'temp':temp})


def selectproject(request):
    query=project.objects.all()
    name=request.user
    return render_to_response('project_option.html',{'project':query,'name':name})
def noproject(request):
    query=project.objects.all()
    issues=issue.objects.all()
    name=request.user
    only=True
    return render_to_response('project_option.html',{'project':query,'only':only,'issue':issues,'name':name})

def create(request,pk):
    form=Issueform()
    """if request.user.groups.get().name=='Manager':
        usr='Manager'
    elif request.user.groups.get().name=='Associate':
        usr='Associate'
    elif request.user.groups.get().name=='Adminstration':
        usr='Adminstration'"""

    if request.user.groups.get().name=='Associate':
        user=request.user
        return render_to_response('edit_issue.html',{'cannot':True,'user':user})
    else: #request.user.groups.get().name=='Manager':
        if request.method=='POST':
            form=Issueform(request.POST)
            if form.is_valid():
                task=form.save(commit=False)
                temp=project.objects.get(id=pk)
                #d=issue.objects.get(id=pk)
                task.project_id=temp
                name=request.user.first_name+" "+request.user.last_name
                task.created_by=name
                task.modify_by=name
                task.save()
                form.save()
                return HttpResponseRedirect('/project/'+pk)
                #reverse('index')
                #return HttpResponse(pk)
            new=True
            error=True
            return render(request,'edit_issue.html',{'form':form,'create':new,'error':error})
        new=True
        return render(request,'edit_issue.html',{'form':form,'create':new,'proj': pk})
def create_project(request):
    if request.user.groups.get().name=='Associate':
        user=request.user
        return render_to_response('edit_issue.html',{'cannot':True,'name':user})
    else:
        form=projectform()
        p=True
        if request.method=="POST":
            form=projectform(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/index')
            else:
                p=True
                return render(request,'edit_issue.html',{'form':form,'project':p})
        return render(request,'edit_issue.html',{'form':form,'project':p})

def delete_issue(request,pk):
    iss=issue.objects.get(id=pk)
    iss.delete()
    return HttpResponse("deleted <a href=/index/>Click</a> to Dashboard")



def new(request):
    pr=True
    if request.method=='POST':
        form=Issueform(request.POST)
        if form.is_valid():
            task=issue()
            name=request.user.first_name+" "+request.user.last_name
            task.modify_by=name
            #task.created_by=name
            task.save()
            form.save()

            return HttpResponseRedirect('/index')
        else:
            form=projectform(request.POST)
        return render(request,'edit_issue.html',{'form':form,'project':pr})
    else:
        #request.method=='GET':
        form=Issueform()
        return render(request,'edit_issue.html',{'form':form,'project':pr})


def auth_view(request):
    #form=LoginForm(request.POST)
    #if form.is_valid():
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/index/')
        #return redirect('%s' %request.path)
    elif request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
    #return HttpResponseRedirect('/invalid')
        form=LoginForm(request.POST)
        c={'form':form,'error':True}
        c.update(csrf(request))
        return render(request,'registration/login.html',c)
    #return render(request,'registration/login.html')

"""def login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:
        c={}
        c.update(csrf(request))
        return render_to_response('registration/login.html',views.login)
        #views.login
        #return HttpResponse(views.login)"""

"""if request.user is None:
        return HttpResponseRedirect('/index')
    else:
        return HttpResponse(views.login)"""


        #d.login
        #c={}
        #c.update(csrf(request))
        #return render_to_response('registration/login.html',c)





class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_authenticated_user = False
    authentication_form = LoginForm
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to=self.get_success_url()
            #if redirect_to==self.request.path
            return HttpResponseRedirect(redirect_to)
        return super(LoginView,self).dispatch(request,*args)



    def get_success_url(self):
        """Ensure the user-originating redirection URL is safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, ''))

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def form_invalid(self, form):
        auth_login(self.request,form.get_user())
        return HttpResponseRedirect(self.get_success_url())

@login_required(login_url='/accounts/login')
def profile(request):
    email=request.user.email
    group=Group.objects.get(user=request.user.id)
    #Blog=request.user.objects.get(id=1)
    nn=request.user.date_joined
    argus={'user':request.user,
           'email':email,
           'group':group,
           'join':nn,
           }
    return render_to_response('registration/profile.html',argus)
#    return HttpResponse(user)

"""def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect('/accounts/invalid')"""

def issue_edit(request,pk):
    query=issue.objects.get(id=pk)
    temp='issue_details.html'
    return render_to_response(temp,{'obj':query})

import csv
def export_csv(requests):
    #query=issue.objects.all()
    #file=open('result.csv','wt',newline='')
    #row=csv.writer(file)
    model=[]
    for f in issue.objects.all():
        model.append(f.__dict__)
    return render_to_response('test.html',{'models':model})
    #row=csv.writer(file)

