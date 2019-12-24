from django.urls import path, include
from store import views as store_view

urlpatterns = [
    path('', store_view.home_view, name='home'),
]