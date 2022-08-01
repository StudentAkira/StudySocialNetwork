from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import TokenLogin, CheckAuth, GetUserAPIView, GetUsers, NewUserAPIView, ChangeAvatar, CreateNewPostAPIView, GetPosts, GetPostAPIView
from django.conf import settings

urlpatterns = [
    path('registrate/', NewUserAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.authtoken')),
    path('getToken/', TokenLogin.as_view()),
    path('me/', CheckAuth.as_view()),
    path('user/<int:pk>/', GetUserAPIView.as_view()),
    path('users/<int:pk>', GetUsers.as_view()),
    path('post/<int:pk>/', GetPostAPIView.as_view()),
    path('posts/<int:pk>', GetPosts.as_view()),
    path('changeavatar/', ChangeAvatar.as_view()),


    path('', include('social_django.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

    path('test/', CreateNewPostAPIView.as_view()),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
