from django.db import models

import random
import string


class Settings(models.Model):
    default_hash = models.CharField(max_length=30)


class PersonSet(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=30, primary_key=True)  # Random number to share a link with your play set


class Person(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='people')
    person_set = models.ForeignKey(PersonSet, on_delete=models.CASCADE)
