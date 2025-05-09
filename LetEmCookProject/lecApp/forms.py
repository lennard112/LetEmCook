
from django import forms

class EmailMFAForm(forms.Form):
    code = forms.CharField(max_length=6, label='Enter the code sent to your email')
