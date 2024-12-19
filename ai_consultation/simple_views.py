from django.shortcuts import render

# تابع صفحه اصلی
def home(request):
    return render(request, 'home.html')  # فایل home.html باید وجود داشته باشد
