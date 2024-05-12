import os
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from django.conf import settings
from .models import ClothingItem, Profile
from django.http import HttpResponseRedirect
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
    dont_has_picture = True
    if request.user.profile.picture:
        dont_has_picture = False
    if request.method == 'POST':
        new_clothing_item = ClothingItem(
        image = request.FILES.get('clothing-image'),
        name = request.POST.get('name'),
        description = request.POST.get('description'),
        price = request.POST.get('price'),
        owner = request.user  
        )
        new_clothing_item.save()
        return HttpResponseRedirect(reverse('core:personal_page')) 
    return render(request, 'add_clothing_item.html', {'dont_has_picture': dont_has_picture})

def user_clothing_items(request):
    user_clothing_items = ClothingItem.objects.filter(owner=request.user)
    context = {
        'user_clothing_items': user_clothing_items
    }
    return render(request, 'user_clothing_items.html', context)

def detail_item(request, item_id):
    item = ClothingItem.objects.get(id=item_id)
    return render(request, 'detail_item.html', {'item': item})

def remove_item(request, item_id):
    item = get_object_or_404(ClothingItem, pk=item_id)
    item.delete()
    return HttpResponseRedirect(reverse('core:personal_page')) 


def add_favorite(request, item_id):
    item = get_object_or_404(ClothingItem, pk=item_id)
    profile = request.user.profile  # Assuming you have a Profile model associated with User

    # Assign the item as the favorite clothing item for the user's profile
    profile.favorite_clothing_item = item
    profile.save()

    # Redirect to a relevant page
    return redirect('core:detail_item', item_id=item_id)

