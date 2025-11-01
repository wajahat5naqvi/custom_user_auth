
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email', )
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(email=email, phone_number=phone_number, password=password)
            return redirect('login')
        else:
            return render(request,  'accounts/register.html',             {'error': 'Email already exists!'})

    return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


@login_required
def home(request):
    return render(request, 'accounts/home.html', {'user': request.user})


def logout_user(request):
    logout(request)
    return redirect('login')
