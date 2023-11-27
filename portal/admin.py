import django
from django.contrib import admindocs
from django.contrib.auth.models import User
from django.contrib import admin
from django.apps import apps
# Register your models here.
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    
    except django.contrib.admin.sites.AlreadyRegistered:
        pass