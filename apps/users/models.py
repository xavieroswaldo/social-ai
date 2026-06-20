from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(unique=True)

    email_verified = models.BooleanField(
        default=False
    )

    identification = models.CharField(
        max_length=20,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

class UserSubscription(models.Model):

    PLAN_CHOICES = [
        ("free", "Gratis"),
        ("premium", "Premium"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="free"
    )

    posts_generated = models.IntegerField(default=0)

    images_generated = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    businesses_deleted = models.PositiveIntegerField(
        default=0)

    def __str__(self):

        return f"{self.user.username} - {self.plan}"