from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categorys(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    base_price = models.IntegerField()
    image = models.CharField(max_length=7000)
    category = models.ForeignKey( Categorys, on_delete=models.CASCADE,related_name="category", default='1')
    add_user = models.ForeignKey(User, related_name="add_user", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"(({self.id})){self.title}: base price={self.base_price}"
    
class Watchlist(models.Model):
    actives = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="actives")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="watchlit_owne")
    
    def __str__(self):
        return f"{self.actives} on {self.user} watchlist"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comment_user", on_delete=models.CASCADE)
    comment = models.CharField( max_length=100)
    active = models.ForeignKey(Listing, related_name="comment_active", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} commented {self.comment} on {self.active}"
    
    
class Bids(models.Model):
    user = models.ForeignKey(User, related_name="bid_user", on_delete=models.CASCADE)
    price = models.IntegerField()
    active = models.ForeignKey(Listing, related_name="bid_active", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} porpos {self.price} on {self.active}"
 