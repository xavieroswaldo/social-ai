from django.contrib import admin
from .models import BusinessType, MarketingObjective, GeneratedPost, GeneratedPoster


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )


@admin.register(MarketingObjective)
class MarketingObjectiveAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )


@admin.register(GeneratedPost)
class GeneratedPostAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "user",
        "business",
        "business_type",
        "platform",
        "is_favorite",
        "created_at",
    )

    list_filter = (
        "platform",
        "is_favorite",
        "created_at",
    )

    search_fields = (
        "title",
        "product_name",
        "generated_text",
    )

admin.site.register(GeneratedPoster)