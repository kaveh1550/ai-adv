from rest_framework import serializers
from .models import User, Advisor, Reservation, Consultation, Payment

# سریالایزر برای مدل User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # اضافه کردن تمام فیلدهای مدل User

# سریالایزر برای مدل Advisor
class AdvisorSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # استفاده از سریالایزر User برای مشاور

    class Meta:
        model = Advisor
        fields = ['id', 'user', 'expertise', 'hourly_rate']

# سریالایزر برای مدل Reservation
class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # کاربر مربوط به رزرو
    advisor = AdvisorSerializer()  # مشاور مربوط به رزرو

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'advisor', 'scheduled_time', 'status']

# سریالایزر برای مدل Consultation
class ConsultationSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()  # رزرو مربوط به مشاوره

    class Meta:
        model = Consultation
        fields = ['id', 'reservation', 'consultation_time', 'notes', 'cost', 'status']

# سریالایزر برای مدل Payment
class PaymentSerializer(serializers.ModelSerializer):
    advisor = AdvisorSerializer()  # مشاور مربوط به پرداخت
    client = UserSerializer()  # کاربر مربوط به پرداخت

    class Meta:
        model = Payment
        fields = ['id', 'advisor', 'client', 'amount', 'status', 'transaction_date']

# سریالایزر Consultation اضافی از کد‌های شما
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'
