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

register = template.Library()

def home(request):
        if request.method == 'GET':
                return render(request, "main/index.html")
        else:
                return HttpResponse("Method not allowed on /.", status=405)
        
@sensitive_post_parameters('userid')
def specificUser(request, user_id):
        if request.method == 'GET':
                if request.user.is_authenticated:
                        userid = request.user.id
                        user = User.objects.get(pk=userid)
                        m = hashlib.md5()
                        m.update(user.email.encode("utf-8"))
                        #m.digest()
                        default = "https://www.gravatar.com/avatar/"
                        url = default + m.hexdigest()
                        print(url)
                        return HttpResponse(render(request, 'main/specificUser.html', {'user' : user, 'url' : url}), status = 200)
                        
                else:
                        return HttpResponseRedirect("/auth/signin")
        else:
                return HttpResponse("Method not allowed on /main/users/.", status = 405)