from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserSubscription

admin.site.register(User, UserAdmin)
@admin.register(UserSubscription)

class UserSubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "plan",
        "posts_generated",
        "images_generated",
    )

    list_filter = (
        "plan",
    )

    search_fields = (
        "user__username",
        "user__email",
    )
