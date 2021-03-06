from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from store.models import Post
from .models import Wishlist
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm

from django.db import connection

# Create your views here.
def home_view(request):
    return HttpResponse("Hello World!")

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.phone_number = form.cleaned_data.get('phone_number')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        print(connection.queries)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'users/profile.html'
    context_object_name = 'posts'
    paginate_by=3
    ordering = ['-datetime']

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = 'profile'
        context['post_count']= Post.objects.filter(user=self.request.user).count()
        context['sold_count']= Post.objects.filter(user=self.request.user).filter(sold=True).count()

        print(connection.queries)
        return context


def update_view(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print(connection.queries)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        print("GOKIL")
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        messages.warning(request, 'Not Successful')

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/update_profile.html',context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed!')
            return redirect('profile')
        else:
            messages.success(request, 'There are errors during the update, Try again!')
            return redirect('change')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'users/change_password.html', {'form': form})

class WishlistView(ListView):
    model = Wishlist
    template_name = 'users/wishlist.html'
    context_object_name = 'wishlist'
    ordering = ['-datetime'] 
    paginate_by = 3

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = 'wishlist'
        return context