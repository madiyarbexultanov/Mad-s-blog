from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect

from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User, EmailVerification
from common.views import TitleMixin

class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Sign In'
    

# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data = request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password = password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    success_message = 'Congrats! You are successfully registrated!'
    title = 'Registration'

# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Congrats! You are successfully registrated!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)

class ProfileView(TitleMixin, TemplateView):
    template_name = 'users/profile.html'
    title = 'About Me'

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