from django.shortcuts import render
from apps.business.models import BusinessProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import GeneratePostForm
from .models import GeneratedPost
from apps.ia.services.openai_service import generate_content, generate_image
import base64
from django.core.files.base import ContentFile
from .models import GeneratedImage
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from .tasks import test_task
import traceback
#from PIL import Image
#from PIL import ImageDraw
#from PIL import ImageFont
#from io import BytesIO
#from django.core.files.base import ContentFile

#Generar publicaciones
@login_required
def generate_post(request):
    
    generated_text = None
    generated_content = None
    final_tone = None
    generated_post = None

    active_business_id = request.session.get("active_business_id")

    active_business = None

    if active_business_id:

        active_business = BusinessProfile.objects.filter(
            id=active_business_id, user=request.user
        ).first()

    if not active_business:

        messages.warning(
            request, "Debes seleccionar uno de tus negocios antes de generar contenido"
        )

        return redirect("business_list")

    if request.method == "POST":

        form = GeneratePostForm(request.POST)

        if form.is_valid():

            
            objective = form.cleaned_data["objective"]
            platform = form.cleaned_data["platform"]
            product_name = form.cleaned_data["product_name"]
            tone_override = form.cleaned_data["tone_override"]
            final_tone = (
                tone_override
                if tone_override
                else active_business.communication_tone
            )

            print("OBJETIVO SELECCIONADO:", objective.name)


            #Bloqueo de publicaciones, por ahora desde aqui
            subscription = request.user.subscription

            if subscription.plan == "premium":

                post_limit = settings.PREMIUM_POST_LIMIT

            else:

                post_limit = settings.FREE_POST_LIMIT

            if subscription.posts_generated >= post_limit:

                messages.error(
                    request,
                    f"Has alcanzado el límite de {post_limit} publicaciones de tu plan."
                )

                return redirect("upgrade_plan")
                        
            #hasta aqui


            generated_content = generate_content(
                business=active_business,
                product_name=product_name,
                objective=objective,
                platform=platform,
                tone=final_tone,
            )

            generated_text = "\n\n".join(generated_content.values())

            generated_post = GeneratedPost.objects.create(
                user=request.user,
                business=active_business,
                business_type=active_business.business_type,
                objective=objective,
                platform=platform,
                title=f"Promoción {product_name}",
                product_name=product_name,
                prompt="Texto simulado",
                generated_text=generated_text,
                professional_text=generated_content.get("professional", ""),
                friendly_text=generated_content.get("friendly", ""),
                funny_text=generated_content.get("funny", ""),
                photo_idea=generated_content.get("photo_idea", "")
            )

            subscription.posts_generated += 1

            subscription.save()

    else:

        form = GeneratePostForm()

    tone_labels = {
    "friendly": "Amigable",
    "professional": "Profesional",
    "funny": "Divertido",
    "elegant": "Elegante",
    }

    selected_tone_display = tone_labels.get(final_tone, final_tone)



    return render(
        request,
        "ia/generate_post.html",
        {
            "form": form,
            "generated_content": generated_content,
            "active_business": active_business,
            "selected_tone": selected_tone_display,
            "generated_post": generated_post,

        },
    )

#generar imagen
@login_required
def generate_post_image(request, post_id):

    return HttpResponse(
        "ESTA ES LA NUEVA VISTA",
        content_type="text/plain"
    )


"""
@login_required
def generate_post_image(request, post_id):

    test_task.delay()
    return HttpResponse("Tarea enviada")


    post = get_object_or_404(
        GeneratedPost,
        id=post_id,
        user=request.user
    )

    if post.images.count() >= 3:

        messages.error(
            request,
            "Esta publicación ya alcanzó el límite de 3 imágenes generadas."
        )

        return redirect(
            "post_detail",
            post_id=post.id
        )


    subscription = request.user.subscription

    if subscription.plan == "premium":

        image_limit = settings.PREMIUM_IMAGE_LIMIT

    else:

        image_limit = settings.FREE_IMAGE_LIMIT

    if subscription.images_generated >= image_limit:

        messages.error(
            request,
            f"Has alcanzado el límite de {image_limit} imágenes de tu plan."
        )

        return redirect("upgrade_plan")

    result = generate_image(post.photo_idea)

    image_b64 = result.data[0].b64_json

    image_data = base64.b64decode(image_b64)

    generated_image = GeneratedImage.objects.create(
        generated_post=post,
        prompt=post.photo_idea,
    )

    generated_image.image.save(
        f"post_{post.id}.png",
        ContentFile(image_data),
        save=True
    )

    subscription = request.user.subscription

    subscription.images_generated += 1

    subscription.save()
    
    return redirect("post_history")
"""
    

#historial de las pubicaciones
@login_required
def post_history(request):

    posts = GeneratedPost.objects.filter(
        user=request.user
    ).order_by("-created_at")

    paginator = Paginator(posts, 25)  # 10 por página

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "ia/post_history.html",
        {
            "page_obj": page_obj
        }
    )


@login_required
def toggle_favorite(request, pk):

    post = get_object_or_404(GeneratedPost, pk=pk, user=request.user)

    post.is_favorite = not post.is_favorite

    post.save()

    return redirect("post_history")

#detalle de la publicacion
@login_required
def post_detail(request, post_id):

    post = get_object_or_404(
        GeneratedPost,
        id=post_id,
        user=request.user
    )

    return render(
        request,
        "ia/post_detail.html",
        {
            "post": post
        }
    )


# Funcionalidad pausada temporalmente.
"""
@login_required
def generate_poster(request, post_id):

    post = get_object_or_404(
        GeneratedPost,
        id=post_id,
        user=request.user
    )

    if post.posters.count() >= 3:

        messages.error(
            request,
            "Esta publicación ya alcanzó el límite de 3 posters."
        )

        return redirect(
            "post_detail",
            post_id=post.id
        )

    subscription = request.user.subscription

    if subscription.plan != "premium":

        messages.error(
            request,
            "La generación de posters es una función exclusiva para usuarios Premium."
        )

        return redirect("upgrade_plan")
    
    style = request.POST.get(
    "style",
    "professional"
    )

    if style == "professional":

        poster_text = post.professional_text

    elif style == "friendly":

        poster_text = post.friendly_text

    else:

        poster_text = post.funny_text

    messages.success(
        request,
        f"Texto seleccionado: {style}"
    )


    last_image = post.images.last()

    if not last_image:

        messages.error(
            request,
            "La publicación no tiene imágenes generadas."
        )

        return redirect(
        "post_detail",
        post_id=post.id
    )
    #crea poster
    base_image = Image.open(
        last_image.image.path
    )

    base_image = base_image.resize(
        (1080, 700)
    )

    #crea el lienzo
    poster = Image.new(
    "RGB",
    (1080, 1080),
    color="white"
    )
    #pegar imagen
    poster.paste(
    base_image,
    (0, 0)
    )

    #pegar texto
    draw = ImageDraw.Draw(
    poster
    )

    font = ImageFont.truetype(
    "C:/Windows/Fonts/arial.ttf",
    40
    )
    short_text = poster_text[:150]

    draw.rectangle(
    [(0, 700), (1080, 1080)],
    fill=(245, 245, 245)
)

    #dibujar
    draw.text(
    (40, 740),
    short_text,
    fill="black",
    font=font
    )


    #guarad en memoria
    buffer = BytesIO()

    poster.save(
        buffer,
        format="PNG"
    )

    #crea registro
    generated_poster = GeneratedPoster.objects.create(
    generated_post=post
    )

    #guarad archivo
    generated_poster.image.save(
    f"poster_{post.id}.png",
    ContentFile(buffer.getvalue()),
    save=True
    )      

    return redirect(
        "post_detail",
        post_id=post.id
    )

"""


    