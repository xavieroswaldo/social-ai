from django.db import models
from django.conf import settings
from apps.ia.models import BusinessType


class BusinessProfile(models.Model):

    TONE_CHOICES = [
        ("friendly", "Amigable"),
        ("professional", "Profesional"),
        ("funny", "Divertido"),
        ("elegant", "Elegante"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="businesses"
    )

    business_name = models.CharField(max_length=255)

    business_type = models.ForeignKey(
        BusinessType, on_delete=models.SET_NULL, null=True
    )

    city = models.CharField(max_length=100)

    description = models.TextField()

    target_audience = models.TextField()

    communication_tone = models.CharField(max_length=20, choices=TONE_CHOICES)

    phone = models.CharField(max_length=30, blank=True)

    address = models.CharField(max_length=255, blank=True)

    instagram = models.CharField(max_length=100, blank=True)

    facebook = models.CharField(max_length=100, blank=True)

    tiktok = models.CharField(max_length=100, blank=True)

    website = models.URLField(blank=True)

    value_proposition = models.TextField(
        blank=True, help_text="¿Qué hace único a tu negocio?"
    )
    logo = models.ImageField(upload_to="business_logos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "Business Profile"

        verbose_name_plural = "Business Profiles"

    def __str__(self):

        return self.business_name
