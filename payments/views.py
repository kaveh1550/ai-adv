from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def process_payment(request):
    # دریافت داده‌های ارسال‌شده
    data = request.data
    
    # بررسی داده‌های ورودی
    if 'amount' not in data or 'currency' not in data:
        return Response({'detail': 'اطلاعات برای اعتبارسنجی ارسال نشده است.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # منطق پردازش پرداخت
    amount = data['amount']
    currency = data['currency']
    
    # (اینجا منطق پرداخت اضافه می‌شود)
    return Response({'status': 'success', 'amount': amount, 'currency': currency})
