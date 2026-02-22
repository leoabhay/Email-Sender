from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import EmailForm
from .models import Email
from django.http import JsonResponse
import traceback

def send_email(request):
    try:
        if request.method == 'POST':
            print("--- POST request received ---")
            form = EmailForm(request.POST)
            if form.is_valid():
                to_email = form.cleaned_data['to_email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                
                print(f"Attempting to send email to: {to_email}")
                print(f"Config: Host={settings.EMAIL_HOST}, Port={settings.EMAIL_PORT}")

                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [to_email],
                        fail_silently=False,
                    )
                    print("Email sent successfully")
                except Exception as e:
                    print(f"CRITICAL: Email send failed: {str(e)}")
                    return JsonResponse({'success': False, 'error': str(e)})

                # Save to database
                try:
                    Email.objects.create(
                        to_email=to_email,
                        subject=subject,
                        message=message,
                    )
                except Exception as db_err:
                    print(f"DB Error: {str(db_err)}")

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid form data'})

        return render(request, 'send_email.html', {'form': EmailForm()})

    except Exception as global_err:
        print(f"Global Error: {str(global_err)}")
        if request.method == 'POST':
            return JsonResponse({'success': False, 'error': "Internal Server Error"})
        raise


def email_sent(request):
    return render(request, 'email_sent.html')