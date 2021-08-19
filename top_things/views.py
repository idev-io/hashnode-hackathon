from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import ThingCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
import os
from .models import Thing, Category
from .utils import is_valid_queryparam


####### Authentication #######
# Logout Page
@login_required
def logout_page(request):
    logout(request)
    messages.success(request, "You logged out successfully")
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://localhost:8000'
    link = f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}'
    return redirect(link)


####### Frontend #######
# Home Page 
def home_page(request):
    things = Thing.objects.filter().order_by('-id')[0:3]

    context={
        'things': things,
    }
    return render(request, 'index.html', context)


# Things Page
def things(request):
    query = Thing.objects.all().order_by('-id')
    categories = Category.objects.all()

    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

    RANK_CHOICES = {
        BEGINNER: 'Beginner',
        INTERMEDIATE: 'Intermediate',
        ADVANCED: 'Advanced'
    }

    levels = RANK_CHOICES

    title_contains_query = request.GET.get('title_contains')
    category = request.GET.get('category')
    level = request.GET.get('level')

    if is_valid_queryparam(title_contains_query):
        query = query.filter(title__icontains=title_contains_query)

    if is_valid_queryparam(category) and category != '--Choose Category--':
        query = query.filter(category_id__category=category)
    
    if is_valid_queryparam(level) and level != '--Choose Level--':
        query = query.filter(rank__icontains=level)


    page = request.GET.get('page',1)
    paginator = Paginator(query,9)

    try:
        things = paginator.page(page)
    except PageNotAnInteger:
        things = paginator.page(1)
    except EmptyPage:
        things = paginator.page(paginator.num_pages)

    context={
        'things': things,
        'categories': categories,
        'levels': levels
    }
    return render(request, 'frontend/things.html', context)
    


# Single Thing Page
def single_thing(request, slug):
    thing = get_object_or_404(Thing, slug=slug)

    context = {
        'thing': thing
    }

    return render(request, 'frontend/single_thing.html', context)


# About Page
def about(request):
    return render(request, 'frontend/about.html')


####### Backend ####### 
# User Dashboard
@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')

    things = Thing.objects.filter(user=user).count()
    last_created_things = Thing.objects.filter(user=user).order_by('-id')[0:3]

    userdata = {
        'user_id': auth0user.uid,
        'name': user.username,
        'picture': auth0user.extra_data['picture'],
    }

    context = {
        'userdata': userdata,
        'things': things,
        'last_created_things': last_created_things
    }

    return render(request, 'backend/user_dashboard.html', context)


# Create Thing
@login_required
def create_thing(request):
    user = request.user
    try:
        form = ThingCreateForm()
        if request.method == 'POST':
            form = ThingCreateForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                thing = form.save(commit=False)
                thing.user = user
                thing.save()
                messages.success(request, "Created successfully")

                return redirect('topthings:things')

    except ObjectDoesNotExist:
        return redirect('topthings:home')

    context = {
        'form': form
    }

    return render(request, 'backend/create_thing.html', context)


# Edit Thing
@login_required
def edit_thing(request, slug):
    thing = Thing.objects.get(slug=slug)

    old_image = thing.picture.path

    form = ThingCreateForm(instance=thing)
    if request.method == 'POST':
        form = ThingCreateForm(request.POST or None, request.FILES or None, instance=thing)
        if form.is_valid():
            new_thing = form.save(commit=False)
            if new_thing.picture.path != old_image:
                os.remove(old_image)
            else:
                new_thing.picture = thing.picture

            new_thing.save()
            messages.info(request, "Edited successfully")

            return redirect('topthings:things')

    context = {
        'form': form,
    }
    return render(request, 'backend/edit_thing.html', context)


# Delete Thing
@login_required
def delete_thing(request, slug):
    user = request.user
    
    thing = get_object_or_404(Thing, slug=slug)
    creator= thing.user.username

    if request.method == "POST" and user.is_authenticated and user.username == creator:
        if len(thing.picture) > 0:
            os.remove(thing.picture.path)
        thing.delete()
        messages.success(request, "Deleted successfully")
        return redirect('topthings:things')
        
    
    context = {
        'thing': thing
    }
    return render(request, 'frontend/things.html', context)


# 404 error page
def error_page(request, exception):
    context = {}
    return render(request,'404.html', context)

