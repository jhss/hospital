# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class join_eval(models.Model):
	ykiho = models.TextField(primary_key=True)
	name  = models.TextField()
	addr  = models.TextField()
	srch_list  = ArrayField(models.IntegerField(null = True, blank= True), null=True, blank=True)
	asmGrdList  = ArrayField(models.IntegerField(null = True, blank= True), null=True, blank=True)
	#top5  = models.TextField()

