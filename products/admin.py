from django.contrib import admin
from products.models import Wheel, RingSize, Width, BoltPattern

# Register your models here.
admin.site.register(RingSize)
admin.site.register(Width)
admin.site.register(BoltPattern)
admin.site.register(Wheel)
