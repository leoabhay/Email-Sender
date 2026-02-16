from django import forms
from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['to_email', 'subject', 'message']
        widgets = {
            'to_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Recipient Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Write your message here...', 'rows': 5}),
        }
