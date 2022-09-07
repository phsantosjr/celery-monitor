from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields["username"].label = "User Name"
        self.fields["password"].label = "Senha"
