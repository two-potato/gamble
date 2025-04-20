from django.urls import path
from .views import (
    RegisterView,
    RegisteredUserList,
    SuccessView,
    PrivatPolicyView,
    NotSubscribedView,
    AlreadySubscribedView,
)

app_name = "gamble"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("register/success", SuccessView.as_view(), name="success"),
    path("register/not_subscribed", NotSubscribedView.as_view(), name="not_subscribed"),
    path(
        "register/already_subscribed",
        AlreadySubscribedView.as_view(),
        name="already_subscribed",
    ),
    path("register/private_policy", PrivatPolicyView.as_view(), name="private_policy"),
    path("api/users/", RegisteredUserList.as_view(), name="user-list"),
]
