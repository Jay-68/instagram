# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Image, Profile, Comments, Likes
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block

# Create your views here.
# @login_required(login_url='/accounts/login/')
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
