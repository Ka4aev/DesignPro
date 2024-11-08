from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from .forms import ApplicationForm
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
    applications = Application.objects.all().order_by('-created_at')
    return render(request, 'catalog/index.html', {'applications': applications})

def profile(request,self):
    applications = Application.objects.filter(user=self.request.user).order_by('-created_at')
    return render(request, 'catalog/profile.html', {'applications': applications})

class Register(generic.CreateView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('catalog:login')




class Profile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'catalog/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(user=self.request.user).order_by('-created_at')
        return context

# def profile_view(request):
#     return render(request, 'catalog/profile.html', {'user': request.user})


def logout_user(request):
    logout(request)
    return redirect('catalog:index')

# View для создания новой заявки
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем объект, но не сохраняем его в базе данных сразу
            application = form.save(commit=False)
            # Назначаем текущего пользователя
            application.user = request.user
            # Сохраняем объект в базе данных
            application.save()
            return redirect('catalog:profile', pk=request.user.id)
    else:
        form = ApplicationForm()

    return render(request, 'catalog/create_application.html', {'form': form})

def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'catalog/application_detail.html', {'application': application})

