from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.urls import reverse
from PIL import Image

class Premium(models.Model):
    name = models.CharField(max_length=100) # basic or premium
    price = models.CharField(max_length=10)

    def __str__(self):
        return self.name

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    premium = models.ForeignKey(Premium, on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100,blank=True)

    def __str__(self):
        return "{} {} {}".format(self.wheel.model.brand.brand, self.wheel.model.model, self.wheel.name)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug}) # new

    def get_images(self):
        return self.wheelimage_set.all()

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

class WheelImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='post_images', verbose_name='Image')

    def save(self, *args, **kwargs):
        super(WheelImage, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
