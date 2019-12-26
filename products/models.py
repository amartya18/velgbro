from django.db import models
from store.models import Post

class Wheel(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
