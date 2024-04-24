from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, FormView

from referral.models import User, AuthCodeModel
from referral.forms import EnterPhoneNumberForm, EnterAuthCodeForm

from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect

from referral.forms import EnterReferralCodeForm

from django.core.exceptions import BadRequest, ObjectDoesNotExist



# Create your views here.


class IndexView(LoginRequiredMixin, FormView):
    form_class = EnterReferralCodeForm
    login_url = reverse_lazy('enter_phone')
    template_name = 'referral/profile.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['phone_number'] = user.phone_number
        context['inviter'] = user.inviter
        return context
    
    def form_valid(self, form):
        user = self.request.user
        form_ref_code = form.cleaned_data.get('referral_code')
        try:
            form_ref_user = User.objects.get(referral_code=form_ref_code)
            if form_ref_user == user:
                raise ValueError
            user.inviter = form_ref_user
            user.save()
        except User.DoesNotExist:
            form.add_error(None, 'Invalid referral code')
            return super().form_invalid(form)
        except ValueError:
            form.add_error(None, 'You cannot use your own referral code')
            return super().form_invalid(form)

        return super().form_valid(form) 
    



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

        try:
            new_write = AuthCodeModel.objects.create(user=phone_user, code='123456')
            new_write.save()
        except:
            pass
        self.request.session['user_id'] = phone_user.id

        return super().form_valid(form) 
        

class EnterAuthCodeView(FormView):
    form_class = EnterAuthCodeForm 
    template_name = 'referral/enter_auth_code.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if not self.request.session.get('user_id'):
            return redirect(reverse_lazy('enter_phone'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user_id = self.request.session['user_id']
        auth_code = form.cleaned_data['auth_code']
        user = authenticate(user_id=user_id, auth_code=auth_code)
        del self.request.session['user_id']
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)
    


def logout_view(request):
    logout(request)
    return redirect('/')
