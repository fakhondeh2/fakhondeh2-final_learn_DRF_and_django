## سرفصل: Custom Managers

### منابع آموزشی

**مستندات رسمی Django:**
- [Managers — مرجع کامل Manager، نحوه نام‌گذاری، افزودن متدهای سفارشی و تغییر QuerySet اولیه](https://django.readthedocs.io/en/5.2.x/topics/db/managers.html)

**نمونه‌های عملی در GitHub:**
- [Compile-N-Run – 7-django-model-managers.mdx — کد کامل سه Manager سفارشی برای Product](https://github.com/Compile-N-Run/Compile-N-Run/blob/main/docs/framework/django/3-django-models-and-database/7-django-model-managers.mdx#1)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. حالا می‌خواهیم برای مدل `Book` چند Manager سفارشی بسازیم تا کوئری‌های پرتکرار (کتاب‌های موجود، کتاب‌های تخفیف‌خورده، کتاب‌های یک نویسنده خاص) را از ویوها به لایه مدل منتقل کنیم و کد را DRY نگه داریم. DRY چیست ؟

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت Manager پیش‌فرض و نقش آن**  
   هر مدل Django به‌طور خودکار یک Manager به نام `objects` دارد. وقتی `Book.objects.all()` را می‌نویسیم، در واقع از این Manager استفاده می‌کنیم. Manager یک واسط (facade) نازک روی QuerySet است و متدهایی مثل `filter()`، `get()` و `create()` را فراهم می‌کند.

2. **درک تفاوت Manager و QuerySet**  
   متدهایی که روی `Book.objects` صدا می‌زنیم (مثل `filter` و `exclude`) در واقع روی کلاس QuerySet تعریف شده‌اند، نه Manager. Manager فقط یک لایه روی QuerySet است که هر بار یک QuerySet تازه می‌سازد و متد را روی آن صدا می‌زند. به همین دلیل وقتی می‌خواهیم متد سفارشی بنویسیم، بهتر است آن را روی QuerySet تعریف کنیم و بعد به Manager وصل کنیم.

3. **الگوی صحیح: Custom QuerySet + as_manager()**  
   بهترین الگو برای نوشتن کوئری‌های سفارشی این است: یک کلاس `BookQuerySet` که از `models.QuerySet` ارث‌بری می‌کند بسازیم، متدهای سفارشی را در آن تعریف کنیم، و سپس در مدل بنویسیم `objects = BookQuerySet.as_manager()`. این روش DRY است و نیازی به پیاده‌سازی مجدد متدها در Manager ندارد.

4. **ساخت `BookQuerySet` با متد `available()`**  
   کلاس `BookQuerySet` را در `shop/models.py` تعریف می‌کنیم. یک متد به نام `available()` می‌نویسیم که کتاب‌های موجود (با `stock__gt=0` و `is_available=True`) را برگرداند. این متد یک QuerySet برمی‌گرداند، پس قابل زنجیره‌سازی است.

5. **افزودن متد `on_sale()` به `BookQuerySet`**  
   یک متد دیگر به نام `on_sale()` اضافه می‌کنیم که کتاب‌هایی را برگرداند که فیلد `discount_price` آن‌ها مقدار دارد و کمتر از `price` است. این متد هم قابل زنجیره‌سازی است.

6. **افزودن متد `by_author()` به `BookQuerySet`**  
   یک متد `by_author(name)` اضافه می‌کنیم که کتاب‌های یک نویسنده خاص را بر اساس نام او فیلتر کند: `self.filter(author__name__icontains=name)`. این متد برای ساخت کوئری‌های داینامیک در ویوها مفید است.

7. **افزودن متد `popular()` به `BookQuerySet`**  
   یک متد `popular(min_reviews=10)` اضافه می‌کنیم که کتاب‌هایی را برگرداند که تعداد نظرهایشان بیشتر از یک حد مشخص است. این متد از `annotate` و `Count` استفاده می‌کند: `self.annotate(review_count=Count('review')).filter(review_count__gte=min_reviews)`.

8. **وصل کردن `BookQuerySet` به مدل با `as_manager()`**  
   در مدل `Book` خط `objects = BookQuerySet.as_manager()` را اضافه می‌کنیم. حالا `Book.objects.available()`، `Book.objects.on_sale()` و سایر متدها در دسترس هستند و می‌توان آن‌ها را زنجیره کرد: `Book.objects.available().on_sale()`.

9. **تست زنجیره‌سازی متدها در shell**  
   در `python manage.py shell` کوئری‌های زیر را اجرا می‌کنیم:
   - `Book.objects.available().count()` → تعداد کتاب‌های موجود
   - `Book.objects.available().on_sale()` → کتاب‌های موجود که تخفیف دارند
   - `Book.objects.by_author('رولینگ').available()` → کتاب‌های موجود رولینگ
   - `Book.objects.popular(min_reviews=5).on_sale()` → کتاب‌های محبوبی که تخفیف دارند
   
   هر متد یک QuerySet برمی‌گرداند، پس می‌توان آن‌ها را به‌صورت زنجیره‌ای ترکیب کرد.

10. **ساخت یک Manager سفارشی جداگانه برای کتاب‌های تخفیف‌دار**  
    علاوه بر QuerySet اصلی، یک Manager جداگانه به نام `BookDiscountManager` می‌سازیم که `get_queryset()` را override کند و فقط کتاب‌های تخفیف‌دار را برگرداند:
    ```python
    class BookDiscountManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(discount_price__isnull=False)
    ```
    سپس در مدل `Book` یک فیلد `discounted = BookDiscountManager()` اضافه می‌کنیم. حالا `Book.discounted.all()` فقط کتاب‌های تخفیف‌دار را برمی‌گرداند.

11. **بررسی تفاوت `objects` و `discounted` در ادمین و shell**  
    در shell اجرا می‌کنیم:
    - `Book.objects.count()` → همه کتاب‌ها
    - `Book.discounted.count()` → فقط کتاب‌های تخفیف‌دار
    
    در پنل ادمین هم می‌توانیم یک `ModelAdmin` سفارشی بسازیم که از `discounted` به‌عنوان queryset استفاده کند تا ادمین فقط کتاب‌های تخفیف‌دار را ببیند.

12. **ساخت `ReviewQuerySet` با متد `positive()`**  
    یک کلاس `ReviewQuerySet` برای مدل `Review` می‌سازیم. یک متد `positive()` تعریف می‌کنیم که نظرهای با امتیاز ۴ و ۵ را برگرداند: `self.filter(rating__gte=4)`. سپس در مدل `Review` می‌نویسیم `objects = ReviewQuerySet.as_manager()`.

13. **ترکیب کوئری‌های دو مدل در shell**  
    در shell یک کتاب خاص را می‌گیریم و نظرهای مثبت آن را می‌خوانیم:
    ```python
    book = Book.objects.popular(min_reviews=3).first()
    book.review_set.positive().count()
    ```
    این نشان می‌دهد که Manager سفارشی روی رابطه معکوس (`review_set`) هم کار می‌کند.

14. **ساخت `AuthorQuerySet` با متد `prolific()`**  
    یک `AuthorQuerySet` برای مدل `Author` می‌سازیم. متد `prolific(min_books=3)` تعریف می‌کنیم که نویسندگانی را برگرداند که تعداد کتاب‌هایشان از یک حد مشخص بیشتر است: `self.annotate(book_count=Count('books')).filter(book_count__gte=min_books)`.

15. **استفاده از `prolific()` در ویو**  
    در یک ویو، لیست نویسندگان پرکار را نمایش می‌دهیم: `Author.objects.prolific(min_books=3).order_by('-book_count')`. این کوئری بدون نوشتن منطق پیچیده در ویو، مستقیماً از لایه مدل می‌آید.

16. **افزودن متد `with_rating_avg()` به `BookQuerySet`**  
    یک متد `with_rating_avg()` اضافه می‌کنیم که میانگین امتیاز هر کتاب را به‌عنوان یک attribute اضافه کند: `self.annotate(avg_rating=Avg('review__rating'))`. این متد به ما اجازه می‌دهد در تمپلیت به `book.avg_rating` دسترسی داشته باشیم.

17. **تست `with_rating_avg()` در shell**  
    اجرا می‌کنیم:
    ```python
    for book in Book.objects.with_rating_avg().available():
        print(book.title, book.avg_rating)
    ```
    می‌بینیم که هر کتاب میانگین امتیازش را نشان می‌دهد.

18. **ساخت `Manager.from_queryset()` به‌جای `as_manager()`**  
    برای درک معادل بودن این دو، یک Manager جدید به نام `BookManager` می‌سازیم:
    ```python
    BookManager = models.Manager.from_queryset(BookQuerySet)
    ```
    سپس در مدل `Book` از `BookManager()` استفاده می‌کنیم. نتیجه دقیقاً مثل `BookQuerySet.as_manager()` است.

19. **بررسی اولین Manager و اهمیت ترتیب تعریف**  
    اگر چند Manager در یک مدل تعریف کنیم (مثل `objects` و `discounted`)، اولین Managerی که در مدل تعریف می‌شود به‌عنوان Manager پیش‌فرض Django شناخته می‌شود و در برخی بخش‌ها (مثل migration و admin) استفاده می‌شود. ترتیب تعریف را تغییر می‌دهیم و تأثیر آن را بررسی می‌کنیم.

20. **انتقال منطق از ویو به Manager و مقایسه کد**  
    یک ویو ساده می‌نویسیم که قبلاً کوئری‌های پیچیده را در خودش داشت:
    ```python
    # قبل
    books = Book.objects.filter(stock__gt=0, is_available=True, discount_price__isnull=False)
    ```
    حالا همان ویو را با Manager سفارشی می‌نویسیم:
    ```python
    # بعد
    books = Book.objects.available().on_sale()
    ```
    مقایسه می‌کنیم که چقدر کد خواناتر و قابل تست‌تر شده است. منطق کوئری حالا در یک جای مشخص (مدل) قرار دارد و در چندین ویو قابل استفاده مجدد است.
