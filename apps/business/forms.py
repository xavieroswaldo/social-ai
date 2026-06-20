from django import forms

from .models import BusinessProfile


class BusinessProfileForm(forms.ModelForm):

    class Meta:

        model = BusinessProfile

        fields = [
            "business_name",
            "business_type",
            "city",
            "description",
            "target_audience",
            "communication_tone",
            "phone",
            "address",
            "instagram",
            "facebook",
            "tiktok",
            "website",
            "value_proposition",
            #"logo",
        ]

        widgets = {
            "business_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del negocio"}),
            "business_type": forms.Select(attrs={"class": "form-select"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ciudad"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Descripción de su negocio"}),
            "target_audience": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "Público objetivo"}
            ),
            "communication_tone": forms.Select(attrs={"class": "form-select"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono de contacto"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dirección"}),
            "instagram": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese su cuenta"}),
            "facebook": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese su cuenta"}),
            "tiktok": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese su cuenta"}),
            "website": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese su link"}),
            "value_proposition": forms.Textarea(
                attrs={"class": "form-control", "rows": 2,"placeholder": "Ingrese la propuesta de valor de su negocio" }
            ),
        }

class BusinessProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = BusinessProfile

        fields = [
            "business_name",
            "city",
            "description",
            "target_audience",
            "communication_tone",
            "phone",
            "address",
            "instagram",
            "facebook",
            "tiktok",
            "website",
            "value_proposition",
        ]

        widgets = {
            "business_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "target_audience": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "communication_tone": forms.Select(attrs={"class": "form-select"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "instagram": forms.TextInput(attrs={"class": "form-control"}),
            "facebook": forms.TextInput(attrs={"class": "form-control"}),
            "tiktok": forms.TextInput(attrs={"class": "form-control"}),
            "website": forms.TextInput(attrs={"class": "form-control"}),
            "value_proposition": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }