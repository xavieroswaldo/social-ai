from django.urls import path

from .views import (
    business_list,
    business_create,
    business_update,
    business_delete,
    set_active_business,
)

urlpatterns = [
    path("", business_list, name="business_list"),
    path("create/", business_create, name="business_create"),
    path("update/<int:pk>/", business_update, name="business_update"),
    path("delete/<int:pk>/", business_delete, name="business_delete"),
    path("set-active/<int:pk>/", set_active_business, name="set_active_business"),
]
