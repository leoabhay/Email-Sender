from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import EmailForm
from .models import Email
from django.http import JsonResponse

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Attempt to send the email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [to_email],
                    fail_silently=False,
                )

                # Save the email to the database
                Email.objects.create(
                    to_email=to_email,
                    subject=subject,
                    message=message,
                )

                return JsonResponse({'success': True})
            except Exception as e:
                # Return the error message
                return JsonResponse({'success': False, 'error': str(e)})

    # If the request is not POST or the form is invalid
    return render(request, 'send_email.html', {'form': EmailForm()})


def email_sent(request):
    return render(request, 'email_sent.html')
