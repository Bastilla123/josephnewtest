from django.urls import resolve
from django.shortcuts import render
from django.views.generic.edit import FormView, ModelFormMixin
from django.views.generic.detail import SingleObjectMixin

from demoapp.forms import *
from demoapp import *


class EditHistorie(FormView, ModelFormMixin, SingleObjectMixin):
    model = Estates
    form_class = Estatesform
    success_url = '/'
    template_name = 'form.html'

    def get_queryset(self):
        return Estates.objects.all()

    def set_object(self, request):
        if not resolve(request.path).url_name == 'add':
            queryset = self.get_queryset()
            self.object = self.get_object(queryset=queryset)
        else:
            self.object = None

    def get(self, request, *args, **kwargs):
        self.set_object(request)
        return super(EditHistorie, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.set_object(request)
        return super(EditHistorie, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


def home(request):
    data = {
        'objs': Estates.objects.all()
    }
    return render(request, 'home.html', data)