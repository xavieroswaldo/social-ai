from django.db import migrations


def seed_marketing_objectives(apps, schema_editor):
    MarketingObjective = apps.get_model('ia', 'MarketingObjective')

    objectives = [
        "Promoción fin de semana",
        "Nuevo producto",
        "Descuento",
        "Evento especial",
        "Fidelización",
        "Promocionar producto",
        "Generar interacción",
        "Posicionar marca",
        "Lanzar producto o servicio",
    ]

    for name in objectives:
        MarketingObjective.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('ia', '0012_seed_business_types_v2'),
    ]

    operations = [
        migrations.RunPython(seed_marketing_objectives),
    ]


