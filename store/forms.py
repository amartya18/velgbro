from django.forms import ModelForm
from store.models import Post
from products.models import Wheel

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ()
class ProductForm(ModelForm):
    class Meta:
        model = Wheel
        fields = ('name',)