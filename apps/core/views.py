from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import UserSubscription, User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from apps.business.models import BusinessProfile
from apps.ia.models import GeneratedPost, GeneratedImage
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator


@login_required
def dashboard(request):

    subscription = request.user.subscription

    if subscription.plan == "premium":

        post_limit = settings.PREMIUM_POST_LIMIT
        image_limit = settings.PREMIUM_IMAGE_LIMIT

    else:

        post_limit = settings.FREE_POST_LIMIT
        image_limit = settings.FREE_IMAGE_LIMIT

    post_percentage = int(
        (subscription.posts_generated / post_limit) * 100
    ) if post_limit else 0

    image_percentage = int(
        (subscription.images_generated / image_limit) * 100
    ) if image_limit else 0

    return render(
        request,
        "core/dashboard.html",
        {
            "subscription": subscription,
            "post_limit": post_limit,
            "image_limit": image_limit,
            "post_percentage": post_percentage,
            "image_percentage": image_percentage,
        }
    )

def home(request):

    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")

def privacy_policy(request):

    return render(
        request,
        "core/privacy_policy.html"
    )



def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")

        email = request.POST.get("email")

        message = request.POST.get("message")

        send_mail(
            subject=f"[Social AI] Nuevo mensaje de {name}",

            message=f"""
Nombre: {name}

Correo: {email}

Mensaje:

{message}
""",

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[
                settings.CONTACT_EMAIL
            ],

            fail_silently=False,
        )

        messages.success(
            request,
            "Tu mensaje ha sido enviado correctamente."
        )

        return redirect("contact")

    return render(
        request,
        "core/contact.html"
    )

#panel del administrador
@staff_member_required
def admin_dashboard(request):

    total_users = User.objects.count()

    free_users = UserSubscription.objects.filter(
        plan="free"
    ).count()

    premium_users = UserSubscription.objects.filter(
        plan="premium"
    ).count()

    total_businesses = BusinessProfile.objects.count()

    total_posts = GeneratedPost.objects.count()

    total_images = GeneratedImage.objects.count()

    users_list = User.objects.all().order_by("-date_joined")

    paginator = Paginator(
        users_list,
        10
    )

    page_number = request.GET.get("page")

    users = paginator.get_page(page_number)



    return render(
        request,
        "admin_panel/dashboard.html",
        {
            "total_users": total_users,
            "free_users": free_users,
            "premium_users": premium_users,
            "total_businesses": total_businesses,
            "total_posts": total_posts,
            "total_images": total_images,
            "users": users,
        }
    )

@staff_member_required
def toggle_user_plan(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    subscription = user.subscription

    if subscription.plan == "free":

        subscription.plan = "premium"

        messages.success(
            request,
            f"{user.username} ahora es Premium."
        )

    else:

        subscription.plan = "free"

        messages.success(
            request,
            f"{user.username} ahora es Free."
        )

    subscription.save()

    return redirect(
        "admin_dashboard"
    )

