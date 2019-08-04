from django.contrib import admin
from .models import saved, recent, category

# Register your models here.
admin.site.register(saved)
admin.site.register(recent)
admin.site.register(category)