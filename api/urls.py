from django.contrib import admin
from django.urls import path
from api.views import register, login, update_score, get_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/', login),
    path('update-score/', update_score),
    path('get-user/', get_user),
]