from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import EmailForm
from .models import Email
from django.http import JsonResponse

def send_email(request):
    if request.method == 'POST':
        print("POST request received at send_email")
        form = EmailForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            print(f"Attempting to send email to: {to_email}")

            try:
                # Attempt to send the email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [to_email],
                    fail_silently=False,
                )
                print("Email sent successfully")

                # Save the email to the database
                try:
                    Email.objects.create(
                        to_email=to_email,
                        subject=subject,
                        message=message,
                    )
                    print("Email saved to database")
                    return JsonResponse({'success': True})
                except Exception as db_err:
                    print(f"Database error: {str(db_err)}")
                    # Even if DB fails, email was sent
                    return JsonResponse({'success': True, 'warning': f'Email sent but failed to save to history: {str(db_err)}'})

            except Exception as e:
                print(f"Email send error: {str(e)}")
                return JsonResponse({'success': False, 'error': f"Failed to send email: {str(e)}"})
        else:
            print(f"Form invalid: {form.errors}")
            return JsonResponse({'success': False, 'error': 'Invalid form data', 'details': form.errors.get_json_data()})

    return render(request, 'send_email.html', {'form': EmailForm()})


def email_sent(request):
    return render(request, 'email_sent.html')
