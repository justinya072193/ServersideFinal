from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm, RegistrationForm
from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_post_parameters

@sensitive_post_parameters('username','password','passwordconf','email','first_name','last_name')
def register(request):
        if request.method == 'GET':
                #print('aaa')
                return HttpResponse(render(request, "auth/register.html", {'form' : RegistrationForm}), status = 200)
        elif request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        #form.save()
                        username = form.cleaned_data.get('username')
                        password = form.cleaned_data.get('password')
                        passwordconf = form.cleaned_data.get('passwordconf')
                        email = form.cleaned_data.get('email')
                        first_name = form.cleaned_data.get('first_name')
                        last_name = form.cleaned_data.get('last_name')
                        #print(fName)
                        if(password != passwordconf):
                                return HttpResponse("Passwords did not match.", status=400) 
                        user, created = User.objects.get_or_create(username=username, email = email, 
                                first_name = first_name, last_name = last_name)
                        user.set_password(password)

                        user.save()
                        return HttpResponseRedirect("/auth/signin")
                else:
                        return HttpResponse("Invalid registration request.", status = 405)
        else:
                return HttpResponse("Method not allowed on /auth/register.", status = 405)

@sensitive_post_parameters('username','password')
def signin(request):
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


def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse("Sign out successful.", status = 200)
        else:
            return HttpResponse("Not logged in.", status = 200)
    else:
        return HttpResponse("Method not allowed on auth/signout.", status = 405)


