from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    sold = models.BooleanField(default=False)
    # premium = models.ForeignKey()
    # if post.premium does not exist = post not premium

class Premium(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    datetime = models.DateTimeField()

class WheelImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()