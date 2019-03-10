# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class SpotPost(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField(max_length=100)
	photo = models.ImageField(upload_to="spot/%Y/%m/%d")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	latitude = models.CharField(max_length=100)
	longitude = models.CharField(max_length=100)
	spot_user = models.ForeignKey(User, related_name='spot_poster')

	def __str__(self):
		return self.title

class StreetPost(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	category =  models.CharField(max_length=100)
	city =  models.CharField(max_length=100)
	spots = models.ManyToManyField(SpotPost)
	user = models.ForeignKey(User, related_name='poster')
	recommends = models.ManyToManyField(User, blank=True, related_name='recommend_post')

	def __str__(self):
		return self.title

	def total_recommend(self):
		return self.recommends.count()

	def get_absolute_url(self):
		return reverse("street_detail", kwargs={"pk" : self.pk })