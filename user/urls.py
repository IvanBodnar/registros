from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from .views import inicio

AuthenticationForm.error_messages = error_messages = {
        'invalid_login': (
            "Por favor ingrese usuario y contraseña correctos. Tenga en cuenta que ambos "
            "campos distinguen mayúsculas y minúsculas."
        ),
        'inactive': ("Esta cuenta se encuentra inactiva."),
    }

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'user/login.html',
         'extra_context': {'next': 'user_inicio'}},
        name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^inicio/$', inicio, name='user_inicio')
]