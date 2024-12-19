from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated

from .models import User, Advisor, Reservation, Consultation, Payment
from .serializers import (
    UserSerializer,
    AdvisorSerializer,
    ReservationSerializer,
    ConsultationSerializer,
    PaymentSerializer
)

import stripe
from django.conf import settings
import requests

# ViewSet برای ثبت نام کاربر
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # بدون نیاز به احراز هویت
    authentication_classes = []  # حذف کلاس‌های JWT Authentication

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کاربر با موفقیت ثبت شد", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View ثبت نام مستقل بدون نیاز به JWT
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # No need for authentication here

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کاربر با موفقیت ثبت شد", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet مشاوران (با IsAuthenticated)
class AdvisorViewSet(viewsets.ModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت شده دسترسی دارند.
    authentication_classes = []  # می‌توانید برای استفاده از توکن JWT از JWTAuthentication استفاده کنید


# ViewSet رزروها (با IsAuthenticated)
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت شده دسترسی دارند.
    authentication_classes = []  # مشابه بالا، اگر از JWT استفاده می‌کنید باید اینجا JWTAuthentication قرار دهید


# ViewSet مشاوره‌ها (با IsAuthenticated)
class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت شده دسترسی دارند.
    authentication_classes = []  # مانند قبل، اینجا می‌توانید از JWTAuthentication استفاده کنید

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "مشاوره ایجاد شد", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        consultations = Consultation.objects.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# صفحه اصلی
def home(request):
    return HttpResponse("Welcome to the consultation platform!")


# تنظیم Stripe برای پرداخت آنلاین
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@api_view(['POST'])
def process_payment(request):
    try:
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'usd')

        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency=currency,
            metadata={'integration_check': 'accept_a_payment'},
        )

        return Response({'client_secret': intent.client_secret})
    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# پرداخت از طریق زرین پال
@api_view(['POST'])
def process_zarinpal_payment(request):
    amount = request.data.get('amount')
    description = request.data.get('description', 'Payment description')
    email = request.data.get('email')
    mobile = request.data.get('mobile')

    data = {
        'merchant_id': 'your_zarinpal_merchant_id',
        'amount': amount,
        'description': description,
        'email': email,
        'mobile': mobile,
        'callback_url': 'http://localhost:8000/api/v1/payment/callback/',
    }

    response = requests.post('https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json', data=data)
    result = response.json()

    if result['Status'] == 100:
        return Response({'payment_url': f"https://www.zarinpal.com/pg/StartPay/{result['Authority']}"})
    else:
        return Response({'error': 'Payment request failed'}, status=status.HTTP_400_BAD_REQUEST)


# ViewSet پرداخت‌ها (با IsAuthenticated)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت شده دسترسی دارند.
    authentication_classes = []  # مانند قبل، می‌توانید از JWTAuthentication استفاده کنید
