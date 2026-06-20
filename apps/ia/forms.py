from django import forms

from .models import BusinessType, MarketingObjective


class GeneratePostForm(forms.Form):
    TONE_CHOICES = [
        ("", "Usar tono del negocio"),
        ("friendly", "Amigable"),
        ("professional", "Profesional"),
        ("funny", "Divertido"),
        ("elegant", "Elegante"),
    ]

    objective = forms.ModelChoiceField(
        queryset=MarketingObjective.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    platform = forms.ChoiceField(
        choices=[
            ("instagram", "Instagram"),
            ("facebook", "Facebook"),
            ("whatsapp", "WhatsApp"),
            #("tiktok", "TikTok"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    product_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: Cappuccino 2x1"}
        ),
    )

    tone_override = forms.ChoiceField(
        choices=TONE_CHOICES,
        required=False,
        label="Tono de esta publicación",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
