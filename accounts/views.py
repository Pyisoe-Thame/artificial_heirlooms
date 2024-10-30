from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm   # for login

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main')  # Redirect to home or another page of your choice
        else:
            print(form.errors)
            print("no new account was created...")
    else:
        form = SignUpForm()
        if request.user.is_authenticated:  # there is nothing here for authenticated user
            return redirect('main')
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')  # redirect to home or another page of your choice
            else:
                print("Invalid credentials")
        else:
            print(form.errors)
            print("Login failed")
    else:
        form = AuthenticationForm()
        if request.user.is_authenticated:  # redirect if user is already logged in
            return redirect('main')
    return render(request, 'login.html', {'form': form})

