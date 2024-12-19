from django.shortcuts import render

# ویو صفحه اصلی
def home(request):
    return render(request, 'home.html')  # رندر کردن صفحه home.html
