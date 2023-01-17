from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators import csrf

from .forms import UserRegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан {username}.')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog-reglog.html', {'form': form,
                                                'login_form': LoginForm()})


@login_required
def profile(request):
    return render(request, 'profile.html')
