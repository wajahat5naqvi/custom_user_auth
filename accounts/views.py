
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from .models import LoggedInUser
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404



def register_user(request):
    if request.user.is_authenticated:
        return redirect('users')
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(email=email, phone_number=phone_number, password=password)
            return redirect('login')
        else:
            context = {
                'error': 'Email already exists!'
            }
            return render(request,  'accounts/register.html', context)

    return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('users')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


@login_required
def users(request):
    
    query = request.GET.get('q', '')  # search query
    if query:
        users = User.objects.filter(full_name__icontains=query) | \
                User.objects.filter(email__icontains=query) | \
                User.objects.filter(phone_number__icontains=query)
    else:
        users = User.objects.all()

    return render(request, 'accounts/users.html', {
        'users': users,
        'query': query
    })

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')

        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()
        return redirect('edit_user', user_id=user.id)

    return render(request, 'accounts/edit_user.html', {'user': user})




def logout_user(request):
    logout(request)
    return redirect('login')
