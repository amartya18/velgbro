from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    sold = models.BooleanField(default=False)
    # premium = models.ForeignKey()
    # if post.premium does not exist = post not premium

    slug = models.SlugField(max_length=100,blank=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug}) # new

    def save(self, *args, **kwargs):
        slug_save(self)
        super(Post, self).save(*args, **kwargs)

def slug_save(obj):
    if not obj.slug:  # if there isn't a slug
        obj.slug = get_random_string(100)  # create one
        slug_is_wrong = True
        while slug_is_wrong:  # keep checking until we have a valid slug
            slug_is_wrong = False
            other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
            if len(other_objs_with_slug) > 0:
                # if any other objects have current slug
                slug_is_wrong = True
            # naughty_words = list_of_swear_words_brand_names_etc
            # if obj.slug in naughty_words:
            #     slug_is_wrong = True
            if slug_is_wrong:
                # create another slug and check it again
                obj.slug = get_random_string(100)

class Premium(models.Model):
    name = models.CharField(max_length=100)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    # status = models.BooleanField(default=False)
    datetime = models.DateTimeField()
    # price (?)

# class WheelImage(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     image = models.ImageField()
