import jwt
import logging
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured

# پیکربندی لاگ‌ها
logger = logging.getLogger(__name__)

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # بررسی مقدار JWT_SECRET
        if not hasattr(settings, 'JWT_SECRET') or not settings.JWT_SECRET:
            logger.error("کلید JWT_SECRET در تنظیمات یافت نشد.")
            raise ImproperlyConfigured('JWT_SECRET تنظیم نشده است!')

    def __call__(self, request):
        token = request.headers.get('Authorization')

        if not token:
            logger.warning("توکن در هدر درخواست موجود نیست.")
            return JsonResponse({'message': 'توکن موجود نیست'}, status=403)

        try:
            # حذف "Bearer " از ابتدای توکن
            token = token.split(' ')[1] if token.startswith('Bearer ') else token

            # بررسی اعتبار توکن
            decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

            # افزودن اطلاعات کاربر به درخواست
            request.user = decoded
        except jwt.ExpiredSignatureError:
            logger.warning("توکن منقضی شده است.")
            return JsonResponse({'message': 'توکن منقضی شده است'}, status=401)
        except jwt.InvalidTokenError:
            logger.error("توکن معتبر نیست.")
            return JsonResponse({'message': 'توکن معتبر نیست'}, status=401)
        except Exception as e:
            logger.exception(f"خطا در پردازش توکن: {str(e)}")
            return JsonResponse({'message': f'خطا در پردازش توکن: {str(e)}'}, status=500)

        response = self.get_response(request)
        return response
