from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from .models import Profile

def initial_page(request):
    return  render(request, 'initial_page.html')

def join_page(request):
    return  render(request, 'join_page.html')

def personal_page(request):
    dont_has_picture = True
    if request.user.profile.picture:
        dont_has_picture = False
    return render(request, 'personal_page.html', {'dont_has_picture': dont_has_picture})

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

def login_handler(request):
    if request.method == 'POST':
        username = request.POST.get('name')  
        password = request.POST.get('password')
        if username is not None and password is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('core:initial_page'))
            else:
                response = """
                    <script>
                        alert('Invalid username or password. Please try again.');
                        window.location.href = '{0}';
                    </script>
                """.format(reverse('core:join_page'))
                return HttpResponse(response)
        else:
            response = """
                <script>
                    alert('Please provide both username and password.');
                    window.location.href = '{0}';
                </script>
            """.format(reverse('core:join_page'))
            return HttpResponse(response)


def logout_handler(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:initial_page'))

def signin_handler(request):
    if request.method == 'POST':
        username = str(request.POST['name'])
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile(user=user)
        profile.save()
        login(request, user)
        return HttpResponseRedirect(reverse('core:initial_page'))
    else:
        return render(request, 'intial_page.html')


