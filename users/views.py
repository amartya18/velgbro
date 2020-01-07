from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm

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
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_view(request):
    pagination=10
    return render(request, 'users/profile.html',{'nbar':'profile'})

def update_view(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
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
            messages.error(request, 'Please correct the error')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'users/change_password.html', {'form': form})