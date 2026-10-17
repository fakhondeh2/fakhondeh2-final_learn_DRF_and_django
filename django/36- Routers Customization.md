## سرفصل: Routers Customization

### منابع آموزشی

**مستندات رسمی Django REST Framework:**
- [Routers — مرجع کامل روترها، DefaultRouter و ساخت روتر سفارشی](https://www.django-rest-framework.org/api-guide/routers/)
- [ViewSets — مرجع ViewSetها و @action](https://www.django-rest-framework.org/api-guide/viewsets/)

**پکیج‌های شخص ثالث:**
- [drf-nested-routers — مستندات روترهای تو در تو برای DRF](https://github.com/alanjds/drf-nested-routers)
- [drf-extensions — اکشن‌ها و روترهای پیشرفته برای DRF](https://chibisov.github.io/drf-extensions/docs/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. ViewSetهایی برای `Author`، `Book` و `Review` ساخته‌ایم. حالا می‌خواهیم مدیریت URLها را با روترها بهینه کنیم، مسیرهای تو در تو (مثل لیست کتاب‌های یک نویسنده) با `drf-nested-routers` بسازیم و اکشن‌های سفارشی مثل حذف گروهی (bulk delete) اضافه کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت Router و تفاوت آن با urls.py دستی**  
   Router در DRF یک ابزار است که به‌طور خودکار URLها را برای یک ViewSet تولید می‌کند. به‌جای اینکه برای هر اکشن (`list`، `retrieve`، `create` و...) یک `path` دستی در `urls.py` بنویسیم، یک Router استاندارد مثل `DefaultRouter` همه آن‌ها را با یک `router.register()` ایجاد می‌کند. این کار باعث می‌شود kencode DRY بماند و از اشتباهات تایپی در URLها جلوگیری شود.

2. **استفاده از DefaultRouter پایه**  
   در `mysite/urls.py` یک `DefaultRouter` ساخته و `BookViewSet` را با `router.register('books', BookViewSet, basename='book')` ثبت می‌کنیم. سپس `urlpatterns` اصلی را با `path('api/', include(router.urls))` به Router وصل می‌کنیم. حالا مسیرهای `/api/books/`، `/api/books/{id}/` به‌طور خودکار فعال هستند.

3. **شناخت پارامتر basename و نقش آن**  
   پارامتر `basename` نام پایه مسیرها را مشخص می‌کند و در URLهای معکوس (reverse) و در `permissions` و `actions` استفاده می‌شود. اگر ViewSet یک `queryset` داشته باشد، basename به‌طور خودکار از نام ViewSet گرفته می‌شود، اما اگر `queryset` حذف شده باشد یا ViewSet سفارشی باشد، حتماً باید `basename` را دستی مشخص کنیم. این تفاوت را تست می‌کنیم.

4. **ساخت Router سفارشی با ارث‌بری از DefaultRouter**  
   تفاوت مهم DefaultRouter و SimpleRouter این است که DefaultRouter یک صفحه API root در `/api/` نمایش می‌دهد و از فرمت‌های داده (`.json`، `.api`) پشتیبانی می‌کند. برای شخصی‌سازی بیشتر، یک کلاس `CustomRouter(DefaultRouter)` می‌سازیم و متد `get_urls()` را override می‌کنیم تا بتوانیم مثلاً مسیرهای اضافی یا Prefix سفارشی اضافه کنیم.

5. **اضافه کردن مسیر سفارشی به روتر**  
   در روتر سفارشی، متد `get_urls()` را override می‌کنیم، ابتدا URLهای پیش‌فرض را با `super().get_urls()` می‌گیریم و سپس یک `path` سفارشی (مثلاً `/books/{id}/download/`) به لیست اضافه می‌کنیم. این مسیر به یک View یا ViewSet خاص اشاره می‌کند.

6. **ایجاد اکشن سفارشی با @action و متد HTTP مختلف**  
   در `BookViewSet` یک متد با دکوراتور `@action` می‌سازیم. مثلاً `@action(detail=False, methods=['get'])` برای `popular` که کتاب‌های محبوب را برمی‌گرداند، و `@action(detail=True, methods=['post'])` برای `add_review`. پارامتر `detail=True` یعنی روی یک کتاب خاص، و `detail=False` یعنی روی کل مجموعه. این اکشن‌ها به‌طور خودکار توسط Router به URL تبدیل می‌شوند.

7. **استفاده از url_path برای URL سفارشی اکشن**  
   پارامتر `url_path` در `@action` اجازه می‌دهد نام متد و URL اکشن متفاوت باشند. مثلاً متد `most_rated` با `url_path='top-rated'` به URL `/api/books/top-rated/` تبدیل می‌شود. `url_name` هم برای reverse کردن URL با نام مشخص استفاده می‌شود. این دو پارامتر را همراه هم تست می‌کنیم.

8. **ساخت Bulk Delete با @action**  
   یک اکشن `@action(detail=False, methods=['delete'])` به نام `bulk_delete` در `BookViewSet` می‌سازیم. این اکشن یک لیست از `id`ها را در `request.data` دریافت می‌کند و چند کتاب را هم‌زمان حذف می‌کند. این یک الگوی رایج برای APIهایی است که نیاز به عملیات گروهی دارند. بعد از حذف، تعداد کتاب‌های باقی‌مانده را برمی‌گردانیم.

9. **نصب و پیکربندی drf-nested-routers**  
   پکیج `drf-nested-routers` را با `pip install drf-nested-routers` نصب می‌کنیم. این پکیج اجازه می‌دهد روترها داخل هم قرار بگیرند تا URLهای تو در تو ساخته شوند. سپس `NestedRouter` را import می‌کنیم و برای ساخت مسیر `/api/authors/{author_pk}/books/` از آن استفاده می‌کنیم.

10. **ساخت مسیر تو در تو برای Author و Books**  
    با `NestedRouter` یک Router برای `Author` می‌سازیم و `BookViewSet` را در آن به‌صورت nested ثبت می‌کنیم:
    ```python
    router = NestedRouter()
    router.register('authors', AuthorViewSet, basename='authors')
    router.register('authors/books', BookViewSet, basename='author-books', parents_query_lookups=['author'])
    ```
    حالا `/api/authors/1/books/` همه کتاب‌های نویسنده با id برابر ۱ را برمی‌گرداند.

11. **تنظیم `parents_query_lookups` در NestedRouter**  
    پارامتر `parents_query_lookups` تعیین می‌کند ViewSet کتاب‌ها چگونه کتاب را بر اساس نویسنده پدر فیلتر کند. مقدار `['author']` یعنی فیلد `author` در `queryset` مدل `Book` با `author_pk` در URL فیلتر می‌شود. یک تست با curl بررسی می‌کنیم که آدرس `/api/authors/1/books/` فقط کتاب‌های نویسنده ۱ را برمی‌گرداند.

12. **اضافه کردن nested برای Reviews زیر Books**  
    می‌توانیم سطح دیگری به NestedRouter اضافه کنیم تا `/api/authors/1/books/2/reviews/` کار کند. برای این کار `ReviewViewSet` را با `parents_query_lookups=['author', 'book']` در زیر Book ثبت می‌کنیم. حالا یک مسیر سه‌سطحی داریم که تمام راه‌ها را به‌درستی به هم متصل می‌کند.

13. **استفاده از register برای ثبت چند ViewSet در یک روتر**  
    همه ViewSetهای پروژه (`AuthorViewSet`، `BookViewSet`، `ReviewViewSet`) را در یک روتر واحد ثبت می‌کنیم. اگر همه از DefaultRouter استفاده کنند، آدرس API root (`/api/`) یک لیست کامل از همه مسیرها نشان می‌دهد. خروجی صفحه root را با مرورگر بررسی می‌کنیم.

14. **تست مسیرهای تولیدشده توسط روتر**  
    از دستور `python manage.py show_urls` (با پکیج `django-extensions`) یا بررسی `urls.py` استفاده می‌کنیم تا لیست کامل URLهای تولیدشده توسط روتر را ببینیم. بررسی می‌کنیم که برای هر اکشن استاندارد (list، retrieve، create، update، partial_update، delete) و هر @action سفارشی، مسیر درست تولید شده است.

15. **مقایسه Router با urlpatterns دستی**  
    برای درک ارزش Router، یک مسیر را ابتدا به‌صورت دستی در `urls.py` با `path('books/', BookListView.as_view())` و `path('books/<int:pk>/', BookDetailView.as_view())` می‌نویسیم، سپس همان را با Router پیاده‌سازی می‌کنیم. مقایسه می‌کنیم که Router چقدر کد کمتر و ساختاری یکنواخت‌تر ایجاد می‌کند. در نهایت تصمیم می‌گیریم کدام روش برای پروژه‌های مختلف مناسب‌تر است.