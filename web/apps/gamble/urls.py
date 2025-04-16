from django.urls import path
from .views import RegisterView, RegisteredUserList

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("api/users/", RegisteredUserList.as_view(), name="user-list"),
]
