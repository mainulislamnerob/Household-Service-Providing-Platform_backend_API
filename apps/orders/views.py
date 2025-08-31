from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, CheckoutSerializer
from apps.users.permissions import IsAdmin

class CheckoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = CheckoutSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        order = ser.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class MyOrdersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

class AdminOrdersView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("-created_at")

class AdminOrderStatusView(views.APIView):
    permission_classes = [IsAdmin]
    def patch(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({"detail":"Order not found"}, status=404)
        status_value = request.data.get("status")
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({"detail":"Invalid status"}, status=400)
        order.status = status_value
        order.save()
        return Response(OrderSerializer(order).data)
