from django.urls import path, include
from store import views as store_view
# from store.views import post_list_view, PostDetailView
from store.views import HomePageView, SearchResultView, PostDetailView

urlpatterns = [
    # path('', store_view.post_list_view, name='post-list'),
    path('post/', store_view.create_post_view, name='create-post'),
    path('search/', store_view.SearchResultView.as_view(), name='search-results'),
    path('', store_view.HomePageView.as_view(), name='home'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('charge', store_view.charge_view, name='post-charge'),
    path('success', store_view.charge_view, name='payment-success'),
    path('webhook', store_view.my_webhook_view, name='webhook'),
]