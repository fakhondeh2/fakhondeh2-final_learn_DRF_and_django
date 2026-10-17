## سرفصل: Exception Handling

### منابع آموزشی

**مستندات رسمی DRF:**
- [Exceptions — مرجع کامل Exceptionها در DRF، کلاس APIException و custom exception_handler](https://www.django-rest-framework.org/api-guide/exceptions/)

**مستندات رسمی Django:**
- [Django Logging — نحوه پیکربندی logging در Django برای ثبت خطاها](https://django.readthedocs.io/en/5.2.x/topics/logging.html)
- [Django Exception Handling — خطاهای پیش‌فرض Django و نحوه سفارشی‌سازی آن‌ها](https://django.readthedocs.io/en/5.2.x/ref/exceptions.html)

---
### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. می‌خواهیم یک سیستم مدیریت خطای یکپارچه برای API خود داشته باشیم. خطاهای ۴۰۴، ۴۰۰ و ۵۰۰ را با ساختاری یکسان به کلاینت برمی‌گردانیم، Exceptionهای سفارشی می‌سازیم و خطاها را در فایل لاگ ثبت می‌کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت `APIException` و کلاس‌های خطای پیش‌فرض DRF**  
   DRF یک کلاس پایه به نام `APIException` دارد که همه Exceptionهای DRF از آن ارث‌بری می‌کنند. کلاس‌های آماده مثل `NotFound`، `ValidationError`، `PermissionDenied`، `AuthenticationFailed` و `NotAcceptable` هر کدام یک کد وضعیت HTTP پیش‌فرض و یک `detail` پیش‌فرض دارند. نحوه کار این کلاس‌ها را در مستندات بررسی می‌کنیم.

2. **ساخت یک Exception سفارشی `BookNotFound`**  
   یک کلاس سفارشی به نام `BookNotFound` می‌سازیم که از `APIException` ارث‌بری می‌کند:
   ```python
   from rest_framework.exceptions import APIException

   class BookNotFound(APIException):
       status_code = 404
       default_detail = 'کتاب درخواست‌شده یافت نشد.'
       default_code = 'book_not_found'
   ```
   این Exception را در ویوهایی که کتاب بر اساس `id` یا `isbn` پیدا نمی‌کنند، استفاده می‌کنیم.

3. **بررسی سه ویژگی اصلی `APIException`: `detail`، `status_code` و `code`**  
   هر Exception شامل: `detail` (متن خطا برای کاربر)، `status_code` (کد HTTP) و `code` (شناسه خطا برای کلاینت) است. یک Exception سفارشی دیگر به نام `OutOfStockError` با `status_code=400`، `default_detail='کتاب در انبار موجود نیست'` و `default_code='out_of_stock'` می‌سازیم. این Exception را برای خرید کتاب ناموجود استفاده می‌کنیم.

4. **پیاده‌سازی `custom_exception_handler` جهانی**  
   در `shop/utils.py` یک تابع `custom_exception_handler` می‌نویسیم:
   ```python
   from rest_framework.views import exception_handler

   def custom_exception_handler(exc, context):
       response = exception_handler(exc, context)
       if response is not None:
           response.data = {
               'error_code': getattr(exc, 'default_code', 'error'),
               'message': response.data.get('detail', str(exc)),
               'status_code': response.status_code,
           }
       return response
   ```
   این تابع ساختار خطا را استاندارد می‌کند و به جای `detail` محض، یک آبجکت با کلیدهای `error_code`، `message` و `status_code` برمی‌گرداند.

5. **ثبت `custom_exception_handler` در `settings.py`**  
   در `REST_FRAMEWORK` تنظیمات DRF، `EXCEPTION_HANDLER` را به تابع خودمان اشاره می‌دهیم:
   ```python
   REST_FRAMEWORK = {
       'EXCEPTION_HANDLER': 'shop.utils.custom_exception_handler',
   }
   ```
   از این به بعد همه خطاهای DRF از این Handler عبور می‌کنند.

6. **استفاده از `set_rollback()` برای عملیات اتمی**  
   وقتی در یک Transaction هستیم (در `transaction.atomic()`) و یک Exception رخ می‌دهد که نباید باعث Rollback Transaction شود، از `set_rollback()` استفاده می‌کنیم. مثلاً در یک Custom Exception Handler اگر خود Handler خطا بدهد، با `set_rollback()` از فسخ Transaction جلوگیری می‌کنیم:
   ```python
   from django.db.transaction import set_rollback
   from rest_framework.exceptions import APIException

   if response is None and isinstance(exc, APIException):
       set_rollback()
   ```
   این اطمینان می‌دهد که Transaction درست مدیریت می‌شود.

7. **تمایز بین Debug Mode و Production Mode**  
   در `settings.py`، متغیر `DEBUG` را مدیریت می‌کنیم. اگر `DEBUG=True`، جزئیات خطا (مثل traceback) را به پاسخ اضافه می‌کنیم. در `custom_exception_handler` با `settings.DEBUG` چک می‌کنیم که آیا خطا باید جزئیات فنی داشته باشد یا فقط یک پیام عمومی برگرداند.

8. **استفاده از کدهای وضعیت HTTP مناسب**  
   برای هر سناریو کد وضعیت مناسب را انتخاب می‌کنیم: `400 Bad Request` برای ورودی نامعتبر، `401 Unauthorized` برای احراز هویت نشده، `403 Forbidden` برای دسترسی ممنوع، `404 NotFound` برای منبع ناموجود، `409 Conflict` برای تداخل داده (مثلاً ایزبن تکراری)، `429 Too Many Requests` برای محدودیت نرخ. هر کدام را در یک ویو تست می‌کنیم.

9. **ساختار پاسخ خطا برای کلاینت**  
   در `custom_exception_handler` پاسخ خطا را به این ساختار استاندارد تبدیل می‌کنیم:
   ```json
   {
       "error_code": "book_not_found",
       "message": "کتاب درخواست‌شده یافت نشد.",
       "status_code": 404,
       "timestamp": "2026-10-10T12:00:00Z"
   }
   ```
   اضافه کردن `timestamp` به کلاینت کمک می‌کند خطاها را لاگ و رفع اشکال کند.

10. **ثبت خطاها با Python Logging**  
    در `settings.py` logging را پیکربندی می‌کنیم:
    ```python
    LOGGING = {
        'version': 1,
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'logs/api_errors.log',
            },
        },
        'loggers': {
            'shop': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
    ```
    سپس در `custom_exception_handler` یک Logger می‌گیریم و متن کامل خطا (شامل traceback) را در فایل لاگ ثبت می‌کنیم.

11. **تست Exception Handler با APIClient**  
    یک تست می‌نویسیم که یک کتاب ناموجود را درخواست کند و بررسی کند که پاسخ دارای کلیدهای `error_code`، `message` و `status_code` است. همچنین بررسی می‌کنیم که کد وضعیت ۴۰۴ باشد. تست دوم: کتابی با قیمت منفی ارسال کنیم و خطای ۴۰۰ دریافت کنیم.

12. **رفتار مناسب برای خطاهای ۵۰۰ (Internal Server Error)**  
    در Production Mode، خطاهای ۵۰۰ نباید جزئیات فنی (مثل traceback) داشته باشند. یک سناریو خطای ۵۰۰ را شبیه‌سازی می‌کنیم (مثلاً با تقسیم بر صفر در ویو) و بررسی می‌کنیم که پاسخ فقط یک پیام عمومی مثل «خطای داخلی سرور» برگرداند، بدون نشان دادن جزئیات کد. در عین حال، لاگ کامل خطا در فایل نوشته می‌شود.

13. **Exception Handling در سطح View (Local vs Global)**  
    گاهی لازم است Exceptionها را در سطح خود ویو مدیریت کنیم، نه به صورت global. یک ویو می‌سازیم که `try/except` داخلی دارد و خطای `IntegrityError` دیتابیس (مثلاً مقدار تکراری) را به `ValidationError` تبدیل می‌کند تا Handler جهانی آن را به‌درستی برگرداند. این روش برای خطاهای خاص ویو مفید است.

14. **ساخت یک Exception برای محدودیت نرخ سفارش**  
    یک Exception سفارشی به نام `OrderLimitExceeded` با `status_code=429` و `default_code='order_limit_exceeded'` می‌سازیم. در ویو ثبت سفارش، بررسی می‌کنیم که کاربر در یک ساعت بیش از حد مجاز سفارش نداده باشد. اگر داده باشد، این Exception را raise می‌کنیم و پاسخ مناسب (با هدر `Retry-After`) به کلاینت برمی‌گردد.

15. **اضافه کردن `custom_exception_handler` به `REST_FRAMEWORK` و تست زنجیره‌ای**  
    در یک تست جامع، چندین نوع خطای مختلف را بررسی می‌کنیم: ۴۰۴ برای منبع ناموجود، ۴۰۰ برای داده نامعتبر، ۴۰۳ برای دسترسی غیرمجاز و ۴۰۱ برای توکن منقضی. بررسی می‌کنیم که همه پاسخ‌ها از یک ساختار استاندارد پیروی می‌کنند و کد وضعیت HTTP درست است.