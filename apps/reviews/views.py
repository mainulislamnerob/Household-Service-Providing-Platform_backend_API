from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from apps.services.models import Service
from apps.orders.models import Order, OrderItem

class ServiceReviewListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        qs = service.reviews.select_related("user").order_by("-created_at")
        return Response(ReviewSerializer(qs, many=True).data)

    def post(self, request, slug):
        if not request.user.is_authenticated:
            return Response({"detail":"Authentication required"}, status=401)
        service = get_object_or_404(Service, slug=slug, is_active=True)

        # Only allow users who have an order for this service to review
        has_order = OrderItem.objects.filter(order__user=request.user, service=service).exists()
        if not has_order:
            return Response({"detail":"You can only review services you have ordered."}, status=403)

        ser = ReviewSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        # enforce uniqueness per user-service
        if Review.objects.filter(user=request.user, service=service).exists():
            return Response({"detail":"You already reviewed this service."}, status=400)
        review = Review.objects.create(
            user=request.user,
            service=service,
            rating=ser.validated_data["rating"],
            comment=ser.validated_data.get("comment", ""),
        )
        return Response(ReviewSerializer(review).data, status=201)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can edit only your own review")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can delete only your own review")
        instance.delete()
