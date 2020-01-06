from django.forms import ModelForm, ChoiceField
from store.models import Post, WheelImage
from products.models import Wheel

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('premium',)

class ProductForm(ModelForm):
    class Meta:
        model = Wheel
        fields = ('model','name','ring_size','width','bolt_pattern', 'color', 'material','offset', 'condition', 'price')


# class ProductForm(ProductBaseForm):
#     offset_type_choice = (('',''),('+','+'),('-','-'))
#     offset_type = ChoiceField(choices=offset_type_choice)

#     class Meta:
#         model = Wheel
#         fields = ProductBaseForm.Meta.fields + ('offset_type',)


class ImageForm(ModelForm):
    class Meta:
        model = WheelImage
        fields = ('image',)