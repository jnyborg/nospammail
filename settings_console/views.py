from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'console.html')
    else:
        return render(request, 'frontpage.html')




