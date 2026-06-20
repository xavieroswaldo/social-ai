from django.contrib import admin

from .models import BusinessProfile


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "business_name",
        "user",
        "business_type",
        "city",
        "phone",
        "instagram",
        "communication_tone",
    )

    search_fields = (
        "business_name",
        "city",
    )

    list_filter = (
        "business_type",
        "communication_tone",
    )
