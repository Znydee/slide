"""slide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users.views import register,send_friend_request,cancel_friend_request,accept_friend_request, decline_friend_request,like_post,notifications_as_read,get_all_notifications,profileupdate
from chat.views import mark_specific_as_read
from django.contrib.auth import views as auth_views
import notifications.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
     path('chat', include('chat.urls')),
    path('login/',auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    
    path('logout',auth_views.LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    path('profileupdate/',profileupdate,name="profileupdate" ),
    path('register',register,name="register"),
    path('sendrequest',send_friend_request,name="send-request"),
    path('cancelrequest',cancel_friend_request,name="cancel-request"),
    path('acceptrequest',accept_friend_request,name="accept-request"),
    path('declinerequest', decline_friend_request,name="decline-request"),
    path('likepost', like_post,name="like-post"),
    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('readnotification', notifications_as_read,name="mark-notification-as-read"),
    path('getallnotifications', get_all_notifications,name="get-all-notifications"),
    path("password-reset/",auth_views.PasswordResetView.as_view(template_name="users/password_reset.html") , name="password_reset"),
    path("password-reset/done",auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html") , name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html") , name="password_reset_confirm"),
    path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html") , name="password_reset_complete"),
    path('mark_specific_as_read',mark_specific_as_read,name="message_as_read"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)