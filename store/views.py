import stripe
from django.shortcuts import render, HttpResponse, Http404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Post, WheelImage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from store.forms import PostForm, ProductForm, ImageForm
from products.models import Wheel, RingSize, Width, BoltPattern
from django.utils import timezone
from django.db.models import Q
from django.forms.models import modelformset_factory

stripe.api_key = settings.STRIPE_SECRET_KEY # new

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ringsize'] = RingSize.objects.all()
        context['width'] = Width.objects.all()
        context['boltpattern'] = BoltPattern.objects.all()
        return context

class SearchResultView(ListView): # search result 
    model = Post
    template_name = 'store/search_result.html'
    context_object_name = 'posts'
    ordering = ['-datetime'] # will use hit in the future

    def get_queryset(self):
        # name = self.request.GET.get('name')
        ring_size = self.request.GET['ringsize']
        width = self.request.GET['width']
        bolt_pattern = self.request.GET['boltpattern']
        posts = Post.objects.filter(
            # Q(wheel__name__icontains=name) 
            Q(wheel__ring_size__ring_size__icontains=ring_size) & Q(wheel__width__width__icontains=width) & Q(wheel__bolt_pattern__bolt_pattern__icontains=bolt_pattern)
        )
        return posts


# temp
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

# temp
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
    # ImageFormSet = modelformset_factory(WheelImage, fields=('image',), extra=2) # extra = max amount of photos 
    ImageFormSet = modelformset_factory(WheelImage, form=ImageForm, extra=2) # extra = max amount of photos 
    if request.method == "POST":
        post_form = PostForm(request.POST)
        product_form = ProductForm(request.POST)
        image_form = ImageFormSet(request.POST, request.FILES)
        if post_form.is_valid() and product_form.is_valid() and image_form.is_valid():
            post = post_form.save(False)
            post.user = request.user
            post.datetime = timezone.now()
            product = product_form.save(False)
            product.post = post
            post.save()
            product.save()


            for form in image_form.cleaned_data:
                try:
                    photo = WheelImage(post=post, image=form['image'])
                    photo.save()
                except Exception as e:
                    print("Error")
                    break
            return redirect('home')
    else:
        post_form = PostForm(instance=Post())
        product_form = ProductForm(instance=Wheel())
        image_form = ImageFormSet(queryset=WheelImage.objects.none())

        context = {}
        context['post_form'] = post_form
        context['product_form'] = product_form
        context['image_form'] = image_form
        print(request.user.username)

        return render(request, "store/post_create.html", context)
