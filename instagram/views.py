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
def like_post(request):
    image = get_object_or_404(Image, id=request.POST.get('image_id'))
    image.likes.add(request.user)
    return redirect('landing')
