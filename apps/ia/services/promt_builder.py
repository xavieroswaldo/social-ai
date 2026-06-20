def build_marketing_prompt(business, objective, platform, product_name):

    print(business.communication_tone)

    prompt = f"""
Eres un experto en marketing digital.

DATOS DEL NEGOCIO

Nombre:
{business.business_name}

Tipo:
{business.business_type}

Ciudad:
{business.city}

Descripción:
{business.description}

Público Objetivo:
{business.target_audience}

Tono:
{business.communication_tone}

Instagram:
{business.instagram}

Propuesta de Valor:
{business.value_proposition}

SOLICITUD

Producto:
{product_name}

Objetivo:
{objective}

Plataforma:
{platform}

Genera:

1. Texto publicitario.
2. Llamado a la acción.
3. Hashtags.
"""

    return prompt
