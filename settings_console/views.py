from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'console.html')
    else:
        return render(request, 'frontpage.html')



def request_page(request):
  if(request.GET.get('mybtn')):
      print(request.GET.get('mytextbox'))
  return render(request,'console.html')

