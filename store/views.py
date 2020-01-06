import json
import stripe
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, HttpResponse, Http404, redirect, reverse
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

stripe.api_key = settings.STRIPE_SECRET_KEY # new

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ringsize'] = RingSize.objects.all()
        context['width'] = Width.objects.all()
        context['boltpattern'] = BoltPattern.objects.all()
        context['brand'] = Brand.objects.all()
        context['model'] = Model.objects.all()
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
            success_url='http://localhost:8000/{}'.format(post_slug),
            cancel_url='http://localhost:8000/cancel',
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
    post = Post.objects.filter(slug=session['client_reference_id']).first()
    post.premium = Premium.objects.all()[1]
    post.save()

  return HttpResponse(status=200)

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
    ImageFormSet = modelformset_factory(WheelImage, form=ImageForm, extra=2) # extra = max amount of photos 
    if request.method == "POST":
        post_form = PostForm(request.POST)
        product_form = ProductForm(request.POST)
        image_form = ImageFormSet(request.POST, request.FILES)
        if post_form.is_valid() and product_form.is_valid() and image_form.is_valid():
            post = post_form.save(False)
            post.user = request.user
            post.datetime = timezone.now()
            post.premium = Premium.objects.all()[0]
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

            if request.POST['premium'] == '2':
                print("PREMIUM")
                request.session['stripe_redirect'] = True
                # redirect to stripe payment then success page
                base_url = reverse('post-charge')
                query_string = urlencode({'post_slug': post.slug})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)

            elif request.POST['premium'] == '1':
                print("basic")
                # redirect to success page
                return redirect('post-detail', slug=post.slug)

            return Http404
    else:
        post_form = PostForm(instance=Post())
        product_form = ProductForm(instance=Wheel())
        image_form = ImageFormSet(queryset=WheelImage.objects.none())

        context = {}
        context['post_form'] = post_form
        context['product_form'] = product_form
        context['image_form'] = image_form

        return render(request, "store/post_create.html", context)
