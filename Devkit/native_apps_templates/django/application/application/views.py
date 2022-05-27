from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import yaml
import os

config_path = os.path.join(settings.BASE_DIR, 'config.yaml')
with open(config_path) as yaml_file:
	config = yaml.safe_load(yaml_file)


def index(request):
    return render(request=request,
                  template_name="index.html",
                  context={})

@login_required(login_url='/Login')
def logout_view(request):
    logout(request)
    return render(request=request,
                  template_name="index.html",
                  context={})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("<p> The username or password is incorrect, <a href='/Login'>Return back</a> </p>")
    return render(request=request,
                  template_name="login.html",
                  context={})

def Registration(request, *args, **kwargs):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('secretcode')
        if User.objects.filter(username=email).exists():
            return HttpResponse("<p>User with same email id exists, try with different email id !  <a href='/Register'>Return back</a> </p>")
        else:
            user = User.objects.create_user(username=email,
                                            password=password,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name)
            user.save()

        if user:
            auth_login(request, user)
            return HttpResponseRedirect('/')
    return render(request, template_name="signup.html", context={})
