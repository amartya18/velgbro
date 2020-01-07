from django.forms import ModelForm, ChoiceField
from django import forms
from store.models import Post, WheelImage, Comments
from products.models import Wheel

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('premium',)

class ProductForm(ModelForm):
    class Meta:
        model = Wheel
        fields = ('model','name', 'description', 'ring_size','width','bolt_pattern', 'color', 'material','offset', 'condition', 'price')


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

class CommentForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Insert Comment here...','rows':5,'cols':100}))

    class Meta:
        model = Comments
        fields = ('content',)

        