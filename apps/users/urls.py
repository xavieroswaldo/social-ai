from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, logout_view, register_view, my_plan, upgrade_plan, profile_view, verify_email


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    path("my-plan/",my_plan, name="my_plan"),
    path("upgrade-plan/",upgrade_plan, name="upgrade_plan"), 
    #path("activate-premium/",activate_premium, name="activate_premium"),
    path("profile/",profile_view,name="profile"),
    path("verify-email/<uidb64>/<token>/",verify_email,name="verify_email"),
]
