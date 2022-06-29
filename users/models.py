from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete = models.CASCADE)
    bio = models.TextField(blank=True)
    image=models.ImageField(default="default.jpg" , upload_to="profile_pictures")
    slug = AutoSlugField(populate_from='user',always_update=True)
    friends= models.ManyToManyField(User,related_name="friends_list", blank=True)
    def __str__(self):
        return f"{self.user.username}'s profile"
class Posts(models.Model):
    user=models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)       
    post=models.TextField(blank=False)
    date_posted=models.            DateTimeField(auto_now_add=True)
    
class FriendRequests(models.Model):
    sent_from = models.ForeignKey(User,related_name="request_sent",on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User,related_name="request_recieved",on_delete=models.CASCADE)
    time_sent= models.            DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"from{self.sent_from.username} to {self.sent_to.username}"