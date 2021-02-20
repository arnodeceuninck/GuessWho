from django.db import models

import random
import string


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


class PersonSet(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=30, primary_key=True)  # Random number to share a link with your play set

    def __init__(self, name, user_id, *args, **kwargs):
        super().__init__()
        self.hash = get_random_alphanumeric_string(5)
        while PersonSet.objects.filter(hash=self.hash).count():
            self.hash = get_random_alphanumeric_string(5)
        self.name = name
        self.user_id = user_id


class Person(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='people')
    person_set = models.ForeignKey(PersonSet, on_delete=models.CASCADE)
