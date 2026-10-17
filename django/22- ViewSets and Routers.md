## سرفصل: ViewSetها و Routerها در DRF (ViewSets and Routers)

### منابع آموزشی

**مستندات رسمی Django REST Framework:**
- [DRF – ViewSets — مرجع کامل ViewSet، ModelViewSet و اکشن‌ها](https://www.django-rest-framework.org/api-guide/viewsets/)
- [DRF – Routers — مرجع کامل Routerها و نحوه‌ی تولید خودکار URL](https://www.django-rest-framework.org/api-guide/routers/)
- [DRF – Tutorial 6: ViewSets & Routers — آموزش گام‌به‌گام ViewSet و Router](https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/)

**مطالب تکمیلی:**
- [Classy DRF — مشاهده‌ی سورس کلاس‌های ViewSet](https://www.cdrf.co/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` فروشگاه کتاب را داریم. تا حالا برای هر عملیات (لیست، ایجاد، جزئیات، ویرایش، حذف) ویوهای جداگانه می‌نوشتیم. می‌خواهیم ببینیم چطور می‌توان همه‌ی این‌ها را در یک کلاس `ViewSet` جمع کرد و با یک `Router` همه‌ی URLها را خودکار ساخت. هدف این است که کد کمتری بنویسیم و ساختار REST یکدست بماند.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **ViewSet چیست و با View معمولی چه تفاوتی دارد؟**  
   یک `ViewSet` کلاسی است که چند اکشن را در خود جمع می‌کند: `list`، `create`، `retrieve`، `update`، `partial_update` و `destroy`. برخلاف `APIView` که هر متد HTTP را خودتان به یک تابع وصل می‌کنید، ViewSet نمی‌داند کدام URL به کدام اکشن می‌رسد؛ این کار Router است. پس ViewSet = منطق، Router = مسیرها.

2. **شروع با `ViewSet` پایه (بدون مدل)**  
   کلاس `viewsets.ViewSet` پایه‌ی همه است و فقط اکشن‌ها را نگه می‌دارد. اگر بخواهید منطق کاملاً دستی داشته باشید، از این ارث‌بری می‌کنید و خودتان `list()`، `retrieve()` و... را می‌نویسید. این مرحله را انجام دهید تا ببینید ViewSet بدون هیچ کمکی چقدر کار دستی دارد.

3. **کلاس `GenericViewSet` و ترکیب با Mixinها**  
   `GenericViewSet` همان ViewSet است اما `get_queryset()` و `get_serializer()` را دارد. با ترکیب آن با Mixinها (مثل `ListModelMixin`) می‌توانید فقط اکشن‌هایی که می‌خواهید را بسازید. این حالت برای وقتی است که نمی‌خواهید همه‌ی CRUD را داشته باشید.

4. **کلاس `ModelViewSet`: CRUD کامل در یک کلاس**  
   `ModelViewSet` از ترکیب همه‌ی Mixinها ساخته شده است. با تعریف فقط دو خط `queryset = Book.objects.all()` و `serializer_class = BookSerializer`، هر شش اکشن را یکجا به دست می‌آورید. این پرکاربردترین ViewSet در پروژه‌های واقعی است. خودتان این کلاس را برای مدل Book بنویسید.

5. **کلاس `ReadOnlyModelViewSet`: فقط خواندن**  
   اگر API فقط باید لیست و جزئیات بدهد و اجازه‌ی تغییر ندارد، از `ReadOnlyModelViewSet` استفاده کنید. این کلاس فقط `list` و `retrieve` را دارد و متدهای POST/PUT/DELETE روی آن به‌طور خودکار خطای 405 برمی‌گردانند. برای مدل Author یک ViewSet فقط-خواندنی بسازید.

6. **`Router` چیست و چرا لازم است؟**  
   Router یک شیء است که با متد `register()` یک ViewSet را می‌گیرد و تمام URLهای لازم را خودکار می‌سازد. به‌جای اینکه پنج `path()` دستی بنویسید، یک خط `register` می‌نویسید. Router می‌داند هر اکشن ViewSet باید به کدام متد HTTP و کدام مسیر وصل شود.

7. **تفاوت `SimpleRouter` و `DefaultRouter`**  
   `SimpleRouter` فقط URLهای ViewSetها را می‌سازد. `DefaultRouter` همان کار را می‌کند به‌علاوه‌ی یک «صفحه‌ی ریشه‌ی API» که فهرست همه‌ی endpointها را با لینک نشان می‌دهد. برای توسعه و کشف آسان API، `DefaultRouter` بهتر است.

8. **ساخت Router و ثبت ViewSet با `register()`**  
   در فایل `urls.py` یک `DefaultRouter` بسازید. با `router.register(r'books', BookViewSet, basename='book')` آن را ثبت کنید. پارامتر اول پیشوند مسیر است (`books`)، دوم خود ViewSet، و سوم `basename` که وقتی `queryset` روی ViewSet تعریف شده باشد اختیاری است اما گذاشتنش توصیه می‌شود.

9. **اتصال URLهای Router به urlpatterns**  
   بعد از ثبت، باید `urlpatterns` را به `router.urls` وصل کنید. یک راه این است که `urlpatterns = router.urls` بگذارید؛ راه بهتر برای پروژه‌های بزرگ این است که `path('api/', include(router.urls))` را داخل `urlpatterns` اصلی بگذارید تا همه‌ی مسیرها زیر پیشوند `api/` بیایند.

10. **مشاهده‌ی URLهایی که Router ساخته است**  
    با `python manage.py show_urls` (اگر django-extensions نصب باشد) یا با بازکردن صفحه‌ی ریشه‌ی DefaultRouter در مرورگر، ببینید Router چه مسیرهایی ساخته: `/api/books/` و `/api/books/{pk}/`. سعی کنید حدس بزنید کدام مسیر به کدام اکشن می‌رسد و بعد تأیید کنید.

11. **افزودن اکشن سفارشی با دکوراتور `@action`**  
    گاهی به endpointی خارج از CRUD نیاز دارید؛ مثلاً «کتاب‌های موجود» یا «امانت‌گرفتن یک کتاب». با `@action(detail=False, methods=['get'])` یک متد روی ViewSet بسازید. `detail=False` یعنی روی کل مجموعه کار می‌کند، و `detail=True` یعنی روی یک شیء خاص (و در URL آن `pk` می‌آید).

12. **تفاوت `detail=True` و `detail=False` در اکشن‌ها**  
    اکشن با `detail=True` روی یک کتاب مشخص کار می‌کند و URL آن چیزی شبیه `/api/books/5/borrow/` است. اکشن با `detail=False` روی همه‌ی کتاب‌ها کار می‌کند و URL آن `/api/books/available/` می‌شود. انتخاب درست این دو، طراحی URL را تمیز نگه می‌دارد.

13. **سفارشی‌سازی `url_path` و `url_name` اکشن**  
    به‌طور پیش‌فرض نام متد در URL استفاده می‌شود. اگر می‌خواهید URL یا نام مسیر فرق کند، در دکوراتور `url_path='in-stock'` و `url_name='in-stock'` را پاس دهید. این کار برای خوانایی URLهای فارسی/انگلیسی مفید است.

14. **گرفتن `pk` در اکشن‌های `detail=True`**  
    در اکشن با `detail=True`، می‌توانید با `self.get_object()` شیء جاری را بگیرید؛ اگر پیدا نشد، خودش 404 می‌دهد. این همان مکانیزمی است که در `retrieve` استفاده می‌شود و نیازی به نوشتن دستی کوئری ندارید.

15. **Router تودرتو (Nested Router) — معرفی**  
    اگر بخواهید URLهایی مثل `/api/books/5/reviews/` داشته باشید (نظرهای یک کتاب خاص)، Router پیش‌فرض Django از آن پشتیبانی نمی‌کند. برای این کار از کتابخانه‌ی `drf-nested-routers` استفاده می‌شود. این را فقط بشناسید؛ در سرفصل «Routers Customization» بیشتر می‌بینیم.

16. **تست همه‌ی endpointهای ViewSet**  
    با سرور در حال اجرا، این مسیرها را تست کنید: `GET /api/books/` (لیست)، `POST /api/books/` (ایجاد)، `GET /api/books/1/` (جزئیات)، `PUT /api/books/1/` (ویرایش کامل)، `PATCH /api/books/1/` (ویرایش جزئی)، `DELETE /api/books/1/` (حذف). هر کدام را با httpie یا curl بزنید و کد وضعیت را ببینید.

17. **مقایسه‌ی کد ViewSet با Viewهای جداگانه**  
    تعداد خطوط کدی که برای همین CRUD با `APIView`های جداگانه می‌نوشتید را بشمارید و با نسخه‌ی ViewSet مقایسه کنید. این مقایسه دلیل اصلی محبوبیت ViewSetها را نشان می‌دهد: حذف کد تکراری.

18. **تمرین تکمیلی: ViewSet برای Review با اکشن سفارشی**  
    یک `ReviewViewSet` بسازید که CRUD کامل داشته باشد. سپس با `@action` یک اکشن `detail=False` به نام `top-rated` اضافه کنید که فقط نظرهای با امتیاز ۵ را برگرداند. آن را در Router ثبت کنید و از طریق مرورگر تست کنید.
