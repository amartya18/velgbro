from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from .models import Post

# Create your views here.
def home_view(request):
    return HttpResponse("Main Page!")

class HomeView(ListView):
    model = Post
    context_object_name = 'posts' # used in template 
    template_name = 'store/home.html'
    ordering = ['-datetime'] # hit