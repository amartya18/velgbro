from django.db import models
from store.models import Post
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from products.validators import my_blank_validator

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

class Brand(models.Model):
    brand = models.CharField(max_length=50)

    def __str__(self):
        return self.brand

class Model(models.Model):
    model = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.model

class Color(models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.color

class Material(models.Model):
    material = models.CharField(max_length=50)

    def __str__(self):
        return self.material

class Wheel(models.Model): # everything should be CASCADE
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='wheel')
    name = models.CharField(max_length=50, blank=True)
    ring_size = models.ForeignKey(RingSize, on_delete=models.CASCADE)
    width = models.ForeignKey(Width, on_delete=models.CASCADE)
    bolt_pattern = models.ForeignKey(BoltPattern, on_delete=models.CASCADE)

    # validators=[MaxValueValidator(50), MinValueValidator(-50)]
    offset = models.IntegerField(default=None, null=True, blank=True)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.SET_NULL)
    condition_choices = [
        ('NEW','New'),
        ('USED','Used'),
    ]
    condition = models.CharField(
        max_length=4,
        choices=condition_choices,
        # default='',
    )
    material = models.ForeignKey(Material, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(validators=[MaxLengthValidator(2500)])


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # save offset value based on offset type (+/-)
        super(Wheel, self).save(*args, **kwargs)
        # self.offset_type
        # if self.offset_type == '-':
        #     self.offset *= -1
