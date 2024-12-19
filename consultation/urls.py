from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # اضافه کردن Import
from .views import (
    RegisterUserView,
    UserViewSet,
    AdvisorViewSet,
    ReservationViewSet,
    ConsultationViewSet,
    PaymentViewSet,
    process_payment,
    process_zarinpal_payment
)

# تنظیم Router برای ViewSet‌ها
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'advisors', AdvisorViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    # ثبت نام کاربر جدید بدون نیاز به احراز هویت
    path('api/users/register/', RegisterUserView.as_view(), name='register'),

    # مسیر پرداخت‌ها
    path('api/v1/process_payment/', process_payment, name='process_payment'),
    path('api/v1/zarinpal_payment/', process_zarinpal_payment, name='process_zarinpal_payment'),

    # شامل کردن مسیرهای ViewSet‌ها
    path('api/v1/', include(router.urls)),

    # مسیرهای مربوط به JWT Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
