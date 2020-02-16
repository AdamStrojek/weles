from django_registration.backends.one_step.views import RegistrationView as BaseRegistrationView

from .forms import RegistrationForm


class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm
