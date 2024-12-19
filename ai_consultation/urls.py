from django.contrib import admin
from django.urls import path, include  # استفاده از include برای ارجاع به urls دیگر

urlpatterns = [
    path('admin/', admin.site.urls),  # مسیر پنل مدیریت
    path('api/v1/', include('consultation.urls')),  # مسیرهای API برای اپلیکیشن consultation
    path('', include('consultation.urls')),  # صفحه اصلی و مسیرهای اپلیکیشن مشاوره
]
