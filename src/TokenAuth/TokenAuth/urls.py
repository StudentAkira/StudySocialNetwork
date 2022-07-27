from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import TokenLogin, CheckAuth, GetUserAPIView
from .settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.authtoken')),
    path('getToken/', TokenLogin.as_view()),
    path('me/', CheckAuth.as_view()),
    path('user/<int:pk>/', GetUserAPIView.as_view()),

    path('', include('social_django.urls')),

]
urlpatterns+=static('/', document_root=MEDIA_ROOT)
