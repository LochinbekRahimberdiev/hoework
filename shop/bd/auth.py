from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from shop.forms import LoginForm


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return render('pruct_list')
            else:
                messages.error(request, 'Username or password incorrect')
    else:
        form = LoginForm()
    return render(request , 'login.html', {'form': form})


def register(request):
    return render(request , 'register.html')



def logout_page(request):
    logout(request)
    return render('product_list')



def register_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if  User.objects.filter(username=username):
            return render(request, 'register.html', {"message_user": "Bunday foydalanuchi mavjud"})
        if password == password2:
            new_user = User(first_name=first_name, last_name=last_name, username=username, email=email)
            new_user.set_password(password)
            return redirect('login')
        else:
            return render(request, 'register.html', {"message": "Passwords Error"})
    return render(request, 'register.html')




