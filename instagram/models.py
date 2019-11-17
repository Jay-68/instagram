# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Image(models.Model):
    post = models.ImageField(upload_to='images/', blank=True)
    caption = HTMLField()
    posted_on = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null='True')

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['posted_on']

    def save_img(self):
        self.save()

    def delete_img(self):
        self.delete()
