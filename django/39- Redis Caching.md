## سرفصل: Redis Caching

### منابع آموزشی

**مستندات رسمی django-redis:**
- [django-redis Documentation — راهنمای کامل پیکربندی، استفاده و راه‌اندازی Redis به‌عنوان Cache در Django](https://django-redis.readthedocs.io/en/latest/)

**مستندات رسمی Django:**
- [Django Cache Framework — مرجع کامل سیستم کش Django، دکوراتورها و API پایین‌سطح](https://django.readthedocs.io/en/5.2.x/topics/cache.html)
- [The per-view cache — دکوراتورهای cache_page و cache_control](https://django.readthedocs.io/en/5.2.x/topics/cache.html#the-per-view-cache)

**مستندات رسمی DRF:**
- [Rendering and Caching در DRF — کش کردن پاسخ‌های API](https://www.django-rest-framework.org/api-guide/renderers/#caching)

---
### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. می‌خواهیم با Redis پاسخ‌های API و کوئری‌های پرتکرار دیتابیس را کش کنیم تا سرعت پاسخ‌دهی بالا برود و فشار روی دیتابیس کم شود. همچنین کش را هنگام تغییر داده‌ها به‌صورت خودکار بی‌اعتبار (invalidate) می‌کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **نصب و راه‌اندازی Redis**  
   ابتدا Redis را نصب می‌کنیم: `sudo apt install redis-server`. سپس با `redis-cli ping` بررسی می‌کنیم که پاسخ `PONG` برگردد، یعنی سرور Redis در حال اجراست. این پیش‌نیاز همه تمرین‌های بعدی است.

2. **نصب `django-redis`**  
   با `pip install django-redis` بسته را نصب می‌کنیم. این بسته یک Backend آماده برای استفاده از Redis در سیستم کش Django فراهم می‌کند.

3. **پیکربندی `CACHES` در `settings.py`**  
   در `settings.py` تنظیمات کش را اضافه می‌کنیم:
   ```python
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/1",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           },
           "TIMEOUT": 300,
       }
   }
   ```
   عدد `1` در آدرس یعنی از دیتابیس شماره ۱ در Redis استفاده می‌کنیم که جدا از داده‌های دیگر Redis است. تنظیم `TIMEOUT` یعنی اگر هیچ اعتبار مدتی مشخص نشود، کلیدها بعد از ۳۰۰ ثانیه منقضی می‌شوند.

4. **استفاده از API پایین‌سطح کش (`cache.get` و `cache.set`)**  
   در یک ویو، نتیجه یک کوئری گران را کش می‌کنیم:
   ```python
   from django.core.cache import cache

   def book_list(request):
       books = cache.get('all_books')
       if books is None:
           books = list(Book.objects.select_related('author').all())
           cache.set('all_books', books, timeout=600)
       return render(request, 'books.html', {'books': books})
   ```
   دفعه اول داده از دیتابیس خوانده و در کش ذخیره می‌شود؛ دفعات بعد مستقیماً از Redis خوانده می‌شود.

5. **افزودن دکوراتور `cache_page` به یک ویوی DRF**  
   برای کش کردن پاسخ کامل یک `APIView` از دکوراتور `cache_page` استفاده می‌کنیم:
   ```python
   from django.views.decorators.cache import cache_page
   from django.utils.decorators import method_decorator

   @method_decorator(cache_page(60 * 15), name='get')
   class BookListView(ListAPIView):
       queryset = Book.objects.all()
       serializer_class = BookSerializer
   ```
   با این کار پاسخ GET این ویو به مدت ۱۵ دقیقه کش می‌شود. دکوراتور باید روی متد `get` قرار بگیرد، نه روی کلاس.

6. **استفاده از `cache_control` برای کنترل کش در سطح HTTP**  
   دکوراتور `cache_control` هدرهای `Cache-Control` را تنظیم می‌کند تا کلاینت و پروکسی‌ها بفهمند پاسخ چقدر معتبر است:
   ```python
   @cache_control(private=True, max_age=3600)
   def profile_view(request):
       ...
   ```
   با `no_cache=True` و `no_store=True` پاسخ را اصلاً قابل کش نمی‌کنیم، مثلاً برای داده‌های حساس.

7. **تعریف Key Prefix برای هر اپلکیشن**  
   برای جلوگیری از تداخل کلیدهای کش بین اپلیکیشن‌های مختلف، از `KEY_PREFIX` استفاده می‌کنیم:
   ```python
   CACHES['default']['KEY_PREFIX'] = 'shop_v1'
   ```
   همه کلیدها با پیشوند `shop_v1:` ساخته می‌شوند. این کار در Deploy نتیجه می‌دهد: وقتی نسخه جدید اپلیکیشن منتشر می‌شود، تغییر `KEY_PREFIX` همه کش قبلی را یکجا بی‌اعتبار می‌کند.

8. **بکاپ گرفتن آمار کلیدهای کش با `keys` و `ttl`**  
   با `redis-cli --scan --pattern "shop_v1*"` همه کلیدهای کش اپلیکیشن را لیست می‌کنیم. با `redis-cli TTL shop_v1:all_books` زمان باقی‌مانده انقضای یک کلید را می‌بینیم. این ابزارها برای دیباگ و مانیتورینگ کش مفید هستند.

9. **بی‌اعتبارسازی کش با `cache.delete()` و `cache.clear()`**  
   بعد از به‌روزرسانی یک کتاب، کش‌های مربوط به آن را حذف می‌کنیم:
   ```python
   cache.delete(f'book_detail_{book.pk}')
   cache.delete('all_books')
   ```
   و اگر لازم است همه کش را خالی کنیم (مثلاً بعد از bulk update): `cache.clear()`. توجه می‌کنیم که `cache.clear()` همه دیتابیس جاری Redis را خالی می‌کند، پس استفاده از یک دیتابیس جداگانه برای کش مهم است.

10. **اتصال بی‌اعتبارسازی کش به `post_save` و `post_delete` Signal**  
    هنگام تغییر یا حذف یک `Book`، کش باید خودکار بی‌اعتبار شود. در `signals.py` یک Receiver روی `post_save` و `post_delete` مدل `Book` می‌سازیم که کلیدهای کش `all_books` و `book_detail_{id}` را حذف کند. به این ترتیب هر تغییری فوراً در سایت دیده می‌شود و کاربران داده قدیمی (stale) نمی‌بینند.

11. **کش کردن پاسخ Serializer با `cache_page` و پارامترهای درخواست**  
    مشکل `cache_page` این است که کوئری‌استرینگ‌های متفاوت (مثل صفحه‌بندی `?page=2`) کلیدهای متفاوتی می‌سازند. یک ویو می‌سازیم که لیست کتاب‌ها را با صفحه‌بندی و فیلتر کش کند. برای این کار، کلید کش را با خود کوئری‌استرینگ می‌سازیم: `f"books:{request.GET.urlencode()}"`. این روش باعث می‌شود هر ترکیب فیلتر جداگانه کش شود.

12. **کش کردن QuerySet با استفاده از `cache.get_or_set`**  
    متد `get_or_set` هم خواندن و هم نوشتن را در یک خط انجام می‌دهد:
    ```python
    featured_books = cache.get_or_set(
        'featured_books',
        Book.objects.filter(is_featured=True).select_related('author'),
        timeout=600
    )
    ```
    اگر کلید وجود داشته باشد مقدار کش برمی‌گردد، وگرنه تابع را اجرا و نتیجه را کش می‌کند.

13. **استفاده از `Sample` انواع کش در DRF با `CacheResponseMixin`**  
    همراه با `django-cachalot` و یا به صورت دستی، می‌توانیم کش را به `GenericViewSet`ها اضافه کنیم. نمون ه ساده: یک `ListAPIView` با `@method_decorator(cache_page(...))`. برای Apiهایی با احراز هویت، کش باید با `vary_on_headers('Authorization')` همراه باشد تا پاسخ یک کاربر برای کاربر دیگر فرستاده نشود.

14. **اندازه‌گیری بهبود کارایی قبل و بعد از کش**  
    با `django-debug-toolbar` یا ابزار `time.perf_counter()` در ویو، زمان اجرای یک درخواست را قبل از کش و بعد از کش اندازه می‌گیریم. در `dbshell` با `EXPLAIN ANALYZE` یا در لاگ‌های Slow Query، تعداد کوئری‌های دیتابیس را قبل و بعد مقایسه می‌کنیم. نتیجه را گزارش می‌کنیم: معمولاً زمان پاسخ از چند صد میلی‌ثانیه به چند میلی‌ثانیه کاهش پیدا می‌کند.

15. **مدیریت `Vary` هدرها و کش پاسخ‌های شخصی‌سازی‌شده**  
    اگر پاسخ به Cookie یا هدر زبان وابسته است، باید از `@vary_on_headers('Accept-Language')` استفاده کنیم. یک ویو می‌سازیم که لیست کتاب‌ها را بر اساس زبان کاربر برمی‌گرداند و با `vary_on_headers` مطمئن می‌شویم پاسخ هر زبان جداگانه کش می‌شود. این از اشتباه بزرگ «دادن داده کش‌شده زبان A به کاربر زبان B» جلوگیری می‌کند.