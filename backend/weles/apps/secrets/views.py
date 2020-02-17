from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from .models import Secret, SecretAccessLog
from .forms import AddSecretForm, CheckPasswordSecretForm


class CreateSecretView(LoginRequiredMixin, CreateView):
    template_name = 'secrets/create.html'
    model = Secret
    form_class = AddSecretForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('secret-detail', kwargs={'uuid': self.object.uuid})


class SecretDetailView(LoginRequiredMixin, DetailView):
    template_name = 'secrets/detail.html'

    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def get_queryset(self):
        return Secret.objects.filter(user=self.request.user).prefetch_related('log')

    def get_context_data(self, **kwargs):
        data = super(SecretDetailView, self).get_context_data(**kwargs)
        data['object_url'] = self.request.build_absolute_uri(self.object.get_absolute_url())
        return data


class SecretRedirectView(SingleObjectMixin, FormView):
    template_name = 'secrets/redirect.html'

    model = Secret  # TODO change it to queryset so can filter only 24h links
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    form_class = CheckPasswordSecretForm

    def get_queryset(self):
        return Secret.objects.active()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SecretRedirectView, self).get_form_kwargs()
        kwargs['secret_obj'] = self.object
        return kwargs

    def form_valid(self, form):
        self.object.create_access_log(self.request)
        return super(SecretRedirectView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_redirect()


class SecretAccessLogView(TemplateView):
    template_name = 'secrets/stats.html'

    def get_queryset(self):
        return SecretAccessLog.objects.filter(secret__user=self.request.user).statistics()

    def get_context_data(self, **kwargs):
        context_data = super(SecretAccessLogView, self).get_context_data(**kwargs)
        context_data['objects'] = self.get_queryset()
        return context_data
