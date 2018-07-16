from django.contrib.auth.forms import AuthenticationForm
from fruit_sales import logging


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input is_midium'
        self.fields['password'].widget.attrs['class'] = 'input is_midium'
