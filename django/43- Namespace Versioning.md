## سرفصل: Namespace Versioning

### منابع آموزشی

**مستندات رسمی DRF:**
- [Versioning — مرجع کامل سیستم Versioning در DRF شامل NamespaceVersioning و AcceptHeaderVersioning](https://www.django-rest-framework.org/api-guide/versioning/)
- [NamespaceVersioning — جزئیات استفاده از فضای نام URL برای ورژن‌بندی API](https://www.django-rest-framework.org/api-guide/versioning/#namespaceversioning)
- [AcceptHeaderVersioning — مذاکره نسخه از طریق هدر Accept](https://www.django-rest-framework.org/api-guide/versioning/#acceptheaderversioning)

**مستندات رسمی Django:**
- [URL namespaces — نحوه تعریف فضای نام URL در Django](https://django.readthedocs.io/en/5.2.x/topics/http/urls.html#url-namespaces)

---
### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. می‌خواهیم با `NamespaceVersioning` چند نسخه از API را هم‌زمان مدیریت کنیم و برای کلاینتی که نمی‌خواهد نسخه در URL باشد، از `AcceptHeaderVersioning` (مذاکره با هدر Accept) پشتیبانی کنیم. اپلیکیشن‌های مجزای `api_v1` و `api_v2` می‌سازیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت NamespaceVersioning و تفاوت آن با URLPathVersioning**  
   در `URLPathVersioning`، نسخه در مسیر URL است (مثل `/api/v1/books/`). اما در `NamespaceVersioning`، نسخه از طریق فضای نام (namespace) URL شناسایی می‌شود، مثل `api:v1:books`. Django با `reverse('api:v1:books-list')` آن را می‌شناسد. تفاوت اصلی: NamespaceVersioning فقط با `reverse()` و درخواست‌های داخلی کار می‌کند و قابل استفاده‌تر است.

2. **پیکربندی `NamespaceVersioning` در `settings.py`**  
   در تنظیمات `REST_FRAMEWORK`:
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
       'DEFAULT_VERSION': 'v1',
       'ALLOWED_VERSIONS': ['v1', 'v2'],
   }
   ```
   با این تنظیم، DRF دنبال namespace ای می‌گردد که به نسخه وصل شده باشد.

3. **ساخت دو اپ مجزا برای v1 و v2**  
   دو اپ جدید می‌سازیم: `python manage.py startapp api_v1` و `python manage.py startapp api_v2`. هر اپ `serializers.py`، `views.py` و `urls.py` مخصوص خودش را دارد. این جداسازی فیزیکی باعث می‌شود توسعه دو نسخه به‌صورت موازی بدون تداخل انجام شود.

4. **ایجاد View و Serializer برای هر نسخه**  
   در `api_v1/views.py`، `BookV1ListView` را می‌سازیم که فقط کتاب‌های موجود را برمی‌گرداند. در `api_v2/views.py`، `BookV2ListView` را می‌سازیم که همه کتاب‌ها را با فیلدهای جدید برمی‌گرداند. هر کدام Serializer مخصوص خود را دارند. این تفکیک View و Serializer مدیریت تغییرات breaking را آسان می‌کند.

5. **تعریف URL با namespace در هر اپ**  
   در `api_v1/urls.py`:
   ```python
   app_name = 'v1'
   urlpatterns = [
       path('books/', BookV1ListView.as_view(), name='books-list'),
   ]
   ```
   در `api_v2/urls.py` هم مشابه `app_name = 'v2'`. سپس در `shop/urls.py` هر دو را با `include` به دامنه اصلی وصل می‌کنیم.

6. **تعریف مسیرهای اصلی با `include` و namespace های تو در تو**  
   در `shop/urls.py`:
   ```python
   urlpatterns = [
       path('api/v1/', include(('api_v1.urls', 'api_v1'), namespace='api_v1')),
       path('api/v2/', include(('api_v2.urls', 'api_v2'), namespace='api_v2')),
   ]
   ```
   برای اینکه NamespaceVersioning کار کند، namespace باید به نسخه اشاره داشته باشد. DRF با بررسی `namespace` همه URLها، نسخه موردنظر را پیدا می‌کند.

7. **استفاده از `reverse()` با namespace در ویو**  
   در یک View، برای ساخت لینک به لیست کتاب‌های v2 از `reverse('api_v2:books-list')` استفاده می‌کنیم. این روش از ثابت نگه داشتن رشته URLs جلوگیری می‌کند و اگر مسیر تغییر کند، همه لینک‌ها خودکار اصلاح می‌شوند. در shell این را امتحان می‌کنیم: `reverse('api_v2:books-list')` → `/api/v2/books/`.

8. **ترکیب NamespaceVersioning با Router (DefaultRouter)**  
   در هر اپ یک `DefaultRouter` می‌سازیم:
   ```python
   from rest_framework.routers import DefaultRouter

   router = DefaultRouter()
   router.register('books', BookViewSet, basename='books')
   urlpatterns = router.urls
   ```
   Router به‌صورت خودکار اکشن‌های CRUD و `urlpatterns` را می‌سازد. با namespace تو در تو (`api_v1:books-list`) همه مسیرهای Router نسخه‌بندی می‌شوند.

9. **استفاده از `request.version` در ViewSet برای نسخه خاص**  
   در یک ViewSet مشترک (که در هر دو اپ استفاده می‌شود)، متدها را بر اساس `request.version` تنظیم می‌کنیم:
   ```python
   class BookViewSet(viewsets.ModelViewSet):
       def get_serializer_class(self):
           if self.request.version == 'v2':
               return BookV2Serializer
           return BookV1Serializer

       def get_queryset(self):
           if self.request.version == 'v2':
               return Book.objects.all()
           return Book.objects.filter(is_available=True)
   ```
   با این روش، یک کلاس واحد می‌تواند در namespace های دو نسخه کار کند.

10. **مدیریت هم‌زمان چند نسخه (Multi-version) و استراتژی مهاجرت**  
    هر دو نسخه هم‌زمان فعال هستند. برای مهاجرت تدریجی، در v1 فقط تغییرات جزئی اعمال می‌کنیم و کلاینت‌ها را تشویق می‌کنیم به v2 بروند. با یک صفحه داشبورد یا اسکریپت، تعداد درخواست‌های v1 و v2 را شمارش می‌کنیم تا بفهمیم چه زمانی کلاینت‌های v1 به صفر رسیده‌اند و می‌توان v1 را حذف کرد. این مهاجرت تدریجی در برابر مهاجرت breaking (حذف ناگهانی v1) مقایسه می‌شود.

11. **استفاده از AcceptHeaderVersioning برای مذاکره نسخه با هدر**  
    برای کلاینتی که نمی‌خواهد نسخه در URL باشد، از `AcceptHeaderVersioning` استفاده می‌کنیم:
    ```python
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning'
    ```
    کلاینت نسخه را با هدر `Accept` اعلام می‌کند:
    ```
    GET /api/books/ HTTP/1.1
    Accept: application/json; version=v2
    ```
    اگر `Accept` نسخه‌ای تعیین نکند، `DEFAULT_VERSION` (v1) استفاده می‌شود. این روش مناسب کلاینت‌هایی است که URL ثابت دارند (مثل موبایل).

12. **تست نسخه‌های متفاوت و مقایسه پاسخ‌ها**  
    تست می‌نویسیم:
    ```python
    def test_namespace_versioning(self):
        response_v1 = self.client.get('/api/v1/books/')
        response_v2 = self.client.get('/api/v2/books/')
        self.assertEqual(response_v1.status_code, 200)
        self.assertEqual(response_v2.status_code, 200)
        # ساختار v1 و v2 متفاوت است
        self.assertIn('cost', response_v1.data[0])
        self.assertIn('price', response_v2.data[0])
    ```
    و برای AcceptHeaderVersioning:
    ```python
    def test_accept_header_versioning(self):
        response = self.client.get(
            '/api/books/',
            HTTP_ACCEPT='application/json; version=v2'
        )
        self.assertEqual(response.data[0]['price'], ...)
    ```

13. **مستندسازی تفاوت نسخه‌ها با drf-spectacular یا دستی**  
    مستندات نسخه‌های مختلف را جدا نگه می‌داریم. اگر از `drf-spectacular` استفاده می‌کنیم، `VERSION` کلاس‌های شکوه یا Schema را برای هر نسخه تنظیم می‌کنیم. یا به‌صورت دستی یک سند تغییرات (Changelog) می‌نویسیم که چه فیلدهایی در v2 اضافه یا تغییر کرده است. یک نقطه پایانی `/api/v2/docs/` برای مستندات تعاملی می‌سازیم.

14. **مدیریت Deprecated در Namespace Versioning**  
    برای نسخه Deprecated (مثل v1)، در ViewSet هدر `Sunset` اضافه می‌کنیم که تاریخ حذف نسخه را به کلاینت می‌گوید:
    ```python
    response['Sunset'] = 'Sat, 31 Dec 2026 23:59:59 GMT'
    ```
    و `Deprecation` را به متن پاسخ اضافه می‌کنیم. این اطلاعات به کلاینت کمک می‌کند به‌موقع مهاجرت کند.

15. **بررسی تداخل namespace ها و حل مشکلات common**  
    اگر namespace اشتباه پیکربندی شود، خطای `NoReverseMatch` یا خطای «version not found» رخ می‌دهد. برای دیباگ، در `custom_exception_handler` بررسی می‌کنیم که وقتی `request.version` قابل تشخیص نیست (`None` برگرداند)، خطای `404` مناسب ارسال شود. یک تست می‌نویسیم که namespace دیگری مثل `api_v3` در `urls.py` تعریف شده است اما در `ALLOWED_VERSIONS` نیست؛ بررسی می‌کنیم که DRF آن را با خطای مناسب رد کند.