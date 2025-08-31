from rest_framework import status, generics, views, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer, RoleUpdateSerializer
from .permissions import IsAdmin
from apps.orders.models import Order

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class MyProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user.profile).data)

    def put(self, request):
        prof = request.user.profile
        ser = ProfileSerializer(prof, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

class MyHistoryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        # minimal representation
        data = [{
            "id": o.id,
            "status": o.status,
            "payment_status": o.payment_status,
            "total_amount": str(o.total_amount),
            "created_at": o.created_at.isoformat(),
            "items": [{"service": i.service.name, "quantity": i.quantity, "unit_price": str(i.unit_price)} for i in o.items.all()]
        } for o in orders]
        return Response(data)

class AdminUsersView(views.APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        qs = User.objects.all().order_by("id")
        return Response(UserSerializer(qs, many=True).data)

class AdminUserRoleView(views.APIView):
    permission_classes = [IsAdmin]
    def patch(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail":"User not found"}, status=404)
        ser = RoleUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        role = ser.validated_data["role"]
        user.role = role
        user.is_staff = (role == "ADMIN")
        user.save()
        return Response({"detail":"Role updated", "user": UserSerializer(user).data})
