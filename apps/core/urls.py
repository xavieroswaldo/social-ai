from django.urls import path
from .views import home, about, privacy_policy, contact, admin_dashboard, toggle_user_plan

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("contact/", contact, name="contact"),
    path("admin-dashboard/",admin_dashboard,name="admin_dashboard"),
    path("toggle-user-plan/<int:user_id>/",toggle_user_plan,name="toggle_user_plan"),
    path("toggle-user-plan/<int:user_id>/",toggle_user_plan, name="toggle_user_plan"),
]
