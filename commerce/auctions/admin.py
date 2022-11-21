from django.contrib import admin
from .models import User, Active_list, Categorys

# Register your models here.
admin.site.register(Active_list)
admin.site.register(Categorys)