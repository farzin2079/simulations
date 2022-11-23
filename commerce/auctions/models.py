from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categorys(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}"

class Active_list(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    base_price = models.IntegerField()
    porpose_price = models.IntegerField(default=0)
    image = models.CharField(max_length=7000)
    category = models.ForeignKey( Categorys, on_delete=models.CASCADE,related_name="category", default='1')
    add_user = models.ForeignKey(User, related_name="add_user", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id}=title:{self.title}, base price: {self.base_price}"
    
class Watchlist(models.Model):
    actives = models.ForeignKey(Active_list, on_delete=models.CASCADE, blank=True, related_name="actives")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return f"{self.actives}"
    
    