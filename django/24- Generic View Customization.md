## سرفصل: سفارشی‌سازی Generic Viewها در DRF (Generic View Customization)

### منابع آموزشی

**مستندات رسمی Django REST Framework:**
- [DRF – Generic views — متدهای قابل override مثل get_queryset و perform_create](https://www.django-rest-framework.org/api-guide/generic-views/#overriding-methods)
- [DRF – Tutorial 3: Class-based Views — استفاده از Generic Viewها](https://www.django-rest-framework.org/tutorial/3-class-based-views/)
- [DRF – Views — مرجع APIView و کلاس‌های پایه](https://www.django-rest-framework.org/api-guide/views/)

**مطالب تکمیلی:**
- [Classy DRF — مشاهده‌ی سورس و متدهای هر Generic View](https://www.cdrf.co/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در فروشگاه کتاب `mysite`، APIهای پایه را با Generic Viewها ساخته‌ایم. حالا می‌خواهیم ببینیم چطور همان ویوها را برای نیازهای واقعی سفارشی کنیم: نمایش فقط کتاب‌های موجود، استفاده از Serializer متفاوت برای خواندن و نوشتن، اعمال مجوز، صفحه‌بندی، فیلتر و ست‌کردن خودکار مالک یک رکورد.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **چرا Generic Viewها را سفارشی می‌کنیم؟**  
   Generic Viewها رفتار پیش‌فرض دارند: مثلاً `ListAPIView` همه‌ی رکوردها را برمی‌گرداند. اما در دنیای واقعی معمولاً می‌خواهیم فقط رکوردهای مجاز به کاربر را بدهیم، Serializer متفاوت برای نوشتن و خواندن بگذاریم، یا قبل از ذخیره کاری انجام دهیم. DRF برای همین کارها متدهای مشخصی گذاشته که override می‌کنیم.

2. **override کردن `get_queryset()`**  
   به‌جای تعریف مستقیم `queryset = Book.objects.all()`، یک متد `get_queryset(self)` بنویسید که queryset را برگرداند. این متد در هر درخواست صدا زده می‌شود، پس می‌توانید بر اساس `self.request.user` یا پارامترهای URL آن را تغییر دهید. مثلاً فقط کتاب‌های متعلق به کاربر جاری.

3. **فیلتر کردن queryset بر اساس کاربر جاری**  
   برای APIهای شخصی، در `get_queryset` بنویسید که اگر کاربر لاگین کرده، فقط رکوردهای خودش را ببیند. توجه: `queryset` تعریف‌شده روی کلاس برای کشف خودکار نام ViewSet توسط Router لازم است؛ پس معمولاً هر دو را می‌گذارید: `queryset = Book.objects.all()` برای Router و `get_queryset` برای منطق واقعی.

4. **فیلتر کردن queryset بر اساس پارامترهای URL**  
   فرض کنید URLی دارید مثل `/api/authors/3/books/` که باید فقط کتاب‌های نویسنده‌ی ۳ را بدهد. در `get_queryset` از `self.kwargs` مقدار `author_id` را بخوانید و queryset را با آن فیلتر کنید. این الگو در ViewSetهای تودرتو زیاد استفاده می‌شود.

5. **override کردن `get_serializer_class()`**  
   گاهی برای خواندن (GET) یک Serializer و برای نوشتن (POST/PUT) Serializer دیگری می‌خواهید. متد `get_serializer_class(self)` را override کنید و بر اساس `self.action` یا `self.request.method` تصمیم بگیرید کدام کلاس برگردد. مثلاً `BookReadSerializer` برای خواندن و `BookWriteSerializer` برای نوشتن.

6. **تفاوت `get_serializer_class` و تعریف `serializer_class`**  
   اگر `serializer_class` را مستقیم روی کلاس بگذارید، همه‌ی اکشن‌ها از همان استفاده می‌کنند. اما `get_serializer_class` انعطاف می‌دهد. قاعده: تا وقتی یک Serializer کافی است، ساده‌ترین راه را برو؛ به‌محض نیاز به تفکیک، به متد سوئیچ کن.

7. **تعیین `permission_classes`**  
   با `permission_classes = [IsAuthenticated]` روی کلاس، فقط کاربران واردشده دسترسی دارند. می‌توانید برای هر اکشن مجوز متفاوت بگذارید؛ مثلاً با override کردن `get_permissions()` و بررسی `self.action`. مثلاً خواندن برای همه آزاد و نوشتن فقط برای لاگین‌شده‌ها.

8. **تعیین `authentication_classes`**  
   مشابه مجوزها، با `authentication_classes` مشخص می‌کنید کاربر چگونه احراز هویت شود (Session، Token، JWT). اگر تنظیمات global در `REST_FRAMEWORK` گذاشته باشید، لازم نیست روی هر ویو تکرار کنید؛ اما برای ویو خاص می‌توانید override کنید.

9. **تنظیم `pagination_class` روی یک ویو خاص**  
   اگر در تنظیمات global صفحه‌بندی روشن است، همه‌ی ویوها از آن استفاده می‌کنند. اگر می‌خواهید یک ویو صفحه‌بندی متفاوت داشته باشد (مثلاً صفحه‌ی کوچک‌تر)، `pagination_class = MyPagination` را روی همان کلاس بگذارید.

10. **تعیین `filter_backends` روی ویو**  
    با `filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]` مشخص می‌کنید این ویو از چه فیلترهایی پشتیبانی کند. سپس `filterset_fields`، `search_fields` و `ordering_fields` را تنظیم می‌کنید. جزئیات کامل در سرفصل «Filtering Data» آمده است.

11. **override کردن `lookup_field` و `lookup_url_kwarg`**  
    به‌طور پیش‌فرض DRF از `pk` برای پیدا کردن شیء استفاده می‌کند. اگر بخواهید با اسلاگ یا UUID کار کنید، `lookup_field = 'slug'` را بگذارید. اگر نام پارامتر در URL با نام فیلد مدل فرق دارد، `lookup_url_kwarg` را هم ست کنید.

12. **override کردن `perform_create()`**  
    این متد قبل از ذخیره‌ی شیء جدید صدا زده می‌شود و بهترین جای ست‌کردن فیلدهایی است که از سمت کلاینت نمی‌آیند. مثلاً `serializer.save(owner=self.request.user)`. کد را در متد بنویسید و `serializer` را از `self.get_serializer()` بگیرید.

13. **override کردن `perform_update()` و `perform_destroy()`**  
    مشابه `perform_create`، این دو متد قبل از ویرایش و حذف صدا زده می‌شوند. برای ثبت لاگ، ارسال سیگنال یا جلوگیری از حذف در شرایط خاص از این‌ها استفاده کنید.

14. **override کردن `get_serializer_context()`**  
    اگر Serializer به داده‌ای خارج از خودش نیاز دارد (مثلاً `request`)، آن را از طریق context پاس می‌دهید. متد `get_serializer_context()` را override کنید و به دیکشنری پیش‌فرض چیزی اضافه کنید. این الگو وقتی مفید است که Serializer باید URL مطلق بسازد یا کاربر جاری را بداند.

15. **override کردن `create()` برای منطق پیچیده‌تر**  
    اگر منطق ایجاد از یک خط `perform_create` بیشتر است (مثلاً ایجاد چند مدل مرتبط)، خود متد `create()` را override کنید. سعی کنید منطق را تا جای ممکن در Serializer نگه دارید و ویو را لاغر بمانید.

16. **مشاهده‌ی ترتیب فراخوانی متدها**  
    با اضافه‌کردن چند `print` یا لاگ موقت در `get_queryset`، `get_serializer_class` و `perform_create`، ببینید هنگام یک درخواست POST به ترتیب چه اتفاقی می‌افتد. این آزمایش درک شما از چرخه‌ی Generic View را عمیق می‌کند.

17. **تست تفکیک Serializer خواندن/نوشتن**  
    دو Serializer بسازید که یکی فیلدهای بیشتر و فقط-خواندنی دارد و دیگری فقط فیلدهای نوشتنی. با `get_serializer_class` بین آن‌ها سوئیچ کنید و با curl ببینید پاسخ GET و POST چه تفاوتی دارند.

18. **تمرین تکمیلی: ویوی سفارشی برای کتاب‌های موجود با صفحه‌بندی و فیلتر**  
    یک `ListAPIView` برای کتاب‌ها بسازید که فقط کتاب‌های `is_available=True` را بدهد، از `OrderingFilter` پشتیبانی کند، صفحه‌بندی ۱۰تایی داشته باشد و فقط برای کاربران لاگین‌شده قابل دسترسی باشد. همه‌ی این تنظیمات را روی همان یک کلاس جمع کنید و در مرورگر تست کنید.
