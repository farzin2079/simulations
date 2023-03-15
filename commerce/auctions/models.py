from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True)
    

class Categorys(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='%m/', blank=True, null=True)
    description = models.CharField(max_length=100)
    base_price = models.IntegerField()
    category = models.ForeignKey( 'Categorys', on_delete=models.CASCADE,related_name="category", default='1')
    add_user = models.ForeignKey(User, related_name="add_user", on_delete=models.CASCADE)
    bids = models.ForeignKey("Bids",on_delete=models.PROTECT, blank=True, null=True)
    
    def __str__(self):
        return f"(({self.id})){self.title}: base price={self.base_price}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comment_user", on_delete=models.CASCADE)
    comment = models.CharField( max_length=100)
    listing = models.ForeignKey(Listing, related_name="comment_active", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} commented {self.comment} on {self.active}"
    
    
class Bids(models.Model):
    user = models.ForeignKey(User, related_name="bid_user", on_delete=models.CASCADE)
    price = models.IntegerField()
    
    def __str__(self):
        return f"{self.user} porpos {self.price} on {self.active}"
 