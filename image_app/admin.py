from django.contrib import admin
from .models import Files, Category

# Register your models here.
admin.site.register([Files, Category])