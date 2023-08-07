from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name = "account"

urlpatterns = [
    # ------------------------------------------------------------
    # Django auth
    # ------------------------------------------------------------
    path("", include("django.contrib.auth.urls")),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "profile/",
        TemplateView.as_view(template_name="account/profile.html"),
        name="profile",
    ),
    # ------------------------------------------------------------
    # Social auth
    # ------------------------------------------------------------
    # https://python-social-auth.readthedocs.io/en/latest/configuration/django.html#urls-entries
    # path("social-auth/", include("social_django.urls", namespace="social")),
]
