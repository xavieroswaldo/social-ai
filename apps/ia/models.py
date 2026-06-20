from django.db import models
from django.conf import settings


class BusinessType(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):

        return self.name


class MarketingObjective(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):

        return self.name


class GeneratedPost(models.Model):

    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("whatsapp", "WhatsApp"),
        #("tiktok", "TikTok"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    business = models.ForeignKey(
        "business.BusinessProfile", on_delete=models.CASCADE, null=True, blank=True
    )

    business_type = models.ForeignKey(
        BusinessType, on_delete=models.SET_NULL, null=True
    )

    objective = models.ForeignKey(
        MarketingObjective, on_delete=models.SET_NULL, null=True
    )

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)

    
    title = models.CharField(max_length=200)

    product_name = models.CharField(max_length=255)

    prompt = models.TextField()

    generated_text = models.TextField()

    photo_idea = models.TextField(blank=True)

    is_favorite = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)  

    professional_text = models.TextField(blank=True)

    friendly_text = models.TextField(blank=True)

    funny_text = models.TextField(blank=True)

    def __str__(self):

        return f"{self.title} - {self.user.username}"


class GeneratedImage(models.Model):

    generated_post = models.ForeignKey(
        GeneratedPost,
        on_delete=models.CASCADE,
        related_name="images"
    )

    prompt = models.TextField()

    image = models.ImageField(
        upload_to="generated_images/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Imagen {self.id}"
    
class GeneratedPoster(models.Model):

    generated_post = models.ForeignKey(
        GeneratedPost,
        on_delete=models.CASCADE,
        related_name="posters"
    )

    image = models.ImageField(
        upload_to="generated_posters/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Poster {self.id}"