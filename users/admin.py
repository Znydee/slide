from django.contrib import admin
from .models import Profile, FriendRequests,Posts,Comment,Like
# Register your models here.
admin.site.register(Profile)
admin.site.register(FriendRequests)
admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Like)