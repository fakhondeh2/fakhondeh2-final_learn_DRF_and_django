## سرفصل: File Uploads

### منابع آموزشی

**مستندات رسمی Django REST Framework:**
- [Parsers — راهنمای کامل پارسرها، شامل FileUploadParser و MultiPartParser](https://www.django-rest-framework.org/api-guide/parsers/)

**مستندات رسمی Django:**
- [File Uploads — راهنمای آپلود فایل در Django، ذخیره‌سازی و سرو فایل‌ها](https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/)
- [File Storage — مستندات کامل Storage backendها](https://docs.djangoproject.com/en/5.2/topics/files/)
- [Managing Static Files (Media) — نحوه سرو فایل‌های مدیا در توسعه و تولید](https://docs.djangoproject.com/en/5.2/howto/static-files/)

**کتابخانه‌های مرتبط:**
- [Pillow – پردازش تصویر در پایتون](https://pillow.readthedocs.io/en/stable/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. می‌خواهیم به مدل `Book` امکان آپلود تصویر جلد کتاب (cover image) اضافه کنیم. همچنین می‌خواهیم یک API برای آپلود فایل‌های عمومی (مثلاً فایل PDF نمونه کتاب) بسازیم. کاربران می‌توانند از طریق API تصویر جلد را آپلود کنند و سیستم اندازه و نوع فایل را اعتبارسنجی کند.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت پارسرهای آپلود فایل در DRF**  
   DRF دو پارسر اصلی برای آپلود فایل دارد: `MultiPartParser` که داده‌های فرم را همراه با فایل دریافت می‌کند (رایج‌ترین روش)، و `FileUploadParser` که فقط فایل خام را با هدر `Content-Type: application/octet-stream` یا `Content-Type: image/*` دریافت می‌کند. در بیشتر موارد از `MultiPartParser` استفاده می‌کنیم.

2. **تنظیمات Media Files در Django**  
   در فایل `settings.py` دو متغیر مهم تنظیم می‌کنیم: `MEDIA_URL` (مسیر URL برای دسترسی به فایل‌ها) و `MEDIA_ROOT` (مسیر مطلق در دیسک که فایل‌ها در آن ذخیره می‌شوند). مقدار `MEDIA_ROOT` را به `BASE_DIR / 'media'` و `MEDIA_URL` را به `'/media/'` تنظیم می‌کنیم.

3. **افزودن فیلد `cover_image` به مدل `Book`**  
   یک فیلد از نوع `ImageField` به مدل `Book` اضافه می‌کنیم: `cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)`. پارامتر `upload_to` مشخص می‌کند فایل در کدام زیرشاخه از `MEDIA_ROOT` ذخیره شود. سپس `makemigrations` و `migrate` را اجرا می‌کنیم.

4. **نصب Pillow برای پردازش تصویر**  
   Django برای `ImageField` به کتابخانه Pillow نیاز دارد. با `pip install Pillow` آن را نصب می‌کنیم. Pillow امکان تغییر اندازه، برش، چرخش و فشرده‌سازی تصاویر را فراهم می‌کند. نصب بودن Pillow را با `pip show Pillow` بررسی می‌کنیم.

5. **ساخت Serializer برای آپلود فایل**  
   یک `BookSerializer` می‌سازیم که فیلد `cover_image` از نوع `ImageField` (سریالایزر) دارد. این فیلد در DRF به‌صورت `ImageField` در سریالایزر تعریف می‌شود. پارسر ویو را به `MultiPartParser` تنظیم می‌کنیم تا بتواند فایل را از `request.data` بخواند.

6. **ساخت View با MultiPartParser**  
   یک `APIView` یا `ModelViewSet` برای `Book` می‌سازیم و در آن `parser_classes = [MultiPartParser, FormParser]` را تنظیم می‌کنیم. `FormParser` هم اضافه می‌شود تا داده‌های متنی فرم (مانند title و price) نیز پردازش شوند. حالا کلاینت می‌تواند در یک درخواست POST هم داده‌های کتاب و هم تصویر جلد را ارسال کند.

7. **اعتبارسنجی نوع فایل (File Extension Validation)**  
   در سریالایزر یک متد `validate_cover_image` اضافه می‌کنیم که نوع فایل آپلودی را بررسی کند. فقط پسوندهای مجاز مثل `.jpg`، `.jpeg`، `.png` و `.gif` را قبول می‌کنیم. از متد `os.path.splitext` برای استخراج پسوند استفاده می‌کنیم و اگر پسوند مجاز نباشد، `serializers.ValidationError` صادر می‌کنیم.

8. **اعتبارسنجی اندازه فایل**  
   در همان متد `validate_cover_image`، اندازه فایل را با `file.size` بررسی می‌کنیم. یک محدودیت مثلاً ۵ مگابایت (۵ × ۱۰۲۴ × ۱۰۲۴ بایت) قرار می‌دهیم. اگر فایل بزرگ‌تر بود، خطای ValidationError با پیام «حجم فایل نباید بیشتر از ۵ مگابایت باشد» برمی‌گردانیم.

9. **تغییر اندازه تصویر با Pillow در هنگام ذخیره**  
   متد `create` و `update` سریالایزر را override می‌کنیم تا بعد از ذخیره فایل، با Pillow تصویر را به ابعاد استاندارد (مثلاً حداکثر عرض ۸۰۰ پیکسل) تغییر دهیم. از `Image.open(file)` و متد `thumbnail` برای تغییر اندازه استفاده می‌کنیم و تصویر تغییر اندازه‌یافته را دوباره ذخیره می‌کنیم.

10. **سرو کردن Media Files در توسعه**  
    در فایل `mysite/urls.py` یک مسیر برای سرو فایل‌های مدیا در حالت DEBUG اضافه می‌کنیم:
    ```python
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```
    این کار فقط برای محیط توسعه مناسب است. در تولید از Nginx یا CDN استفاده می‌شود.

11. **تست آپلود با curl**  
    با دستور curl آپلود را تست می‌کنیم:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/books/ \
      -F "title=کتاب تست" \
      -F "price=120000" \
      -F "cover_image=@/path/to/image.jpg"
    ```
    بررسی می‌کنیم که پاسخ شامل لینک تصویر آپلودی باشد و فایل در پوشه `media/book_covers/` ذخیره شده باشد.

12. **تست آپلود با فرمت JSON (بدون فایل)**  
    یک درخواست POST با `Content-Type: application/json` و بدون فایل می‌فرستیم. مطمئن می‌شویم که فیلد `cover_image` اختیاری است (`null=True, blank=True`) و خطایی برگردانده نمی‌شود.

13. **مدیریت خطاهای آپلود**  
    سناریوهای خطا را تست می‌کنیم: ارسال فایل با پسوند نامعتبر (مثلاً فایل `.exe`)، ارسال فایل بزرگ‌تر از حد مجاز، ارسال درخواست بدون `Content-Type` مناسب. بررسی می‌کنیم که پاسخ خطای مناسب (۴۰۰ یا ۴۱۵) با پیام فارسی برگردانده شود.

14. **ایجاد یک Endpoint اختصاصی برای آپلود فایل**  
    یک `APIView` جداگانه به نام `BookCoverUploadView` می‌سازیم که فقط فایل تصویر را دریافت کند (بدون داده‌های دیگر کتاب). از `FileUploadParser` استفاده می‌کنیم. این ویو برای سناریوهایی مفید است که کتاب از قبل وجود دارد و فقط می‌خواهیم تصویر جلد آن را آپلود کنیم.

15. **آشنایی با Storage Backendهای ابری**  
    در `settings.py` متغیر `DEFAULT_FILE_STORAGE` تعیین می‌کند فایل‌ها کجا ذخیره شوند. پیش‌فرض `FileSystemStorage` است که فایل‌ها را روی دیسک محلی ذخیره می‌کند. در تولید معمولاً از بکندهای ابری مثل `storages.backends.s3boto3.S3Boto3Storage` (AWS S3) یا `storages.backends.gcloud.GoogleCloudStorage` (Google Cloud) استفاده می‌شود. نصب `django-storages` و پیکربندی آن را بررسی می‌کنیم.