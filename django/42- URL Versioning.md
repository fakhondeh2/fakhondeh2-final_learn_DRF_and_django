## سرفصل: URL Versioning

### منابع آموزشی

**مستندات رسمی DRF:**
- [Versioning — مرجع کامل سیستم Versioning در DRF شامل URLPathVersioning و سایر اسکیم‌ها](https://www.django-rest-framework.org/api-guide/versioning/)
- [URLPathVersioning — جزئیات استفاده از مسیر URL برای ورژن‌بندی API](https://www.django-rest-framework.org/api-guide/versioning/#urlpathversioning)

**مستندات رسمی Django:**
- [URL dispatcher — نحوه تعریف مسیرهای URL شامل عبارات منظم و نام‌گذاری مسیرها](https://django.readthedocs.io/en/5.2.x/topics/http/urls.html)

---
### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. API آن در حال رشد است و باید از چند نسخه پشتیبانی کند. می‌خواهیم با استفاده از `URLPathVersioning` مسیر `/api/v1/books/` و `/api/v2/books/` را پیاده‌سازی کنیم تا بتوانیم تغییرات breaking را بدون اختلال در کلاینت‌های قدیمی اعمال کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت URLPathVersioning و مزایای آن**  
   در `URLPathVersioning`، نسخه API مستقیماً در مسیر URL قرار می‌گیرد، مثلاً `/api/v1/books/`. DRF مقدار `v1` را از URL استخراج می‌کند و از طریق `request.version` در دسترس قرار می‌دهد. مزیت این روش: واضح و قابل پیش‌بینی است، کش کردن بر اساس URL متفاوت به‌صورت خودکار انجام می‌شود. عیب: URLها طولانی‌تر می‌شوند.

2. **پیکربندی `DEFAULT_VERSIONING_CLASS` در `settings.py`**  
   در تنظیمات `REST_FRAMEWORK`، کلاس ورژن‌بندی پیش‌فرض را تنظیم می‌کنیم:
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
       'DEFAULT_VERSION': 'v1',
       'ALLOWED_VERSIONS': ['v1', 'v2'],
       'VERSION_PARAM': 'version',
   }
   ```
   `DEFAULT_VERSION` نسخه پیش‌فرض است، `ALLOWED_VERSIONS` نسخه‌های مجاز را محدود می‌کند و `VERSION_PARAM` نام پارامتر در URL است.

3. **تعریف مسیرهای URL با پارامتر `version`**  
   در `shop/urls.py`، مسیرهای API را با پارامتر `version` تعریف می‌کنیم:
   ```python
   from django.urls import path, include

   urlpatterns = [
       path('api/<version>/books/', include('shop.api_urls')),
   ]
   ```
   حالا همه مسیرهای داخل `shop/api_urls.py` تحت `/api/v1/books/` یا `/api/v2/books/` در دسترس هستند. DRF خودکار مقدار `version` را از URL می‌خواند.

4. **تفکیک Serializerها بر اساس نسخه**  
   برای v1 و v2 Serializerهای متفاوت می‌سازیم. مثلاً در v1، فیلد `price` را با نام `cost` برمی‌گردانیم، اما در v2 از نام `price` استفاده می‌کنیم. یک ویو می‌نویسیم که بر اساس `request.version` Serializer متفاوتی انتخاب کند:
   ```python
   class BookListView(ListAPIView):
       queryset = Book.objects.all()

       def get_serializer_class(self):
           if self.request.version == 'v2':
               return BookV2Serializer
           return BookV1Serializer
   ```
   این روش امکان تغییر تدریجی Serializerها را می‌دهد.

5. **تفکیک Viewها بر اساس نسخه**  
   برای تغییرات بزرگ‌تر، Viewهای جداگانه برای هر نسخه می‌سازیم. مثلاً در v1 فقط کتاب‌های موجود برمی‌گردند، در v2 کتاب‌های موجود و ناموجود:
   ```python
   class BookV1ListView(ListAPIView):
       queryset = Book.objects.filter(is_available=True)
       serializer_class = BookV1Serializer

   class BookV2ListView(ListAPIView):
       queryset = Book.objects.all()
       serializer_class = BookV2Serializer
   ```
   سپس هر کدام را به `version` مربوطه متصل می‌کنیم.

6. **استفاده از `request.version` در View برای منطق شرطی**  
   در یک View واحد، با بررسی `request.version` رفتار متفاوت داریم:
   ```python
   def get(self, request, *args, **kwargs):
       if request.version == 'v1':
           return self._handle_v1()
       elif request.version == 'v2':
           return self._handle_v2()
   ```
   این روش برای تغییرات کوچک مناسب است، اما View را پیچیده می‌کند. برای تغییرات بزرگ بهتر است Viewهای جداگانه داشته باشیم.

7. **بررسی نسخه در `get_serializer_class` با پارامتر version**  
   یک الگوی تمیزتر: نگاشت نسخه به Serializer را در یک دیکشنری ذخیره می‌کنیم:
   ```python
   VERSION_SERIALIZER_MAP = {
       'v1': BookV1Serializer,
       'v2': BookV2Serializer,
   }

   def get_serializer_class(self):
       return VERSION_SERIALIZER_MAP.get(
           self.request.version, BookV1Serializer
       )
   ```
   با اضافه شدن نسخه جدید، فقط یک خط اضافه می‌کنیم.

8. **تست نسخه‌های مختلف API با APIClient**  
   یک تست می‌نویسیم که دو درخواست به مسیرهای `/api/v1/books/` و `/api/v2/books/` ارسال کند و بررسی کند که:
   - پاسخ هر دو ۲۰۰ است
   - ساختار داده v1 با v2 متفاوت است (مثلاً v1 فیلد `cost` دارد، v2 فیلد `price` دارد)
   - `request.version` در View مقدار صحیح دارد

9. **مدیریت نسخه‌های قدیمی (Deprecation)**  
   وقتی یک نسخه قدیمی می‌شود، باید آن را Deprecate کنیم. در View مربوطه، هدر `Warning` یا `Sunset` به پاسخ اضافه می‌کنیم:
   ```python
   class BookV1ListView(ListAPIView):
       queryset = Book.objects.filter(is_available=True)
       serializer_class = BookV1Serializer

       def finalize_response(self, request, response, *args, **kwargs):
           response = super().finalize_response(request, response, *args, **kwargs)
           response['Warning'] = '299 - "API v1 is deprecated. Use v2."'
           return response
   ```
   این هدر به کلاینت‌ها اعلام می‌کند که نسخه قدیمی به‌زودی حذف می‌شود.

10. **محدود کردن نسخه‌های مجاز با `ALLOWED_VERSIONS`**  
    با `ALLOWED_VERSIONS = ['v1', 'v2']`، اگر کلاینتی به `/api/v3/books/` درخواست بدهد، DRF به‌طور خودکار خطای `404 Not Found` یا `406 Not Acceptable` برمی‌گرداند. این تنظیم از دسترسی به نسخه‌های منتشرنشده جلوگیری می‌کند.

11. **نگهداری هم‌زمان دو نسخه و Observable Migration**  
    برای مدتی هر دو نسخه v1 و v2 در دسترس هستند. یک صفحه وضعیت (status page) می‌سازیم که نشان دهد نسخه v1 چه زمانی Deprecate می‌شود. یک middleware می‌نویسیم که کاربران را از نسخه قدیمی به جدید راهنمایی کند: اگر کلاینتی به v1 وصل شد، مقدار header `X-API-Version-Suggestion: v2` را برگردانیم.

12. **پیاده‌سازی Rate Limiting جداگانه برای هر نسخه**  
    تنظیمات `DEFAULT_THROTTLE_RATES` را بر اساس نسخه متفاوت می‌کنیم. یک throttle کلاس سفارشی می‌سازیم که `request.version` را بررسی کند. مثلاً v1 با نرخ ۱۰۰ درخواست در ساعت و v2 با نرخ ۱۰۰۰ درخواست در ساعت محدود شود. این کار تشویق به مهاجرت به نسخه جدید است.

13. **تأثیر URL Versioning بر Caching**  
    از آنجایی که URL v1 و v2 متفاوت است، کش (مثلاً با `cache_page`) به‌صورت خودکار آن‌ها را جدا می‌کند. این یکی از مزایای URL Versioning است. در `redis-cli` بررسی می‌کنیم که کلیدهای کش با `v1` و `v2` پیشوند متفاوت دارند و با هم تداخل نمی‌کنند.

14. **API Gateway و URL Rewriting**  
    اگر API Gateway (مثل Nginx یا Kong) داریم، می‌توانیم مسیرهای `/api/v1/*` را به Backend قدیمی و `/api/v2/*` را به Backend جدید هدایت کنیم. تنظیمات Nginx را مثال می‌زنیم:
    ```nginx
    location /api/v1/ {
        proxy_pass http://old-backend:8000/;
    }
    location /api/v2/ {
        proxy_pass http://new-backend:8000/;
    }
    ```
    این کار امکان Deploy مستقل دو نسخه را فراهم می‌کند.

15. **بررسی Reverse Proxy و Versioning**  
    اگر از Nginx معکوس استفاده کنیم، باید مطمئن شویم که `SCRIPT_NAME` یا `FORCE_SCRIPT_NAME` به‌درستی تنظیم شده است تا Django مسیرها را درست تشخیص بدهد. یک middleware بنچمارک می‌نویسیم که `request.path` و `request.version` را لاگ کند تا تأیید کنیم مقدار `version` از URL درست استخراج می‌شود.