import stripe
from django.shortcuts import render, HttpResponse, Http404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from store.forms import PostForm, ProductForm
from products.models import Wheel
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY # new

# Create your views here.
def home_view(request):
    return HttpResponse("Main Page!")

class PostListView(ListView):
    model = Post
    context_object_name = 'posts' # used in template 
    template_name = 'store/home.html'
    ordering = ['-datetime'] # will use hit in the future


def charge_view(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount= 500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        context = {'object' : request.session.get('post_object')}
        return render(request, 'store/charge.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'store/detail.html'

    def get_context_data(self, **kwargs): # stripe
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['price_stripe'] = 500
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

@login_required
def create_post_view(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        product_form = ProductForm(request.POST)
        if post_form.is_valid() and product_form.is_valid():
            post = post_form.save(False)
            post.user = request.user
            post.datetime = timezone.now()
            product = product_form.save(False)
            product.post = post
            post.save()
            product.save()
            return redirect('post-list')
    else:
        post_form = PostForm(instance=Post())
        product_form = ProductForm(instance=Wheel())

        context = {}
        context['post_form'] = post_form
        context['product_form'] = product_form
        print(request.user.username)

        return render(request, "store/post_create.html", context)