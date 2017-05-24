from django.shortcuts import render, render_to_response
from settings_console.generateemail import generateRandomEmail
from settings_console.models import GeneratedEmail, EmailVisiblity
from django.http import HttpResponse
from http import HTTPStatus
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from enum import IntEnum

class ErrorCode(IntEnum):
    SUCCESS = 0
    NO_DESCRIPTION = 1

def index(request):
    if request.user.is_authenticated:
        generated_emails = get_user_emails(request.user, EmailVisiblity.VISIBLE)

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

def get_user_emails(user, visibility):
    if EmailVisiblity(visibility) is not None:
        return GeneratedEmail.objects.filter(user_id=user.id, visibility=visibility)
    else:
        raise Exception("Invalid visibility: {}".format(visibility))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Re-validates session so user does not have to log in again
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })