# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Image, Profile, Comments, Likes
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    '''
    Function that returns website application landing page.
    '''
    images = Image.get_images().order_by('-posted_on')
    profiles = User.objects.all()
    people = Follow.objects.following(request.user)
    comments = Comments.objects.all()
    likes = Likes.objects.all()

    return render(request, 'index.html', {'images': images, 'profiles': profiles, 'people': people, 'comments': comments, 'likes': likes})


@login_required(login_url='/accounts/login/')
def new_post(request):
    """
    Function that enables one to upload images
    """
    profile = Profile.objects.all()
    for profile in profile:

        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.profile = profile
                image.user = request.user
                image.save()
            return redirect('landing')
        else:
            form = ImageForm()
    return render(request, 'new_post.html', {"form": form})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    """
    Function that enables one to edit their profile information
    """
    current_user = request.user
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
        return redirect('landing')
    else:
        form = ProfileForm()
    return render(request, 'profile/edit-profile.html', {"form": form, })


@login_required(login_url='/accounts/login/')
def follow(request, user_id):
    other_user = User.objects.get(id=user_id)
    follow = Follow.objects.add_follower(request.user, other_user)

    return redirect('landing')


@login_required(login_url='/accounts/login/')
def unfollow(request, user_id):
    other_user = User.objects.get(id=user_id)

    follow = Follow.objects.remove_follower(request.user, other_user)

    return redirect('landing')


@login_required(login_url='/accounts/login/')
def search_user(request):
    """
    Function that searches for profiles based on the usernames
    """
    if 'username' in request.GET and request.GET["username"]:
        name = request.GET.get("username")
        searched_profiles = User.objects.filter(username__icontains=name)
        message = f"{name}"
        profiles = User.objects.all()
        people = Follow.objects.following(request.user)
        print(profiles)
        return render(request, 'search.html', {"message": message, "usernames": searched_profiles, "profiles": profiles, })

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def add_comment(request, image_id):
    images = get_object_or_404(Image, pk=image_id)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = images
            comment.save()
    return redirect('landing')


@login_required(login_url='/accounts/login/')
def like_post(request):
    image = get_object_or_404(Image, id=request.POST.get('image_id'))
    image.likes.add(request.user)
    return redirect('landing')
