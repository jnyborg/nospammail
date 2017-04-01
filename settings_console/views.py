from django.http import HttpResponse


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hello, world")
    else:
        return HttpResponse("GTFO")




