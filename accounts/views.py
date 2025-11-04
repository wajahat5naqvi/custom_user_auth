from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User, LoggedInUser
from django.utils import timezone


# 🔹 REGISTER USER
def register_user(request):
    if request.user.is_authenticated:
        return redirect('users')

    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if not User.objects.filter(email=email).exists():
            User.objects.create_user(email=email, phone_number=phone_number, password=password)
            return redirect('login')
        else:
            return render(request, 'accounts/register.html', {'error': 'Email already exists!'})

    return render(request, 'accounts/register.html')


# 🔹 LOGIN USER
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


# 🔹 USERS LIST (Search + Delete + Pagination)
@login_required
def users(request):
    query = request.GET.get('q', '').strip()
    users_list = User.objects.all().order_by('-id')

    # 🔍 Search logic
    if query:
        users_list = users_list.filter(
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(full_name__icontains=query)
        )

    # 🗑 Delete logic
    if request.method == 'POST' and 'delete_user' in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('users')

    # 📄 Pagination logic
    paginator = Paginator(users_list, 5)  # 5 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/users.html', {
        'page_obj': page_obj,
        'query': query
    })


# 🔹 EDIT USER
@login_required
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


# 🔹 LOGOUT USER
def logout_user(request):
    logout(request)
    return redirect('login')
