from django.db import models
from django.utils import timezone
from store.models import Post

class Brand(models.Model):
    brand = models.CharField(max_length=100)

class Model(models.Model):
    model = models.CharField(max_length=100)
    idbrand = models.ForeignKey(Brand, on_delete=models.CASCADE)

class Bolt_Pattern(models.Model):
    boltpattern = models.CharField(max_length=100)

class RingSize(models.Model):
    ringsize = models.IntegerField()

class Width(models.Model):
    width = models.FloatField(max_length=10)

class Material(models.Model):
    material = models.CharField(max_length=100)

class Color(models.Model):
    color = models.CharField(max_length=100
                             )
class Wheel(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, default='')
    date_time = models.DateTimeField(default='')
    bolt_pattern = models.ForeignKey(Bolt_Pattern, on_delete=models.DO_NOTHING, default='')
    ring_size = models.ForeignKey(RingSize, on_delete=models.DO_NOTHING, default='')
    width = models.ForeignKey(Width, on_delete=models.DO_NOTHING, default='')
    offset = models.IntegerField(null=True)
    # new_used = models.BooleanField(default=True)
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING, default='')
    description = models.CharField(max_length=255, default='')
    material = models.ForeignKey(Material, null=True, on_delete=models.DO_NOTHING)
    price = models.CharField(max_length=10, default=0)



