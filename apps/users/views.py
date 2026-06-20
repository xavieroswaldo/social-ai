from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from .models import User
from .models import UserSubscription
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)

from django.utils.encoding import (
    force_bytes,
    force_str
)

from django.core.mail import send_mail




class CustomLoginView(LoginView):

    template_name = "users/login.html"

    authentication_form = LoginForm

    redirect_authenticated_user = True

    next_page = reverse_lazy("dashboard")

    #descomentar para produccion, esto impide que usuario no verificados no pueden logearse
    """ 
    def form_valid(self, form):

        user = form.get_user()

        if not user.email_verified:

            messages.error(
                self.request,
                "Debes verificar tu correo electrónico antes de ingresar."
            )

            return redirect("login")

        return super().form_valid(form)
    
    """
    


def logout_view(request):

    logout(request)

    return redirect("login")


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()
            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

            token = default_token_generator.make_token(
                user
            )
            verification_url = request.build_absolute_uri(
                reverse(
                    "verify_email",
                    args=[uid, token]
                )
            )
            send_mail(
                subject="Verifica tu cuenta de Social AI",

                message=f"""
            Hola {user.username},

            Gracias por registrarte en Social AI.

            Para verificar tu correo electrónico haz clic en el siguiente enlace:

            {verification_url}

            Si no creaste esta cuenta puedes ignorar este mensaje.
            """,

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[user.email],

                fail_silently=False,
            )


            UserSubscription.objects.get_or_create(
                user=user,
                defaults={
                    "plan": "free"
                }
            )

            messages.success(
                request,
                "Tu cuenta fue creada correctamente. Revisa tu correo electrónico para verificar tu cuenta."
            )
                
            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "users/register.html",
        {"form": form}
    )

@login_required
def my_plan(request):

    subscription = request.user.subscription

    return render(
        request,
        "users/my_plan.html",
        {
            "subscription": subscription,
            "post_limit": settings.FREE_POST_LIMIT,
            "image_limit": settings.FREE_IMAGE_LIMIT,
        }
    )


#Mejora el plan, esto por el momento
@login_required
def upgrade_plan(request):
    subscription = request.user.subscription

    return render(
    request,
    "users/upgrade_plan.html",
    {
        "subscription": subscription
    }
)

  
""" 
#activa luego
@login_required
def activate_premium(request, user_id):
    if not request.user.is_superuser:
         redirect("dashboard")

    subscription = request.user.subscription

    subscription.plan = "premium"

    subscription.save()

    messages.success(
        request,
        "Plan Premium activado correctamente."
    )

    return redirect("dashboard")
"""




#Perfil
@login_required
def profile_view(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Perfil actualizado correctamente."
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "users/profile.html",
        {
            "form": form
        }
    )


#validacion de correos
def verify_email(request, uidb64, token):

    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):

        user = None

   

    if user is not None:

        print(
            "VALID TOKEN:",
            default_token_generator.check_token(
                user,
                token
            )
        )

    if (
        user is not None
        and
        default_token_generator.check_token(
            user,
            token
        )
    ):

        user.email_verified = True

        user.save()

        messages.success(
            request,
            "Tu correo electrónico ha sido verificado correctamente. Ya puedes iniciar sesión"
        )

        return redirect("login")

    messages.error(
        request,
        "El enlace de verificación no es válido o ha expirado."
    )

    return redirect("login")