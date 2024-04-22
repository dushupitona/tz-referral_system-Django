from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse

from django.views.generic import TemplateView, FormView

from referral.models import User, AuthCodeModel
from referral.forms import EnterPhoneNumberForm, EnterAuthCodeForm

from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('enter_phone')
    template_name = 'referral/profile.html'




class EnterPhoneNumberView(FormView):
    form_class = EnterPhoneNumberForm
    template_name = 'referral/enter_phone.html'
    success_url = reverse_lazy('enter_auth_code')

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        try:
            phone_user = User.objects.create_user(phone_number=str(phone_number))
        except:
            phone_user = User.objects.get(phone_number=str(phone_number))
        print(f'Phone user ID: {phone_user}')

        try:
            new_write = AuthCodeModel.objects.create(user=phone_user, code='123456')
            new_write.save()
        except:
            pass
        self.request.session['phone_id'] = phone_user.id
        self.request.session['phone_number'] = str(phone_number)
        return super().form_valid(form) 
        

class EnterAuthCodeView(FormView):
    form_class = EnterAuthCodeForm 
    template_name = 'referral/enter_auth_code.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        phone_number = self.request.session['phone_number']
        user_id = self.request.session['phone_id']
        auth_code = form.cleaned_data['auth_code']
        user = authenticate(user_id=user_id, auth_code=auth_code)
        del self.request.session['phone_number']
        del self.request.session['phone_id']

        if user is not None:
                login(self.request, user)
                return reverse_lazy('index')
        else:
            form.add_error(None, "Invalid email or password.")

        print(user)

        return super().form_valid(form)

