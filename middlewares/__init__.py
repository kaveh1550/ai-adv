# ai_consultation/middlewares/__init__.py
# خالی بگذارید

# ai_consultation/middlewares/custom_middleware.py
from django.utils.deprecation import MiddlewareMixin

class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Middleware is processing the request")
