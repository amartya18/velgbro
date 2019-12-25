from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post
from django.conf import settings

# Create your views here.
def home_view(request):
    return HttpResponse("Main Page!")

class PostListView(ListView):
    model = Post
    context_object_name = 'posts' # used in template 
    template_name = 'store/home.html'
    ordering = ['-datetime'] # will use hit in the future

    def get_context_data(self, **kwargs): # stripe
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'store/detail.html'