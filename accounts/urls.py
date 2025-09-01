from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserListView

urlpatterns = [
    # POST {username, password} -> { access, refresh }
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inscription
    path('register/', RegisterView.as_view(), name='register'),

    # (optionnel) liste des users (admin)
    path('users/', UserListView.as_view(), name='user-list'),
]
