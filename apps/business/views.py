from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BusinessProfile
from .forms import BusinessProfileForm, BusinessProfileUpdateForm
from django.conf import settings


# listado y activacion de negocios
@login_required
def business_list(request):

    businesses = BusinessProfile.objects.filter(user=request.user)

    active_business_id = request.session.get("active_business_id")

    return render(
        request,
        "business/business_list.html",
        {
            "businesses": businesses,
            "active_business_id": active_business_id,
        },
    )


# Crear_negocios
@login_required
def business_create(request):

    subscription = request.user.subscription

    count = BusinessProfile.objects.filter(
        user=request.user
    ).count()

    if subscription.plan == "free":

        if count >= settings.FREE_BUSINESS_LIMIT:

            messages.error(
                request,
                "Tu plan gratuito permite registrar únicamente 1 negocio."
            )

            return redirect("upgrade_plan")

    elif subscription.plan == "premium":

        if count >= settings.PREMIUM_BUSINESS_LIMIT:

            messages.error(
                request,
                "Has alcanzado el límite de 3 negocios de tu plan Premium."
            )

            return redirect("business_list")

    if request.method == "POST":

        form = BusinessProfileForm(request.POST, request.FILES)

        if form.is_valid():

            business = form.save(commit=False)

            business.user = request.user

            business.save()

            messages.success(request, "Negocio creado correctamente.")

            return redirect("business_list")

    else:

        form = BusinessProfileForm()

    return render(request, "business/business_form.html", {"form": form})


# editar_negocio
@login_required
def business_update(request, pk):

    business = get_object_or_404(BusinessProfile, pk=pk, user=request.user)

    if request.method == "POST":

        form = BusinessProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=business
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Negocio actualizado.")

            return redirect("business_list")

    else:

        form = BusinessProfileUpdateForm(instance=business)

    return render(request, "business/business_form.html", {"form": form})

"""
# eliminar_negocio en futuro
@login_required
def business_delete(request, pk):

    business = get_object_or_404(BusinessProfile, pk=pk, user=request.user)

    business.delete()

    messages.success(request, "Negocio eliminado.")

    return redirect("business_list")

"""
#la eliminacion no esta permitida
@login_required
def business_delete(request, pk):

    business = get_object_or_404(
        BusinessProfile,
        pk=pk,
        user=request.user
    )

    subscription = request.user.subscription

    if subscription.plan == "premium":

        messages.error(
            request,
            "Los negocios Premium no pueden eliminarse."
        )

        return redirect("business_list")

    if subscription.businesses_deleted >= 1:

        messages.error(
            request,
            "Ya utilizaste tu eliminación disponible del plan gratuito."
        )

        return redirect("business_list")

    business.delete()

    subscription.businesses_deleted += 1
    subscription.save()

    messages.success(
        request,
        "Negocio eliminado correctamente."
    )

    return redirect("business_list")



# activar_negocio
@login_required
def set_active_business(request, pk):

    business = BusinessProfile.objects.filter(id=pk, user=request.user).first()

    if business:

        request.session["active_business_id"] = business.id

    return redirect("business_list")
