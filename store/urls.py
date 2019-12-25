from django.urls import path, include
from store import views as store_view
from store.views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]