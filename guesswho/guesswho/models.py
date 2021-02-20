from django.db import models

class PersonSet(models.Model):
    hash = models.CharField(max_length=30) # Random number to share a link with your play set
    # PersonSet.person_set.all() will contain all persons

class Person(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='people')
    person_set = models.ForeignKey(PersonSet, on_delete=models.CASCADE)