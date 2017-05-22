from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from settings_console.generateemail import generateRandomEmail
from settings_console.models import GeneratedEmail
from django.http import HttpResponse
from http import HTTPStatus

from enum import Enum

class ErrorCode(Enum):
    SUCCESS = 0
    NO_DESCRIPTION = 1

def index(request):
    if request.user.is_authenticated:
        generated_emails = GeneratedEmail.objects.filter(user_id=request.user.id)
        return render(request, 'console.html', context = {"generated_emails": generated_emails})
    else:
        return render(request, 'frontpage.html')


def add_generated_email(request):
    description = request.GET.get('description', None)
    if not isinstance(description, str) or len(str.replace(description, " ", "")) < 1:
        return render_to_response('console_list.html',
                                  {"generated_emails": GeneratedEmail.objects.filter(user_id=request.user.id),
                                   "error_code": ErrorCode.NO_DESCRIPTION,
                                   "error_message": "Please enter a description."})

    if not request.user or not request.user.is_authenticated():
        return HttpResponse("You must log in before proceeding.", status=HTTPStatus.UNAUTHORIZED)

    g = GeneratedEmail(description=description,
                       email=generateRandomEmail(),
                       user=request.user)
    g.save()

    return render_to_response('console_list.html',
                              {"generated_emails": GeneratedEmail.objects.filter(user_id=request.user.id)})


def toggle_email(request):
    email_id = request.GET.get("id", None)
    if email_id != None:
        g = GeneratedEmail.objects.get(id=email_id)
        if g.user.id != request.user.id:
            return HttpResponse("You do not have permission to do this.", status=HTTPStatus.UNAUTHORIZED)

        g.enabled = not g.enabled
        g.save()
    return render_to_response('console_list.html',
                              {"generated_emails": GeneratedEmail.objects.filter(user_id=request.user.id)})