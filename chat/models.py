from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="messages_sent", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="messages_recieved",on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    #tt=models.CharField(max_length=512,blank=True)

    def __str__(self):
        return f"sent from {self.sender} to {self.reciever}"