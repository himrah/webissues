from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from track.form import *
from django.contrib.auth import REDIRECT_FIELD_NAME,get_user_model,login as auth_login, authenticate
from django.core.context_processors import csrf
from django.contrib import auth
from track.serlierlizer import *
from django.views.generic.edit import FormView
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
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

@login_required(login_url='/accounts/login')
def issue_detail(request,pk):
    query=issue.objects.get(id=pk)
    return render_to_response('issue_details.html',{'issue':query,'user':request.user})




@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
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
    return render_to_response(template_name,args)




#@login_required(login_url='/accounts/login')
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    else:
        #return auth_view(request)
        form=LoginForm(request.POST)
        c={'form':form,'error':False}
        c.update(csrf(request))
        return render(request,'registration/login.html',c)

@login_required(login_url='/accounts/login')
def edit(request,pk=None):
    task=get_object_or_404(issue,id=pk)
    form=Issueform(request.POST or None,instance=task)
    user=request.user
    if request.POST and form.is_valid():
        name=request.user.first_name+" "+request.user.last_name
        task.modify_by=name
        task.save()
        form.save()
        return HttpResponseRedirect('/index/')
    return render(request,'edit_issue.html',{'form':form,'task':task,'user':user})


@login_required(login_url='/accounts/login')
def projectupdate(request,pk):
    temp=get_object_or_404(project,id=pk)
    updateproject=True
    form=projectform(request.POST or None, instance=temp)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/totalproject')
    return render(request,'edit_issue.html',{'form':form,'updateproject':updateproject,'temp':temp})

@login_required(login_url='/accounts/login')
def selectproject(request):
    query=project.objects.all()
    name=request.user
    return render_to_response('project_option.html',{'project':query,'name':name})


@login_required(login_url='/accounts/login')
def noproject(request):
    query=project.objects.all()
    issues=issue.objects.all()
    name=request.user
    only=True
    return render_to_response('project_option.html',{'project':query,'only':only,'issue':issues,'name':name})


@login_required(login_url='/accounts/login')
def create(request,pk):
    form=Issueform()
    if request.user.groups.get().name=='Associate':
        user=request.user
        return render_to_response('edit_issue.html',{'cannot':True,'user':user})
    else:
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
            new=True
            error=True
            return render(request,'edit_issue.html',{'form':form,'create':new,'error':error})
        new=True
        return render(request,'edit_issue.html',{'form':form,'create':new,'proj': pk})



@login_required(login_url='/accounts/login')
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

@login_required(login_url='/accounts/login')
def delete_issue(request,pk):
    iss=issue.objects.get(id=pk)
    return render_to_response('delete_confirmation.html',{'query':iss,'user':request.user})


@login_required(login_url='/accounts/login')
def delete_issues(request,pk):
    iss=issue.objects.get(id=pk)
    iss.delete()
    return HttpResponseRedirect('/index')

@login_required(login_url='/accounts/login')
def new(request):
    pr=True
    if request.method=='POST':
        form=Issueform(request.POST)
        if form.is_valid():
            task=issue()
            name=request.user.first_name+" "+request.user.last_name
            task.modify_by=name
            task.save()
            form.save()

            return HttpResponseRedirect('/index')
        else:
            form=projectform(request.POST)
        return render(request,'edit_issue.html',{'form':form,'project':pr})
    else:
        form=Issueform()
        return render(request,'edit_issue.html',{'form':form,'project':pr})


#@login_required(login_url='/accounts/login')
def auth_view(request):
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
        form=LoginForm(request.POST)
        c={'form':form,'error':True}
        c.update(csrf(request))
        return render(request,'registration/login.html',c)


#@login_required(login_url='/accounts/login')
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



@login_required(login_url='/accounts/login')
def issue_edit(request,pk):
    query=issue.objects.get(id=pk)
    temp='issue_details.html'
    return render_to_response(temp,{'obj':query})

import csv
@login_required(login_url='/accounts/login')
def export_csv(requests):
    from django.utils.encoding import smart_str
    response=HttpResponse(content='text/csv')
    row = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    query=issue.objects.all()
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    #row=csv.writer(response)
    #model=[]
    header=['ID','Name','Issue Description','Comments','Created By','Created Date','Modify By','Project Name','Priority','TAT','Status']
    row.writerow(header)
    for f in query:
        row.writerow([
            smart_str(f.id),
            smart_str(f.name),
            smart_str(f.issue_description),
            smart_str(f.comments),
            smart_str(f.created_by),
            smart_str(f.created_date),
            smart_str(f.modify_by),
            smart_str(f.project_id.name),
            smart_str(f.priority),
            smart_str(f.tat),
            smart_str(f.status)
        ])
    return response


@login_required(login_url='/accounts/login')
def searching(request):
    if request.method=='GET':
        search_q=request.GET['srch']
        query=issue.objects.filter(name__contains=search_q)
        context={
            'issues':query,
            'keyword':search_q,
            'user':request.user
        }
        return render_to_response('search_query.html',context)

def grade(request):
    return render_to_response('Grade_card.html',{'user':request.user})

from bs4 import BeautifulSoup as BS
import requests
def result(request):
    enrol=request.GET['enrol']
    option=request.GET['Program']
    url='https://webservices.ignou.ac.in/GradecardM/result.asp?eno='+enrol+'&program='+option+'&HIDDEN_submit=OK'
    print(url)
    r=requests.get(url)
    print(r.status_code)
    soup=BS(r.content,'html.parser')
    print(soup)
    enrol=soup.find_all('b')[3].text
    name=soup.find_all('b')[4].text
    prog=soup.find_all('b')[5].text
    info=[str(enrol),str(name),str(prog)]

    main=[]
    tr=soup.find_all('tr')
    for i in tr:
        td=i.find_all('td')
        temp=[]
        for j in td:
            temp.append(j.text)
        main.append(temp)
    return render_to_response('result.html',{'info':info,'mark':main,'user':request.user})

