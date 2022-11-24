from django.contrib import admin
from .models import User, Listing, Categorys, Watchlist, Comment,Bids

# Register your models here.
admin.site.register(Listing)
admin.site.register(Categorys)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bids)