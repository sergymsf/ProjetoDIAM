import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from django.conf import settings
from .models import ClothingItem, Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage


def initial_page(request):
    return  render(request, 'initial_page.html')

def join_page(request):
    return  render(request, 'join_page.html')

@login_required(login_url=  'core:join_page')
def personal_page(request):
    dont_has_picture = True
    if request.user.profile.picture:
        dont_has_picture = False
    return render(request, 'personal_page.html', {'dont_has_picture': dont_has_picture})

@login_required(login_url=  'core:join_page')
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        if 'profile-picture' in request.FILES:
            if profile.picture:
                file_path = profile.picture.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            username = request.user.username
            file_extension = ".png"
            stri = str(username) +file_extension
            myfile = request.FILES['profile-picture']
            fs = FileSystemStorage()
            filename = fs.save(stri, myfile)
            profile.picture = filename 
        if 'bio' in request.POST:
            profile.bio = request.POST['bio']
        profile.save()
        return HttpResponseRedirect(reverse('core:personal_page'))

    return render(request, 'edit_page.html', {'profile': profile})

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


@login_required(login_url=  'core:join_page')
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
    

@login_required(login_url=  'core:join_page')
def add_clothing_item(request):
    if request.method == 'POST':
        image = request.FILES.get('clothing-image')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        owner = request.user  

        new_clothing_item = ClothingItem.objects.create(
            owner=owner,
            image=image,
            name=name,
            description=description,
            price=price
        )
        return redirect('personal_page.html')  # Redirect to the clothing item list page
    
    return render(request, 'add_clothing_item.html')


