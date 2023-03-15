from django.db.models.signals import post_save, post_delete


from .models import Profile, User

def createprofile(sender, instance, created, **kwargs):
    print('create profile')
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
        )
        
def deleteuser(sender, instance, **kwargs):
    print('delete fired')
    user = instance.user
    user.delete()
    
post_save.connect(createprofile, sender=User)
post_delete.connect(deleteuser, sender=Profile)
