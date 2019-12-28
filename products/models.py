from django.db import models
from store.models import Post

class Wheel(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='wheel')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name