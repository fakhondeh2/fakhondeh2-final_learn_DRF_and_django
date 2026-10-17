## سرفصل: فیلتر کردن داده‌ها (Filtering Data)

### منابع آموزشی

**مستندات رسمی Django REST Framework:**
- [Filtering — مرجع کامل فیلتر کردن: DjangoFilterBackend، SearchFilter، OrderingFilter و روش‌های سفارشی](https://www.django-rest-framework.org/api-guide/filtering/#filtering)
- [Generic Views — توضیح گزینه‌های `filter_backends`، `filterset_fields` و `search_fields` در ویوهای مبتنی بر کلاس](https://www.django-rest-framework.org/api-guide/generic-views/#generic-views)

**مستندات django-filter:**
- [django-filter – راهنمای یکپارچه‌سازی با DRF — نصب، تعریف FilterSet و تنظیم FilterBackend](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)
- [django-filter – مرجع فیلدها — انواع فیلد، lookup_expr و گزینه‌های هر فیلد](https://django-filter.readthedocs.io/en/stable/ref/filters.html)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. حالا می‌خواهیم به API این فروشگاه قابلیت فیلتر کردن اضافه کنیم: کاربر بتواند کتاب‌ها را بر اساس قیمت، تاریخ انتشار، نویسنده و برچسب فیلتر کند، روی عنوان و نام نویسنده جستجو کند و به‌صورت دلخواه نتایج را مرتب کند.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت مفهوم Filtering و نقش Filter Backend**  
   فیلتر کردن یعنی محدود کردن QuerySet بر اساس پارامترهای آدرس (query parameters) مثل `?price__gte=100`. در DRF این کار در لایه ویو و قبل از سریالایز کردن داده انجام می‌شود. ابزار اصلی فیلتر، «Filter Backend» است؛ DRF سه backend از پیش ساخته دارد: `SearchFilter` (جستجوی متنی)، `OrderingFilter` (مرتب‌سازی) و `DjangoFilterBackend` (فیلتر دقیق میدانی که از کتابخانه django-filter می‌آید).

2. **نصب django-filter**  
   با `pip install django-filter` بسته موردنیاز را نصب می‌کنیم. این کتابخانه ابزار قدرتمندی برای تعریف فیلترهای میدانی با لوکاپ‌های مختلف (دقیق، شامل، بزرگ‌تر از و...) فراهم می‌کند و به‌صورت رسمی توسط DRF پشتیبانی می‌شود.

3. **افزودن `django_filters` به `INSTALLED_APPS`**  
   در `settings.py` اپ `django_filters` را به `INSTALLED_APPS` اضافه می‌کنیم. بدون این مرحله، هنگام استفاده از `DjangoFilterBackend` با خطای «App 'django_filters' could not be found» مواجه می‌شویم.

4. **فعال‌سازی سراسری `DjangoFilterBackend`**  
   در دیکشنری `REST_FRAMEWORK` کلید `DEFAULT_FILTER_BACKENDS = ['django_filters.rest_framework.DjangoFilterBackend']` را اضافه می‌کنیم. حالا همه ViewSetها و ویوهای Generic به‌طور خودکار از فیلتر پشتیبانی می‌کنند. این روش برای وقتی مناسب است که همه APIها از یک الگوی فیلتر استفاده کنند.

5. **فیلتر کردن سریع و بدون تعریف کلاس با `filterset_fields`**  
   در `BookViewSet` یک کلاس `ListAPIView` با `queryset = Book.objects.all()`، با `filterset_fields = ['author', 'tags', 'published_date']` فیلترهای دقیق (exact) را فعال می‌کنیم. حالا آدرس `?author=1` فقط کتاب‌های نویسنده ۱ و `?tags=3` فقط کتاب‌های برچسب ۳ را برمی‌گرداند. این ساده‌ترین روش فیلتر است؛ Django به‌صورت خودکار برای هر فیلد یک فیلتر `exact` می‌سازد.

6. **تعریف کلاس صریح `BookFilter(FilterSet)`**  
   برای کنترل بیشتر، یک کلاس `BookFilter` تعریف می‌کنیم که از `django_filters.FilterSet` ارث‌بری می‌کند و با `Meta` مدل و فیلدها را مشخص می‌کند. سپس در ویو با `filterset_class = BookFilter` آن را وصل می‌کنیم. تفاوت این روش با `filterset_fields` این است که می‌توانیم برای هر فیلد لوکاپ دلخواه و اعتبارسنجی تعیین کنیم.

7. **یادگیری انواع لوکاپ فیلد (exact, contains, gt, lt)**  
   در کلاس `BookFilter` فیلد `title` را با `lookup_expr='icontains'` (شامل بدون حساسیت بزرگی حروف) و فیلد `price` را با `lookup_expr='gte'` (بزرگ‌تر از یا مساوی) تعریف می‌کنیم. لوکاپ‌های پرکاربرد شامل `exact`، `iexact`، `contains`، `icontains`، `startswith`، `gt`، `gte`، `lt`، `lte` و `in` هستند. با `field_name` می‌توان به فیلدهای رابطه هم دسترسی داشت؛ مثلاً `author__name` برای فیلتر بر اساس نام نویسنده.

8. **فیلتر محدوده قیمت با `RangeFilter`**  
   یک فیلد `price = filters.RangeFilter()` به `BookFilter` اضافه می‌کنیم. این فیلد به‌صورت خودکار دو پارامتر `?price_min=...` و `?price_max=...` می‌سازد و کتاب‌هایی را برمی‌گرداند که قیمتشان در این بازه باشد. برای تاریخ انتشار هم می‌توان از `DateFromToRangeFilter` استفاده کرد که دو پارامتر `published_date_after` و `published_date_before` فراهم می‌کند.

9. **ساخت فیلتر سفارشی با متد روی FilterSet**  
   برای فیلتری که با یک شرط ساده قابل بیان نیست، متد سفارشی روی `BookFilter` تعریف می‌کنیم. مثلاً یک `BooleanFilter` با نام `on_sale` تعریف و متد `filter_on_sale` را پیاده‌سازی می‌کنیم که کتاب‌های تخفیف‌دار را برگرداند: `self.queryset.filter(discount_price__isnull=False)`. با این تکنیک می‌توان فیلترهای پیچیده‌ای مثل «کتاب‌هایی که الامان چند نظر ۴ ستاره دارند» هم ساخت.

10. **جستجوی متنی در عنوان و نام نویسنده با `SearchFilter`**  
    `SearchFilter` را به `filter_backends` اضافه کرده و `search_fields = ['title', 'author__name', 'isbn']` تنظیم می‌کنیم. حالا `?search=هری` کتاب‌هایی که «هری» در عنوان یا نام نویسنده آن‌ها باشد را برمی‌گرداند. برای جستجوی دقیق‌تر می‌توان با پیشوند `^` (شروع با)، `=` (تطبیق کامل) و `@` (جستجوی تمام‌متن) رفتار هر فیلد را تنظیم کرد. رفتار `SearchFilter` به `CHAR_FIELD_LOOKUP` (پیش‌فرض `icontains`) بستگی دارد.

11. **مرتب‌سازی با `OrderingFilter`**  
    `OrderingFilter` را اضافه و `ordering_fields = ['price', 'published_date', 'title']` تنظیم می‌کنیم. حالا `?ordering=price` صعودی، `?ordering=-published_date` نزولی و `?ordering=price,-published_date` ترکیبی از هر دو را برمی‌گرداند. با `ordering = ['-published_date']` هم می‌توان ترتیب پیش‌فرض را مشخص کرد تا وقتی پارامتری داده نشود از آن استفاده شود.

12. **ترکیب همزمان سه Backend در یک ویو**  
    `filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]` را همراه با `filterset_class = BookFilter`، `search_fields` و `ordering_fields` در یک `BookListView` قرار می‌دهیم. حالا می‌توانیم همه را هم‌زمان ترکیب کنیم: `?author=1&price_min=100&price_max=500&search=هری&ordering=-price`. ترتیب اجرای backendها همان ترتیب ذکر در لیست است.

13. **جلوگیری از نتیجه تکراری با `distinct()`**  
    وقتی روی چند رابطه (مثل `author` و `tags`) هم‌زمان فیلتر می‌زنیم، JOINهای متعدد ممکن است رکوردهای تکراری تولید کنند. در متد `get_queryset` ویو یا با override کردن متد `filter_queryset`، از `.distinct()` استفاده می‌کنیم: `Book.objects.filter(...).distinct()`. این یک مشکل کلاسیک فیلترهای چندرابطه‌ای است.

14. **محدود کردن فیلتر فقط به یک ویو**  
    اگر نخواهیم فیلتر سراسری باشد، مقدار `DEFAULT_FILTER_BACKENDS` را خالی می‌گذاریم و فقط در ویو موردنظر `filter_backends = [DjangoFilterBackend]` را تعیین می‌کنیم. این رویکرد برای وقتی مناسب است که فقط بعضی از endpointها نیاز به فیلتر دارند و بقیه همیشه لیست کامل را برمی‌گردانند.

15. **تست کامل از طریق Browsable API و shell**  
    در مرورگر درگاه `/api/books/` می‌بینیم که DRF به‌صورت خودکار یک فرم فیلتر در بالای صفحه می‌سازد. همه پارامترها را یک‌به‌یک (فیلتر، جستجو، مرتب‌سازی و ترکیب آن‌ها) تست می‌کنیم. سپس در `python manage.py shell` با `request.query_params` و `BookFilter` به‌صورت مستقیم کلاس فیلتر را صدا می‌زنیم و تضمین می‌کنیم خروجی QuerySet همان چیزی است که در API دیده می‌شود.