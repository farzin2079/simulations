from django.contrib import admin
from .models import Post ,Follow, Profile, User
# Register your models here.
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Profile)
