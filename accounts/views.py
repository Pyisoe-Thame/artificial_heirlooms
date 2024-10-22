from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.shortcuts import redirect

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/items/')  # Redirect to home or another page of your choice
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

