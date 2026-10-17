## سرفصل: Model Relationships

### منابع آموزشی

**مستندات رسمی Django:**
- Many-to-one relationships — مرجع کامل `ForeignKey` با مثال‌های عملی
- Many-to-many relationships — مرجع کامل `ManyToManyField`
- One-to-one relationships — مرجع کامل `OneToOneField` با مثال Place/Restaurant
- Related objects reference — دسترسی به اشیاء مرتبط و `related_name`
---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. حالا می‌خواهیم روابط بین مدل‌ها را برقرار کنیم: هر کتاب یک نویسنده دارد، هر کتاب چند برچسب دارد، و هر نویسنده یک پروفایل اختصاصی دارد. هدف این است که هر سه نوع رابطه را در عمل پیاده کنیم و ببینیم هرکدام چطور در دیتابیس، پنل ادمین و کوئری‌ها رفتار می‌کنند.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت سه نوع رابطه در Django**  
   Django سه نوع رابطه اصلی را پشتیبانی می‌کند: **یک‌به‌چند** (`ForeignKey`)، **چند‌به‌چند** (`ManyToManyField`) و **یک‌به‌یک** (`OneToOneField`). هر رابطه برای مدل‌سازی یک سناریوی واقعی متفاوت استفاده می‌شود.

2. **تعریف رابطه یک‌به‌چند با `ForeignKey` در مدل `Book`**  
   در مدل `Book` یک فیلد به نام `author` از نوع `ForeignKey` به مدل `Author` تعریف می‌کنیم: `author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')`. این یعنی هر کتاب فقط یک نویسنده دارد، اما یک نویسنده می‌تواند چندین کتاب داشته باشد.

3. **تنظیم `on_delete` برای `ForeignKey`**  
   پارامتر `on_delete` اجباری است و مشخص می‌کند وقتی نویسنده حذف شود، کتاب‌هایش چه شوند. گزینه `CASCADE` یعنی کتاب‌ها هم حذف شوند. گزینه `PROTECT` یعنی تا وقتی کتابی به نویسنده وصل است، اجازه حذف نویسنده داده نشود. برای این پروژه `PROTECT` انتخاب می‌کنیم چون کتاب بدون نویسنده معنا ندارد و نمی‌خواهیم به‌طور تصادفی داده از دست برود.

4. **تنظیم `related_name`**  
   با `related_name='books'`، از سمت نویسنده می‌توانیم به کتاب‌هایش دسترسی داشته باشیم: `author.books.all()`. اگر `related_name` تنظیم نشود، Django به‌طور پیش‌فرض `book_set` را می‌سازد که نام زیبایی نیست و در صورت وجود چند `ForeignKey` به یک مدل، دچار تداخل می‌شود.

5. **تعریف رابطه چند‌به‌چند با `ManyToManyField`**  
   یک مدل جدید به نام `Tag` تعریف می‌کنیم با فیلد `name`. سپس در مدل `Book` یک فیلد `tags` از نوع `ManyToManyField` به `Tag` اضافه می‌کنیم. این یعنی هر کتاب می‌تواند چند برچسب داشته باشد و هر برچسب می‌تواند روی چند کتاب باشد.

6. **درک جدول واسط در رابطه چند‌به‌چند**  
   وقتی `ManyToManyField` تعریف می‌کنیم، Django به‌طور خودکار یک جدول واسط (junction table) در دیتابیس می‌سازد. این جدول فقط دو ستون دارد: شناسه کتاب و شناسه برچسب. بعد از `migrate` می‌توانیم این جدول را در دیتابیس ببینیم.

7. **تعریف رابطه یک‌به‌یک با `OneToOneField`**  
   یک مدل جدید به نام `AuthorProfile` تعریف می‌کنیم با فیلدهای `website` و `birth_date`. سپس در آن یک فیلد `author` از نوع `OneToOneField` به مدل `Author` تعریف می‌کنیم: `author = models.OneToOneField(Author, on_delete=models.CASCADE)`. این یعنی هر نویسنده فقط یک پروفایل دارد و هر پروفایل فقط به یک نویسنده تعلق دارد.

8. **تفاوت `OneToOneField` با `ForeignKey`**  
   `OneToOneField` در واقع یک `ForeignKey` با `unique=True` است. یعنی مثل `ForeignKey` یک رابطه است، ولی در سمت «چند» فقط یک رکورد مجاز است. این برای مواردی مناسب است که می‌خواهیم یک مدل را به‌طور اختصاصی به یک رکورد دیگر وصل کنیم، مثل پروفایل کاربر.

9. **اجرای `makemigrations` و بررسی migration**  
   دستور `python manage.py makemigrations` را اجرا می‌کنیم. Django یک فایل migration می‌سازد. فایل را باز می‌کنیم و می‌بینیم که برای `ForeignKey` یک `AddField` با `ForeignKey` ساخته شده، برای `ManyToManyField` یک `AddField` با `ManyToManyField` و برای `OneToOneField` یک `AddField` با `OneToOneField`.

10. **اجرای `migrate` و مشاهده جداول در دیتابیس**  
    دستور `python manage.py migrate` را اجرا می‌کنیم. سپس با ابزار خط فرمان دیتابیس (psql یا mysql) جداول را می‌بینیم:
    - جدول `shop_book` یک ستون `author_id` دارد (ForeignKey)
    - جدول `shop_book_tags` به‌عنوان جدول واسط ساخته شده (ManyToMany)
    - جدول `shop_authorprofile` یک ستون `author_id` با `UNIQUE` دارد (OneToOne)

11. **ثبت مدل‌ها در `admin.py`**  
    مدل‌های `Author`، `Book`، `Tag` و `AuthorProfile` را در `admin.py` ثبت می‌کنیم. حالا در پنل ادمین می‌توانیم داده وارد کنیم.

12. **ورود داده نمونه و مشاهده روابط در ادمین**  
    وارد `/admin/` می‌شویم:
    - دو نویسنده اضافه می‌کنیم: «ج. ک. رولینگ» و «ج. ر. ر. تالکین»
    - سه کتاب اضافه می‌کنیم: «هری پاتر ۱» (نویسنده: رولینگ)، «هری پاتر ۲» (نویسنده: رولینگ)، «ارباب حلقه‌ها» (نویسنده: تالکین)
    - سه برچسب اضافه می‌کنیم: «فانتزی»، «ماجراجویی»، «کلاسیک»
    - «هری پاتر ۱» را به برچسب‌های «فانتزی» و «ماجراجویی» وصل می‌کنیم
    - برای رولینگ یک `AuthorProfile` با website و birth_date می‌سازیم
    
    در پنل ادمین می‌بینیم که وقتی «رولینگ» را باز می‌کنیم، کتاب‌هایش نمایش داده می‌شوند (چون `related_name='books'` تنظیم شده). همچنین برچسب‌های هر کتاب در صفحه ویرایش کتاب قابل مشاهده و انتخاب هستند.

13. **تست کوئری‌های رو به جلو (Forward) در shell**  
    در `python manage.py shell`:
    - `book.author` → نویسنده کتاب را برمی‌گرداند
    - `book.tags.all()` → برچسب‌های کتاب را برمی‌گرداند
    - `author.authorprofile` → پروفایل نویسنده را برمی‌گرداند

14. **تست کوئری‌های معکوس (Reverse) در shell**  
    - `author.books.all()` → کتاب‌های نویسنده را برمی‌گرداند (به لطف `related_name`)
    - `tag.book_set.all()` → کتاب‌های یک برچسب را برمی‌گرداند (پیش‌فرض `book_set`)
    - `author.authorprofile` → پروفایل نویسنده را برمی‌گرداند

15. **فیلتر کردن بر اساس روابط در shell**  
    - `Book.objects.filter(author__name='ج. ک. رولینگ')` → کتاب‌های رولینگ
    - `Book.objects.filter(tags__name='فانتزی')` → کتاب‌های فانتزی
    - `Author.objects.filter(authorprofile__website__contains='rowling')` → نویسنده‌ای که website او شامل rowling است

16. **اضافه کردن `select_related` و `prefetch_related` برای بهینه‌سازی**  
    `select_related` برای `ForeignKey` و `OneToOneField` استفاده می‌شود و در یک کوئری JOIN می‌زند. `prefetch_related` برای `ManyToManyField` استفاده می‌شود و در یک کوئری جداگانه داده را می‌آورد. در shell تست می‌کنیم:
    - `Book.objects.select_related('author').all()` → همه کتاب‌ها با نویسنده در یک کوئری
    - `Book.objects.prefetch_related('tags').all()` → همه کتاب‌ها با برچسب‌ها در دو کوئری

17. **افزودن یک `ForeignKey` دیگر به همان مدل و تأثیر آن روی `related_name`**  
    به مدل `Book` یک فیلد `editor` از نوع `ForeignKey` به `Author` اضافه می‌کنیم (ویراستار کتاب). چون حالا دو `ForeignKey` به `Author` داریم، Django خطا می‌دهد اگر `related_name` تنظیم نکنیم. برای `author` مقدار `related_name='written_books'` و برای `editor` مقدار `related_name='edited_books'` می‌گذاریم. این نشان می‌دهد چرا `related_name` ضروری است.

18. **تعریف `ManyToManyField` با `through` برای ذخیره اطلاعات اضافی**  
    اگر بخواهیم برای رابطه بین کتاب و برچسب یک فیلد اضافی مثل `added_at` (زمان اضافه شدن برچسب) ذخیره کنیم، یک مدل واسط به نام `BookTag` تعریف می‌کنیم با دو `ForeignKey` به `Book` و `Tag` و یک `added_at`. سپس در `Book`، فیلد `tags` را با `through='BookTag'` تعریف می‌کنیم. این روش برای روابط چند‌به‌چند پیچیده‌تر استفاده می‌شود.

19. **تست حذف و رفتار `on_delete`**  
    در پنل ادمین یک نویسنده را حذف می‌کنیم. چون `on_delete=models.PROTECT` تنظیم شده، Django اجازه حذف نمی‌دهد و خطا می‌دهد که ابتدا باید کتاب‌ها را حذف یا منتقل کرد. این رفتار امن‌تر از `CASCADE` است.

20. **بررسی `CheckConstraint` برای اعتبارسنجی سطح دیتابیس**  
    در `Meta.constraints` مدل `Book` یک `CheckConstraint` تعریف می‌کنیم که مطمئن شود `price` همیشه مثبت است. بعد از `migrate`، دیتابیس این constraint را اعمال می‌کند و اگر کسی سعی کند کتاب با قیمت منفی ذخیره کند، خطا می‌دهد.

---

### پروژه کوچک: «سیستم مدیریت کتابخانه با روابط کامل»

**هدف:** پیاده‌سازی یک سیستم کتابخانه با هر سه نوع رابطه مدل‌ها و کوئری‌های پیشرفته

**سطح:** متوسط

**تیتر کارها:**

- تعریف مدل `Author` با فیلدهای `name` و `email`
- تعریف مدل `Book` با فیلدهای `title`، `isbn`، `price` و `published_date`
- افزودن `ForeignKey` از `Book` به `Author` با `on_delete=PROTECT` و `related_name='books'`
- تعریف مدل `Tag` با فیلد `name`
- افزودن `ManyToManyField` از `Book` به `Tag`
- تعریف مدل `AuthorProfile` با `website`، `birth_date` و `OneToOneField` به `Author`
- اجرای `makemigrations` و `migrate`
- ثبت همه مدل‌ها در `admin.py`
- افزودن ۳ نویسنده، ۶ کتاب، ۴ برچسب و ۳ پروفایل از پنل ادمین
- اتصال برچسب‌ها به کتاب‌ها در پنل ادمین
- تست کوئری‌های Forward و Reverse در shell
- تست فیلتر کردن بر اساس روابط (`author__name`، `tags__name`)
- افزودن `select_related` و `prefetch_related` و مقایسه تعداد کوئری‌ها
- افزودن `CheckConstraint` برای قیمت مثبت
- تست حذف نویسنده و مشاهده رفتار `PROTECT`