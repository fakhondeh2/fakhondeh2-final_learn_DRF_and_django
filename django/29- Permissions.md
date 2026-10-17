## سرفصل: مجوزها و سطح دسترسی در DRF (Permissions in DRF)

### منابع آموزشی
- [راهنمای رسمی مجوزها در DRF](https://www.django-rest-framework.org/api-guide/permissions/)
- [راهنمای رسمی احراز هویت در DRF](https://www.django-rest-framework.org/api-guide/authentication/)

### تمرین عملی (روی یک کار واقعی)

در این تمرین، سیستم مجوزها (Permissions) را برای پروژه **mysite** و اپ **bookstore** پیاده‌سازی می‌کنیم. از ساده‌ترین مجوزها شروع کرده تا مجوزهای سفارشی و سطح-شیء.

---

**مرحله ۱: تنظیم مجوز پیش‌فرض در settings.py**

فایل `mysite/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

این تنظیم باعث می‌شود همه endpointها به صورت پیش‌فرض فقط برای کاربران احراز هویت شده قابل دسترس باشند.

---

**مرحله ۲: استفاده از AllowAny برای ثبت‌نام (Signup)**

ساخت View ثبت‌نام در `bookstore/views.py`:

```python
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
```

Serializer مربوطه در `bookstore/serializers.py`:

```python
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
```

---

**مرحله ۳: اضافه کردن مسیر Signup**

در `bookstore/urls.py`:

```python
from .views import SignupView

urlpatterns = [
    path('api/signup/', SignupView.as_view(), name='signup'),
]
```

تست:

```bash
curl -X POST http://127.0.0.1:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "newuser@example.com", "password": "pass123"}'
```

---

**مرحله ۴: استفاده از IsAdminUser برای پنل مدیریت**

در `bookstore/views.py`:

```python
from rest_framework import viewsets, permissions
from .models import AuditLog

class AdminOnlyViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
```

اگر مدل `AuditLog` ندارید، می‌توانید یک مدل ساده در `bookstore/models.py` ایجاد کنید:

```python
class AuditLog(models.Model):
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.action} by {self.user}"
```

تست:

```bash
# کاربر عادی
curl http://127.0.0.1:8000/api/audit-logs/ \
  -H "Authorization: Bearer $USER_TOKEN"
# پاسخ: 403 Forbidden

# کاربر ادمین
curl http://127.0.0.1:8000/api/audit-logs/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"
# پاسخ: 200 OK
```

---

**مرحله ۵: استفاده از IsAuthenticatedOrReadOnly برای View عمومی**

در `bookstore/views.py`:

```python
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

تست:

```bash
# خواندن بدون توکن مجاز است
curl http://127.0.0.1:8000/api/books/

# نوشتن بدون توکن ممنوع است
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "author": 1}'
# پاسخ: 401 Unauthorized
```

---

**مرحله ۶: آشنایی با Safe Methods (GET, HEAD, OPTIONS)**

DRF متدهای امن HTTP را تشخیص می‌دهد. `SAFE_METHODS` شامل:

```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

print(SAFE_METHODS)  # ('GET', 'HEAD', 'OPTIONS')
```

کد داخلی `IsAuthenticatedOrReadOnly` از این مفهوم استفاده می‌کند:

```python
class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated
        )
```

---

**مرحله ۷: ساخت Permission سفارشی - IsOwnerOrReadOnly**

فایل جدید `bookstore/permissions.py` ایجاد کنید:

```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    دسترسی نوشتن فقط برای صاحب شیء، خواندن برای همه
    """
    def has_object_permission(self, request, view, obj):
        # متدهای امن برای همه مجاز است
        if request.method in SAFE_METHODS:
            return True

        # نوشتن فقط برای صاحب شیء
        return obj.owner == request.user
```

---

**مرحله ۸: اعمال IsOwnerOrReadOnly روی یک View خاص**

فرض کنید مدل `Review` دارید که فیلد `owner` دارد:

```python
# bookstore/models.py
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.owner} on {self.book}"
```

View مربوطه:

```python
# bookstore/views.py
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

---

**مرحله ۹: ساخت Permission سفارشی - IsStaffOrReadOnly**

در `bookstore/permissions.py`:

```python
class IsStaffOrReadOnly(BasePermission):
    """
    کاربران staff می‌توانند بنویسند، بقیه فقط بخوانند
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
```

---

**مرحله ۱۰: ترکیب چند Permission class**

می‌توانید چند کلاس مجوز را با هم ترکیب کنید. DRF همه آن‌ها را بررسی می‌کند (AND منطقی):

```python
class RestrictedBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsStaffOrReadOnly,
    ]
```

در این ترکیب:
- کاربران احراز هویت نشده به هیچ وجه دسترسی ندارند (به خاطر `IsAuthenticated`)
- کاربران احراز هویت شده عادی فقط خواندن مجاز دارند
- کاربران staff می‌توانند بنویسند

---

**مرحله ۱۱: Permission سفارشی با منطق AND - بررسی زنجیره‌ای**

```python
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# ترکیب سه‌تایی
class SuperStrictViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
        IsOwnerOrReadOnly,
    ]
```

---

**مرحله ۱۲: Permission سفارشی با پارامتر - IsInGroup**

در `bookstore/permissions.py`:

```python
class IsInGroup(BasePermission):
    """
    فقط کاربرانی که در گروه مشخصی هستند دسترسی دارند
    """
    def __init__(self, group_name):
        self.group_name = group_name

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name=self.group_name).exists()

# استفاده در ویو
from rest_framework.views import APIView
from .permissions import IsInGroup

class ModeratorsOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsInGroup('moderators')]

    def get(self, request):
        return Response({"message": "Only moderators can see this"})
```

---

**مرحله ۱۳: Permission سطح-شیء در عمل (Object-Level Permission)**

بررسی `has_object_permission` فقط زمانی فراخوانی می‌شود که `has_permission` قبلاً `True` برگردانده باشد:

```python
class IsReviewOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# ViewSet با object-level permission
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]
```

تست:

```bash
# فرض کنید review با id=1 متعلق به user1 است
curl -X DELETE http://127.0.0.1:8000/api/reviews/1/ \
  -H "Authorization: Bearer $USER2_TOKEN"
# پاسخ: 403 Forbidden - چون user2 صاحب review نیست
```

---

**مرحله ۱۴: لاگین کردن دسترسی‌ها با Permission سفارشی**

در `bookstore/permissions.py`:

```python
import logging
logger = logging.getLogger(__name__)

class LoggedPermission(BasePermission):
    def has_permission(self, request, view):
        result = super().has_permission(request, view) if hasattr(super(), 'has_permission') else True
        logger.info(
            f"User {request.user} accessed {view.__class__.__name__} "
            f"via {request.method} -> {'ALLOWED' if result else 'DENIED'}"
        )
        return result
```

---

**مرحله ۱۵: Permission سفارشی بر اساس زمان (Time-Based)**

```python
from datetime import time

class BusinessHoursOnly(BasePermission):
    """
    فقط ساعت ۸ صبح تا ۶ عصر اجازه دسترسی بده
    """
    def has_permission(self, request, view):
        from datetime import datetime
        now = datetime.now().time()
        return time(8, 0) <= now <= time(18, 0)

# استفاده در ویوی حساس
class SensitiveDataView(APIView):
    permission_classes = [permissions.IsAuthenticated, BusinessHoursOnly]

    def get(self, request):
        return Response({"data": "highly sensitive"})
```

---

**مرحله ۱۶: تعیین Permission به صورت پویا در View**

می‌توانید متد `get_permissions()` را override کنید:

```python
class DynamicPermissionView(APIView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        return Response({"message": "public"})

    def post(self, request):
        return Response({"message": "authenticated only"})
```

---

**مرحله ۱۷: Permission سفارشی برای جلوگیری از Rate-Limiting دستی**

```python
class MaxItemsPerUser(BasePermission):
    """
    هر کاربر حداکثر ۵ کتاب می‌تواند ایجاد کند
    """
    max_items = 5

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.book_set.count() >= self.max_items:
            return False
        return True
```

---

**مرحله ۱۸: تست یکپارچه مجوزها با APITestCase**

فایل `bookstore/tests.py`:

```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

class PermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', password='pass123')
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')

    def test_anonymous_read_books(self):
        """کاربران ناشناس می‌توانند کتاب‌ها را بخوانند"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_book(self):
        """کاربران ناشناس نمی‌توانند کتاب ایجاد کنند"""
        response = self.client.post('/api/books/', {'title': 'Test', 'author': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_only_audit_logs(self):
        """فقط ادمین به لاگ‌ها دسترسی دارد"""
        # کاربر عادی
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/audit-logs/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # ادمین
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/audit-logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

اجرای تست:

```bash
python manage.py test bookstore.tests.PermissionTests
```

---

**خلاصه:** در این تمرین با انواع مجوزهای DRF شامل `IsAuthenticated`, `AllowAny`, `IsAdminUser`, `IsAuthenticatedOrReadOnly` آشنا شدیم. همچنین مجوزهای سفارشی در سطح درخواست (has_permission) و سطح شیء (has_object_permission) را پیاده‌سازی کردیم. ترکیب چند کلاس مجوز، مجوزهای زمان-محور و مجوزهای مبتنی بر گروه نیز بررسی شدند.