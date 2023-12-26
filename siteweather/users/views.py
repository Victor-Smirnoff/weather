from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import forms


def login_user(request):
    if request.method == 'POST':
        form = forms.LoginUserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request=request,
                                username=cleaned_data['username'],
                                password=cleaned_data['password']
                                )
            if user and user.is_active():
                login(request=request, user=user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = forms.LoginUserForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    return HttpResponse("logout")
