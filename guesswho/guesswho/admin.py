from django.contrib import admin
from .models import PersonSet, Person, Settings


class PersonInline(admin.StackedInline):
    model = Person


class PersonSetAdmin(admin.ModelAdmin):
    model = PersonSet
    inlines = [PersonInline]


admin.site.register(PersonSet, PersonSetAdmin)
admin.site.register(Settings)
