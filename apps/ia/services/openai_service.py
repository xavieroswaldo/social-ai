from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_image(image_prompt):

    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=image_prompt,
        size="1024x1024",
    )

    return result

def generate_content(
    business,
    product_name,
    objective,
    platform,
    tone,
):

    prompt = f"""
Actúa como un experto en marketing digital para pequeñas empresas.

INFORMACIÓN DEL NEGOCIO

Nombre: {business.business_name}

Tipo de negocio: {business.business_type.name}

Ciudad: {business.city}

Descripción:
{business.description}

Público objetivo:
{business.target_audience}

Tono de comunicación:
{tone}

Propuesta de valor:
{business.value_proposition}

INFORMACIÓN DE LA CAMPAÑA

Producto o servicio:
{product_name}

Objetivo:
{objective.name}

Red social:
{platform}

INSTRUCCIONES

Analiza cuidadosamente la información del negocio antes de escribir.

PERSONALIZACIÓN

- Utiliza el tono de comunicación indicado.
- Adapta el lenguaje al público objetivo.
- Destaca la propuesta de valor del negocio cuando sea relevante.
- Considera el tipo de negocio para contextualizar la publicación.
- Evita textos genéricos.

TONOS

Si el tono es "friendly":
- Utiliza lenguaje cercano.
- Usa emojis.
- Habla como si conversarás con un amigo.
- Mantén un ambiente cálido y positivo.

Si el tono es "professional":
- Utiliza lenguaje formal.
- Evita expresiones emocionales exageradas.
- Evita emojis.
- Destaca calidad, confianza y profesionalismo.
- El texto debe parecer escrito por una empresa seria.

Si el tono es "funny":
- Utiliza lenguaje creativo y entretenido.
- Agrega humor ligero y apropiado para redes sociales.
- Usa expresiones que generen simpatía o curiosidad.
- Puedes usar emojis cuando sean relevantes.
- Evita humor ofensivo, político o polémico.
- Evita parecer infantil.
- Mantén el enfoque en el producto o servicio.
- El texto debe ser divertido pero profesional.
- Debe parecer escrito por una marca moderna y cercana.

Si el tono es "elegant":
- Utiliza lenguaje sofisticado y refinado.
- Evita expresiones coloquiales.
- Evita emojis llamativos.
- Transmite exclusividad y prestigio.
- El texto debe parecer escrito por una marca premium.

OBJETIVO SELECCIONADO

{objective.name}

La publicación debe alinearse principalmente con este objetivo.

REGLA CRÍTICA

Debes seguir únicamente el objetivo seleccionado.

No combines instrucciones de otros objetivos.


Por ejemplo:

- Si el objetivo es Fidelización, NO promociones descuentos.
- Si el objetivo es Fidelización, NO hables de nuevos productos como lanzamiento.
- Si el objetivo es Fidelización, NO menciones promociones de fin de semana salvo que se indique explícitamente.

La publicación debe centrarse exclusivamente en el objetivo seleccionado.
No asumas que el producto es nuevo a menos que el objetivo seleccionado sea "Nuevo producto".
La versión Funny también debe respetar el objetivo seleccionado.
No utilices humor que ignore el objetivo principal de la campaña.

IMPORTANTE

El objetivo de la campaña tiene prioridad sobre el producto.

El producto es el vehículo del mensaje.

La publicación debe construirse alrededor del objetivo seleccionado.

No construyas la publicación únicamente alrededor del producto.

OBJETIVO

Promoción de fin de semana:
- Motiva al cliente a visitar el negocio durante el fin de semana.
- Destaca experiencias, productos o beneficios especiales.
- Incluye una llamada a la acción.

Nuevo producto:
- Presenta el producto o servicio como una novedad.
- Despierta curiosidad.
- Destaca los principales beneficios.

Descuento:
- Resalta claramente el ahorro o beneficio económico.
- Genera sensación de oportunidad.
- Incluye una llamada a la acción.

Evento especial:
- Comunica el evento de forma atractiva.
- Genera expectativa e interés.
- Invita a participar o asistir.

No asumas fechas específicas.

No menciones "este fin de semana" a menos que la información proporcionada indique explícitamente que el evento ocurre durante el fin de semana.

Fidelización:
- Refuerza la relación con los clientes.
- Transmite cercanía y agradecimiento.
- Fortalece la confianza en la marca.

PLATAFORMA

Instagram:
- Entre 80 y 150 palabras.
- Usa emojis cuando corresponda.
- Incluye entre 3 y 5 hashtags.
- Prioriza impacto visual y emocional.

Facebook:
- Entre 120 y 250 palabras.
- Puede ser más descriptivo.
- Explica mejor el contexto.
- Usa pocos hashtags.

WhatsApp:

- Máximo 50 palabras.
- Máximo 3 párrafos cortos.
- No escribas publicaciones largas.
- Debe parecer un mensaje enviado directamente a un cliente.
- Evita hashtags.
- Utiliza lenguaje cercano y natural.

TikTok:

- Entre 10 y 30 palabras.
- Máximo 3 líneas.
- No escribas párrafos.
- Comienza con un hook.
- Puede usar formato POV.
- Puede usar preguntas.
- Puede usar tendencias.
- Máximo 2 hashtags.
- Debe parecer el texto de un video viral.

La plataforma tiene prioridad sobre el formato.

Instagram:
- Optimizado para engagement visual.

Facebook:
- Optimizado para lectura y contexto.

WhatsApp:
- Optimizado para mensajes directos y personales.

No reutilices el mismo formato entre plataformas.

IMPORTANTE:

El objetivo define qué se quiere lograr con la publicación.
El tono define la personalidad del mensaje.
No confundas ambos conceptos.

DIFERENCIACIÓN DE VERSIONES

Cada versión debe parecer escrita por una marca diferente.

Professional:
- Formal.
- Confiable.
- Orientada a transmitir calidad.
- Lenguaje corporativo y profesional.

Friendly:
- Cercana.
- Conversacional.
- Cálida.
- Uso natural de emojis cuando corresponda.

Funny:
- Creativa.
- Entretenida.
- Moderna.
- Humor ligero relacionado con el producto o servicio.
- Evita humor infantil o exagerado.

INSTRUCCIONES ADICIONALES

- La publicación debe sentirse auténtica.
- Evita frases genéricas.
- No repitas el nombre del negocio innecesariamente.
- Genera textos que parezcan escritos por un especialista en marketing.
- Utiliza lenguaje natural y persuasivo.
- Las tres versiones deben ser claramente diferentes entre sí.

Devuelve únicamente un JSON válido con esta estructura:

{{
    "professional": "texto",
    "friendly": "texto",
    "funny": "texto",
    "photo_idea": "texto"
}}

REGLAS IMPORTANTES:

- No utilices markdown.
- No utilices bloques de código.
- No escribas ```json.
- No agregues explicaciones antes o después.
- No agregues texto fuera del JSON.
- La respuesta debe ser únicamente un objeto JSON válido.
"""    


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "", 1)

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()
    print(content)
    try:
        return json.loads(content)

    except json.JSONDecodeError as e:

        print("ERROR JSON:", e)
        print(content)

        return {
            "professional": content,
            "friendly": "",
            "funny": "",
            "photo_idea": "",
    }