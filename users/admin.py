from django.contrib import admin
from .models import Profile, FriendRequests,Posts,Comment
# Register your models here.
admin.site.register(Profile)
admin.site.register(FriendRequests)
admin.site.register(Posts)
admin.site.register(Comment)