
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileEditForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_detail(request,pk):
    user_profile = request.user.profile 
    context = {
        'profile': user_profile,
    }
    return render(request, 'accounts/profile_detail.html', context)


@login_required
def profile_edit(request, pk):
    # Ya corregiste la firma de la función: def profile_edit(request, pk):

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            
            # --- CORRECCIÓN CLAVE AQUÍ ---
            # 'profile_detail' necesita el pk para construir la URL.
            # Usamos request.user.pk (o request.user.id) para obtener el ID del usuario actual.
            return redirect('profile_detail', pk=request.user.pk) 
            # -----------------------------
            
    else:
        form = ProfileEditForm(instance=request.user.profile)

    context = {
        'form': form,
    }
    return render(request, 'accounts/profile_edit.html', context)
