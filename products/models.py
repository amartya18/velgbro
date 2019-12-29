from django.db import models
from store.models import Post

class RingSize(models.Model):
    ring_size = models.IntegerField()

    def __str__(self):
        return str(self.ring_size)

class Width(models.Model):
    width = models.CharField(max_length=10)

    def __str__(self):
        return self.width

class BoltPattern(models.Model):
    bolt_pattern = models.CharField(max_length=100)

    def __str__(self):
        return self.bolt_pattern

class Wheel(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='wheel')
    name = models.CharField(max_length=50)
    ring_size = models.ForeignKey(RingSize, on_delete=models.DO_NOTHING)
    width = models.ForeignKey(Width, on_delete=models.DO_NOTHING)
    bolt_pattern = models.ForeignKey(BoltPattern, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name