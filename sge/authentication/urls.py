from django.urls import path
from rest_framework_simplejwt import views


urlpatterns = [
    path('auth/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', views.TokenVerifyView.as_view(), name='token_verify')
]
