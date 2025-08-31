from django.urls import path
from .views import RegisterView, MeView, MyProfileView, MyHistoryView, AdminUsersView, AdminUserRoleView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),

    # profile
    path('profile/me/', MyProfileView.as_view(), name='my_profile'),
    path('profile/me/history/', MyHistoryView.as_view(), name='my_history'),

    # admin
    path('admin/users/', AdminUsersView.as_view(), name='admin_users'),
    path('admin/users/<int:user_id>/role/', AdminUserRoleView.as_view(), name='admin_user_role'),
]
