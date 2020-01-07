import json
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import Http404, HttpResponse, get_object_or_404, redirect, render, reverse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Post, WheelImage, Premium
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from store.forms import PostForm, ProductForm, ImageForm
from products.models import Wheel, RingSize, Width, BoltPattern, Brand, Model
from django.utils import timezone
from django.db.models import Q
from django.forms.models import modelformset_factory
from urllib.parse import urlencode
from users.models import Wishlist
from store.models import Post
from users.models import Wishlist
from django.core.paginator import Paginator
from store.forms import CommentForm
from django.views.generic.edit import FormMixin

stripe.api_key = settings.STRIPE_SECRET_KEY # new

# Create your views here.
class HomePageView(ListView):
    template_name = 'store/home.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ringsize'] = RingSize.objects.all()
        context['width'] = Width.objects.all()
        context['boltpattern'] = BoltPattern.objects.all()
        context['brand'] = Brand.objects.all()
        context['model'] = Model.objects.all()
        context['nbar']='home'
        # context['hot_wheels'] = Paginator(Post.objects.all(), 8).page(1)
        return context

class SearchResultView(ListView): # search result 
    paginate_by=10
    model = Post
    template_name = 'store/search_result.html'
    context_object_name = 'posts'
    ordering = ['-datetime'] # will use hit in the future

    # def get_ordering(self):
    #     ordering = self.request.GET.get('ordering', 'premium.price')
    #     ordering.order_by('datetime')
    #     return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ringsize'] = RingSize.objects.all()
        context['width'] = Width.objects.all()
        context['boltpattern'] = BoltPattern.objects.all()
        context['brand'] = Brand.objects.all()
        context['model'] = Model.objects.all()
        context['nbar']='search'
        context['current']=self.request.GET['ringsize']
        
        context['sorted_posts']= Post.objects.filter(sold=False).order_by('premium.price').order_by('-datetime')

        return context

    def get_queryset(self):
        # name = self.request.GET.get('name')
        ring_size = self.request.GET['ringsize']
        width = self.request.GET['width']
        bolt_pattern = self.request.GET['boltpattern']
        brand = self.request.GET['brand']
        model = self.request.GET['model']
        posts = Post.objects.filter(
            # Q(wheel__name__icontains=name) 
            Q(wheel__ring_size__ring_size__icontains=ring_size) & Q(wheel__width__width__icontains=width) & Q(wheel__bolt_pattern__bolt_pattern__icontains=bolt_pattern) & Q(wheel__model__brand__brand__icontains=brand) & Q(wheel__model__model__icontains=model)
        )
        return posts


# temp
def charge_view(request):
    if request.method == 'GET' and 'stripe_redirect' in request.session:
        print("STRIPE")
        post_slug = request.GET.get('post_slug')
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'name': 'Velgbro Premium',
                'description': 'Premium Velgbro Post',
                'amount': '7000000',
                'currency': 'idr',
                'quantity': 1,
            }],
            success_url='http://localhost:8000/detail/{}'.format(post_slug),
            cancel_url='http://localhost:8000/', #cancel payment
            # cancel_url=Http404,
            client_reference_id = post_slug,
        )
        return render(request, 'store/charge.html', {'sessionId': session['id']})
    elif request.method == 'POST':
        raise Http404

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key
    )

  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # Fulfill the purchase...
    print("STRIPE PAYING")
    post = Post.objects.filter(slug=session['client_reference_id']).first()
    post.premium = Premium.objects.filter(name='premium').first()
    post.save()

  return HttpResponse(status=200)

# temp
class PostDetailView(FormMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'store/detail.html'
    form_class = CommentForm

    # def get_success_url(self):
    #     return reverse('post-detail', kwargs={'slug': self.object.slug })

    def get_context_data(self, **kwargs): # stripe
        context = super().get_context_data(**kwargs)
        current_wishlist = Wishlist.objects.filter(user=self.request.user)
        context['current_wishlist'] = current_wishlist.filter(wheel=self.object).first()
        context['current_user'] = self.request.user

        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        print("POST")
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = self.request.user
            comment.save()
            return redirect('post-detail', self.object.slug)
        else:
            return Http404

        # post = get_object_or_404(Post, slug=slug)
        # if request.method == "POST":
        #     form = CommentForm(request.POST)
        #     if form.is_valid():
        #         comment = form.save(commit=False)
        #         comment.post = post
        #         comment.save()
        #         return redirect('post_detail', slug=post.slug)
        # else:
        #     form = CommentForm()
        # return render(request, 'blog/detail.html', {'form': form})
        
    # def form_valid(self, form):
    #     form.save()
    #     return super(PostDetailView, self).form_valid(form)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

@login_required
def create_post_view(request):
    ImageFormSet = modelformset_factory(WheelImage, form=ImageForm, extra=2) # extra = max amount of photos 
    if request.method == "POST":
        post_form = PostForm(request.POST)
        product_form = ProductForm(request.POST)
        image_form = ImageFormSet(request.POST, request.FILES)
        if post_form.is_valid() and product_form.is_valid() and image_form.is_valid():
            post = post_form.save(False)
            post.user = request.user
            post.datetime = timezone.now()
            post.premium = Premium.objects.filter(name='basic').first()
            product = product_form.save(False)
            product.post = post

            # print("OFFSET TYPE:")
            # print(post_form)
            # post.cleaned_data.pop('offset_type')

            post.save()
            product.save()

            for form in image_form.cleaned_data:
                try:
                    photo = WheelImage(post=post, image=form['image'])
                    photo.save()
                except Exception as e:
                    print("Picture Error")
                    break

            if int(request.POST['premium']) == Premium.objects.filter(name='premium').first().pk:
                print("PREMIUM")
                request.session['stripe_redirect'] = True
                # redirect to stripe payment then success page
                base_url = reverse('post-charge')
                query_string = urlencode({'post_slug': post.slug})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)

            elif int(request.POST['premium']) == Premium.objects.filter(name='basic').first().pk:
                print("BASIC")
                # redirect to success page
                return redirect('post-detail', slug=post.slug)

    else:
        post_form = PostForm(instance=Post())
        product_form = ProductForm(instance=Wheel())
        image_form = ImageFormSet(queryset=WheelImage.objects.none())

        context = {}
        context['post_form'] = post_form
        context['product_form'] = product_form
        context['image_form'] = image_form
        context['nbar']='post'

        return render(request, "store/post_create.html", context)

def post_update_view(request, slug):
    post = Post.objects.filter(slug=slug).first()
    if request.method == 'POST':
        wheel_form = ProductForm(request.POST, instance=post.wheel)
        if wheel_form.is_valid():
            wheel_form.save()
            messages.success(request, 'Update Successful')
            return redirect('post-detail', slug=slug)
        else:
            messages.warning(request, 'Error')
    else:
        wheel_form = ProductForm(instance=post.wheel)
    return render(request, 'store/update.html', {'wheel_form': wheel_form})

def post_delete_view(request, slug):
    post = Post.objects.filter(slug=slug).first()
    if request.method =='GET':
        post.delete()
        messages.success(request, 'Delete Successful')
        return redirect('profile')
    else:
        return Http404

def add_wishlist_view(request, slug):
    post = Post.objects.filter(slug=slug).first()
    new_wishlist = Wishlist(user=request.user, wheel=post)
    new_wishlist.save()
    return redirect('post-detail', slug=slug)

class WishlistView(ListView):
    model = Wishlist
    template_name = 'store/wishlist.html'
    context_object_name = 'wishlist'
    ordering = ['-datetime'] 

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = 'wishlist'
        return context

def post_sold(request, slug):
    if request.method == 'GET':
        post = get_object_or_404(Post, slug=slug)
        post.sold = True
        post.save()
        return redirect('post-detail', slug=slug)
