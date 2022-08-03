from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import (
    TokenLoginAPIView,
    CheckAuthAPIView,
    GetUserAPIView,
    GetUsersAPIView,
    NewUserAPIView,
    ChangeAvatarAPIView,
    CreateNewPostAPIView,
    GetPostsAPIView,
    GetPostAPIView,
    EditPostAPIView,
    DeletePostAPIView
    )
from django.conf import settings

urlpatterns = [
    path('registrate/', NewUserAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.authtoken')),
    path('getToken/', TokenLoginAPIView.as_view()),
    path('me/', CheckAuthAPIView.as_view()),
    path('user/<int:pk>/', GetUserAPIView.as_view()),
    path('users/<int:pk>', GetUsersAPIView.as_view()),
    path('post/<int:pk>/', GetPostAPIView.as_view()),
    path('posts/<int:pk>', GetPostsAPIView.as_view()),
    path('changeavatar/', ChangeAvatarAPIView.as_view()),
    path('createpost/', CreateNewPostAPIView.as_view()),
    path('editpost/<int:pk>/', EditPostAPIView.as_view()),
    path('deletepost/<int:pk>/', DeletePostAPIView.as_view()),

    path('', include('social_django.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
