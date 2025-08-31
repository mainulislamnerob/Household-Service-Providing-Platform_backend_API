from django.urls import path
from .views import ServiceReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('services/<slug:slug>/reviews/', ServiceReviewListCreateView.as_view(), name='service_reviews'),
    path('reviews/<int:id>/', ReviewDetailView.as_view(), name='review_detail'),
]
