from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from app.models import Ins, Form
from django.db.models import Sum, Count, Min, Max
import io
import csv
import datetime
import random
import time
# from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from .forms import LoginForm, SignUpForm

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "hodtemp/accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })


def index(request):
    insurance = Ins.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(insurance, 1)
    try:
        ins = paginator.page(page)
    except PageNotAnInteger:
        ins = paginator.page(1)
    except EmptyPage:
        ins = paginator.page(paginator.num_pages)

    return render(request, 'user-tables.html', { 'ins': insurance })

class InsListView(ListView):
    model = Ins
    template_name = 'user-tables.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'id'  # Default: object_list
    paginate_by = 10
    insurance = Ins.objects.all()  

    


def usertables(request):
    insurance = Ins.objects.all()
    return render(request, "user-tables.html",{'ins': insurance})


def kyc(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            form=Form()
            form.email=request.POST.get('email')
            form.password=request.POST.get('password')
            form.save()

            return render(request, "kyc.html")
    else:

            return render(request, "kyc.html")

def pie_chart(request):
    labels = []
    data = []

    insurance = Ins.objects.order_by('-id')[:5]
    for city in insurance:
        labels.append(city.fname)
        data.append(city.id)

    return render(request, 'pie_chart.html', {
        'labels': labels,
        'data': data,
    })
    

def pie_chart2(request):
    labels = []
    data = []

    insurance = Ins.objects.order_by('-id')[:5]
    for city in insurance:
        labels.append(city.lname)
        data.append(city.id)

    return render(request, 'pie_chart2.html', {
        'labels': labels,
        'data': data,
    })

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        insurance = Ins.objects.filter(id__icontains = q)
        return render(request, "hodtemp/user-tables.html",{'ins': insurance})

def export_csv_user(request):
    insurance=Ins.objects.all()
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="userdata.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID','First Name','Last Name'])
   
    for data in insurance:
        writer.writerow([data.id ,data.fname, data.lname])

    return response


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
         
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
