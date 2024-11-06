from django.shortcuts import render
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy
# Create your views here.
def index(request):
    return render(
        request,
        'catalog/index.html'
    )

class Register(generic.CreateView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('catalog:login')