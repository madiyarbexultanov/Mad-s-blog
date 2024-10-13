from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, redirect
from django.utils.decorators import method_decorator

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User, EmailVerification
from common.views import TitleMixin

class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Sign In'
    


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    success_message = 'Congrats! You are successfully registrated!'
    title = 'Registration'


@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form'] = UserProfileForm(self.request.POST, self.request.FILES, instance=self.request.user)
        else:
            context['form'] = UserProfileForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, request.FILES, instance=self.request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile', pk=request.user.pk)  # редирект на страницу профиля после успешного сохранения
        else:
            return self.get(request, *args, **kwargs)  # если форма невалидна, отображаем страницу заново с ошибками

@login_required
def my_profile(request):
    return redirect('user_profile', pk=request.user.pk)


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/verification.html'
    title = 'Blog - Verification'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user = user, code = code)
        if email_verification.exists() and email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))