from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import EmailForm
from .models import Email
from django.http import JsonResponse
import traceback
import sys

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
                print(f"Using Host: {settings.EMAIL_HOST}, Port: {settings.EMAIL_PORT}, User: {settings.EMAIL_HOST_USER}, SSL: {settings.EMAIL_USE_SSL}, TLS: {settings.EMAIL_USE_TLS}")

                # 1. Try sending the email
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
                    print(traceback.format_exc())
                    return JsonResponse({'success': False, 'error': f"Email service error: {str(e)}"})

                # 2. Try saving to database (separately)
                try:
                    Email.objects.create(
                        to_email=to_email,
                        subject=subject,
                        message=message,
                    )
                    print("Email saved to database")
                except Exception as db_err:
                    print(f"WARNING: Database save failed: {str(db_err)}")
                    print(traceback.format_exc())
                    # We still return success: True because the email was sent
                    return JsonResponse({'success': True, 'warning': f'Email sent but history not saved: {str(db_err)}'})

                return JsonResponse({'success': True})
            else:
                print(f"Form validation failed: {form.errors}")
                return JsonResponse({'success': False, 'error': 'Invalid form data', 'details': form.errors.get_json_data()})

        # GET request
        return render(request, 'send_email.html', {'form': EmailForm()})

    except Exception as global_err:
        print("!!! GLOBAL CRASH IN VIEW !!!")
        print(traceback.format_exc())
        if request.method == 'POST':
            return JsonResponse({'success': False, 'error': f"Internal Server Error: {str(global_err)}"})
        raise # Let Django handle it for GET requests (shows 500 page)


def email_sent(request):
    return render(request, 'email_sent.html')