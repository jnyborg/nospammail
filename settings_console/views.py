from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from settings_console.generateemail import generateRandomEmail
from settings_console.models import GeneratedEmail, GeneratedEmailForm



def index(request):
    if request.user.is_authenticated:
        generated_emails = GeneratedEmail.objects.filter(user_id=request.user.id)
        return render(request, 'console.html', context = {"generated_emails": generated_emails})
    else:
        return render(request, 'frontpage.html')


def generate_email(request):
    generatedEmail = generateRandomEmail()
    request.session['generated_email'] = generatedEmail
    data = { "generated_email": generatedEmail }
    return JsonResponse(data)


def add_generated_email(request):
    description = request.GET.get('description', None)
    g = GeneratedEmail(description=description,
                       email=request.session['generated_email'],
                       user=request.user)
    g.save()
    return render_to_response('console_list.html',
                              {"generated_emails": GeneratedEmail.objects.filter(user_id=request.user.id)})


def toggle_email(request):
    email_id = request.GET.get("id", None)
    if email_id != None:
        g = GeneratedEmail.objects.get(id=email_id)
        g.enabled = not g.enabled
        g.save()
    return render_to_response('console_list.html',
                              {"generated_emails": GeneratedEmail.objects.filter(user_id=request.user.id)})





