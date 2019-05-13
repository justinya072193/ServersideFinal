from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
#from django_gravatar.helpers import get_gravatar_url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.safestring import mark_safe
import hashlib
from django import template
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt

register = template.Library()

@csrf_exempt
def home(request):
    if request.method == 'GET':
        return render(request, 'main/index.html', status=200)
    else:
        return HttpResponse("Method not allowed on /.", status=405)