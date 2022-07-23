from django.contrib import admin
from django.urls import path, include

from accounts.views import TestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test1/', include('djoser.urls')),
    path('test2/', include('djoser.urls.authtoken')),

    path('onlyfans/', TestView.as_view()),
]
