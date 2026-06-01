from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "placeholder": "Usuario",
            "style": "width:100%; padding:10px; border-radius:6px; border:1px solid #ccc;"
        })

        self.fields["password"].widget.attrs.update({
            "placeholder": "Contraseña",
            "style": "width:100%; padding:10px; border-radius:6px; border:1px solid #ccc;"
        })
