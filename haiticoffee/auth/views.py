from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm, RegistrationForm
from django.contrib.auth.models import User
from haitiApp.models import Customer
from rest_framework import status
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@sensitive_post_parameters('username','password','passwordconf','email','first_name','last_name')
@csrf_exempt
def register(request):
        """
        Render a new user form on GET request.
        Register new user in database on POST request.
        """
        if request.method == 'GET':
            return HttpResponse(render(request, "auth/register.html", {'form' : RegistrationForm}), status = 200)
        elif request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                passwordconf = form.cleaned_data.get('passwordconf')
                email = form.cleaned_data.get('email')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                if(password != passwordconf):
                        return HttpResponse("Passwords did not match.", status=400) 
                user, created = User.objects.get_or_create(username=username, email = email, 
                        first_name = first_name, last_name = last_name)
                user.set_password(password)
                user.save()
                newCustomer = Customer.objects.create(user = user)
                newCustomer.save()
                return HttpResponseRedirect("/auth/signin")
            else:
                return HttpResponse("Invalid registration request.", status = 405)
        else:
            return HttpResponse("Method not allowed on /auth/register.", status = 405)

@sensitive_post_parameters('username','password')
@csrf_exempt
def signin(request):
    """
    Render login form on GET request.
    Log in user on POST request.
    """
    if request.user.is_authenticated:
        return HttpResponse("You are already signed in!", status=status.HTTP_200_OK)
    if request.method == 'GET':
        return HttpResponse(render(request, "auth/signin.html", {'form' : SigninForm}), status = 200)
    elif request.method == 'POST':
        postdata = request.POST.copy()
        username = postdata.get('username','')
        password = postdata.get('password', '')
        user = authenticate(username = username, password = password)
        if user is not None:
            #print('success')
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid credentials.", status = 401)
    else:
        return HttpResponse("Bad login form.", status = 400)

@csrf_exempt
def signout(request):
    """
    Signs user out on GET request.
    """
    if request.method == 'GET':
        if (request.user.is_authenticated) :
            logout(request)
            return HttpResponse("Sign out successful", status=200)
        else :
            return HttpResponse("Not logged in", status=200)
    else:
        return HttpResponse("Method not allowed on auth/signout.", status = 405)

@csrf_exempt
@login_required(login_url='/auth/signin')
def testAdmin(request):
    """
    Turns current user account into Admin account for testing purposes.
    """
    if request.method == "PATCH":
        currCustomer = Customer.objects.get(user=request.user)
        currCustomer.isAdmin = True
        currCustomer.save()
        print(currCustomer)
        return HttpResponse('Your user account now has admin access', status=status.HTTP_200_OK)