from django.shortcuts import render
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy
# Create your views here.

from django.http import JsonResponse
from .models import User

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Логин уже занят.'
    return JsonResponse(data)


def index(request):
    return render(
        request,
        'catalog/index.html'
    )

class Register(generic.CreateView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('catalog:login')