import logging
from django.http import JsonResponse

# پیکربندی لاگ‌ها
logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # ثبت جزئیات کامل خطا
            logger.exception(f"خطای داخلی سرور: {str(e)}")
            return JsonResponse({'message': 'خطای داخلی سرور'}, status=500)
