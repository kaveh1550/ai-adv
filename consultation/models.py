from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Manager سفارشی برای User
class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError(_('\u0641\u06cc\u0644\u062f \u0627\u06cc\u0645\u06cc\u0644 \u0628\u0627\u06cc\u062f \u0645\u0634\u062e\u0635 \u0634\u0648\u062f'))
        if not phone_number:
            raise ValueError(_('\u0641\u06cc\u0644\u062f \u0634\u0645\u0627\u0631\u0647 \u062a\u0644\u0641\u0646 \u0628\u0627\u06cc\u062f \u0645\u0634\u062e\u0635 \u0634\u0648\u062f'))

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('\u0633\u0648\u067e\u0631\u0648\u0627\u06cc\u0632\u0631 \u0628\u0627\u06cc\u062f is_staff=True \u062f\u0627\u0634\u062a\u0647 \u0628\u0627\u0634\u062f'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('\u0633\u0648\u067e\u0631\u0648\u0627\u06cc\u0632\u0631 \u0628\u0627\u06cc\u062f is_superuser=True \u062f\u0627\u0634\u062a\u0647 \u0628\u0627\u0634\u062f'))

        return self.create_user(email, phone_number, password, **extra_fields)

# مدل User سفارشی
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('client', _('\u0645\u0634\u062a\u0631\u06cc')),
        ('advisor', _('\u0645\u0634\u0627\u0648\u0631')),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        db_table = 'user_new'

# مدل Advisor
class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='advisor_profile')
    expertise = models.CharField(max_length=255)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.expertise}"

    class Meta:
        db_table = 'advisor_new'

# مدل Client
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'client_new'

# مدل Reservation
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='reservations')
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Reservation by {self.user} with {self.advisor} on {self.scheduled_time}"

    class Meta:
        db_table = 'reservation_new'
        indexes = [
            models.Index(fields=['user', 'advisor']),  # ایجاد ایندکس ترکیبی
        ]

# مدل Consultation با مقدار پیش‌فرض consultation_time
class Consultation(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', _('Scheduled')),
        ('In Progress', _('In Progress')),
        ('Completed', _('Completed')),
        ('Cancelled', _('Cancelled')),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='consultations', null=True, blank=True)
    advisor = models.ForeignKey('Advisor', on_delete=models.CASCADE, related_name='consultations', null=True, blank=True)
    reservation = models.OneToOneField('Reservation', null=True, blank=True, on_delete=models.CASCADE, related_name='consultation')
    consultation_time = models.DateTimeField(default=timezone.now)  # مقدار پیش‌فرض consultation_time
    notes = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation for {self.client} with {self.advisor}"

    class Meta:
        db_table = 'consultation_new'

# مدل Payment برای پرداخته‌ها
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]

    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='advisor_payments')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.advisor.user.first_name} {self.advisor.user.last_name} - {self.client.first_name} {self.client.last_name} - {self.amount} - {self.status}"

    class Meta:
        db_table = 'payment_new'
