from django.urls import path, include
from store import views as store_view
# from store.views import post_list_view, PostDetailView
from store.views import PostListView, PostDetailView

urlpatterns = [
    # path('', store_view.post_list_view, name='post-list'),
    path('post/', store_view.create_post_view, name='create-post'),
    path('', store_view.PostListView.as_view(), name='post-list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('charge', store_view.charge_view, name='charge-success'),
]