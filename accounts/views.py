#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from testcode.models import Profile

from .forms import ProfileForm, SignUpForm
 
 
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts\signup.html'

def ProfileView(request):
    us = request.user
    print('user:', us)
    prof, _ = Profile.objects.get_or_create(user=us)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=prof)
        form.save()
    else:
        form = ProfileForm()
    return render(request, 'accounts/profile.html', {'title': 'Профиль','form': form})

