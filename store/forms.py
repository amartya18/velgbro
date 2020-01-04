from django.forms import ModelForm
from store.models import Post, WheelImage
from products.models import Wheel

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('premium',)

class ProductForm(ModelForm):
    class Meta:
        model = Wheel
        fields = ('model','name','ring_size','width','bolt_pattern')

class ImageForm(ModelForm):
    class Meta:
        model = WheelImage
        fields = ('image',)