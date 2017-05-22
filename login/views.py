from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from login.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from nospammail.urls import anonymous_required
from http import HTTPStatus

@anonymous_required(custom_redirect=HttpResponse("You are already signed in, please sign out and try again.", status=HTTPStatus.UNAUTHORIZED))
def signup(request):
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})