from lib2to3.fixes.fix_input import context

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required

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
    status_filter = request.GET.get('status', '')

    if status_filter:
        applications = Application.objects.filter(status=status_filter).order_by('-created_at')
    else:
        applications = Application.objects.all().order_by('-created_at')

    context = {
        'applications': applications,
        'status_filter': status_filter,  # Передаем статус для использования в шаблоне
    }

    return render(request, 'catalog/index.html', context)




class Register(generic.CreateView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('catalog:login')


class Profile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'catalog/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        status_filter = self.request.GET.get('status', '')

        if status_filter:
            applications = Application.objects.filter(user=self.request.user, status=status_filter).order_by(
                '-created_at')
        else:
            applications = Application.objects.filter(user=self.request.user).order_by('-created_at')

        context['applications'] = applications
        context['status_filter'] = status_filter

        return context


def logout_user(request):
    logout(request)
    return redirect('catalog:index')

# View для создания новой заявки
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('catalog:profile')
    else:
        form = ApplicationForm()

    return render(request, 'catalog/create_application.html', {'form': form})

def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'catalog/application_detail.html', {'application': application})


@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if application.user == request.user:
        if application.status == 'n':
            application.delete()
            messages.success(request, "Заявка успешно удалена.")
        else:
            messages.error(request, "Вы можете удалить только заявки, которые находятся в статусе 'Новая'.")
    else:
        messages.error(request, "Вы не можете удалить эту заявку, так как она вам не принадлежит.")

    return redirect('catalog:profile')
