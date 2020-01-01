from django.contrib import admin
from .models import Post, WheelImage
from products.models import Wheel


class WheelInline(admin.StackedInline):
    model = Wheel

# added wheels attribute here
class PostAdmin(admin.ModelAdmin):
    inlines = [
        WheelInline
    ]

    list_display = ('wheel_name', 'wheel_ring_size', 'wheel_width', 'wheel_bolt_pattern', 'user', 'datetime')

    def wheel_name(self, post):
        return post.wheel

    def wheel_ring_size(self, post):
        return post.wheel.ring_size

    def wheel_width(self, post):
        return post.wheel.width

    def wheel_bolt_pattern(self, post):
        return post.wheel.bolt_pattern

admin.site.register(WheelImage)
admin.site.register(Post, PostAdmin)