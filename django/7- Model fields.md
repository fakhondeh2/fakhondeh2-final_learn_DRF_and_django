### تمرین عملی

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. حالا می‌خواهیم برای مدل‌های `Author`، `Book` و `Review` فیلدهای مناسب انتخاب کنیم، آپشن‌های هر فیلد را تنظیم کنیم و ببینیم هر انتخاب چه تأثیری روی دیتابیس و فرم‌ها دارد.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت مفهوم Field و تفاوت آن با attribute معمولی**  
   هر فیلد در مدل، یک نمونه از یک کلاس `Field` است. Django از روی نوع فیلد، نوع ستون دیتابیس، ویجت فرم و قوانین اعتبارسنجی را تعیین می‌کند.

2. **مرور فیلدهای رشته‌ای: `CharField` و `TextField`**  
   در مدل `Author`، فیلد `name` را از نوع `CharField` با `max_length=100` تعریف می‌کنیم (برای نام‌های کوتاه). فیلد `bio` را از نوع `TextField` می‌گذاریم چون زندگینامه می‌تواند طولانی باشد و محدودیت طول ندارد.

3. **مرور فیلدهای عددی: `IntegerField`، `FloatField` و `DecimalField`**  
   در مدل `Book`، فیلد `stock` (موجودی) را از نوع `IntegerField` تعریف می‌کنیم. برای `price` از `DecimalField` با `max_digits=10` و `decimal_places=2` استفاده می‌کنیم تا قیمت دقیقاً دو رقم اعشار داشته باشد. `FloatField` برای قیمت مناسب نیست چون ممکن است خطای دقت ایجاد کند.

4. **مرور فیلدهای بولین: `BooleanField`**  
   در مدل `Book`، فیلد `is_available` را از نوع `BooleanField` با `default=True` تعریف می‌کنیم. این فیلد مشخص می‌کند کتاب موجود است یا نه.

5. **مرور فیلدهای تاریخ و زمان: `DateField`، `TimeField` و `DateTimeField`**  
   در مدل `Book`، فیلد `published_date` را از نوع `DateField` تعریف می‌کنیم. در مدل `Review`، فیلد `created_at` را از نوع `DateTimeField` با `auto_now_add=True` می‌گذاریم تا هنگام ساخت اولین‌بار، تاریخ و ساعت به‌طور خودکار ثبت شود.

6. **مرور فیلدهای رابطه‌ای: `ForeignKey`، `ManyToManyField` و `OneToOneField`**  
   در مدل `Book`، فیلد `author` را از نوع `ForeignKey` به `Author` تعریف می‌کنیم (هر کتاب یک نویسنده). فیلد `tags` را از نوع `ManyToManyField` تعریف می‌کنیم (هر کتاب چند برچسب، هر برچسب چند کتاب). در مدل `Author`، فیلد `profile` را از نوع `OneToOneField` به مدل `Profile` تعریف می‌کنیم (هر نویسنده یک پروفایل).

7. **مرور فیلدهای فایل: `FileField` و `ImageField`**  
   در مدل `Book`، فیلد `cover` را از نوع `ImageField` با `upload_to='covers/'` تعریف می‌کنیم. در مدل `Author`، فیلد `resume` را از نوع `FileField` با `upload_to='resumes/'` تعریف می‌کنیم. این فیلدها فایل‌ها را در مسیر مشخص‌شده ذخیره می‌کنند.

8. **تنظیم آپشن `null` و `blank` و تفاوت آن‌ها**  
   `null=True` یعنی دیتابیس می‌تواند مقدار NULL ذخیره کند. `blank=True` یعنی فرم اجازه می‌دهد فیلد خالی بماند. برای `bio` هر دو را `True` می‌گذاریم. برای `name` هر دو را `False` می‌گذاریم (اجباری). برای فیلدهای رشته‌ای، Django توصیه می‌کند به‌جای `null=True` از رشته خالی استفاده شود.

9. **تنظیم `default` برای فیلدها**  
   برای `stock` مقدار `default=0` می‌گذاریم. برای `is_available` مقدار `default=True` می‌گذاریم. برای `created_at` از `auto_now_add=True` استفاده می‌کنیم (نه `default`).

10. **تنظیم `choices` برای فیلدهای محدود**  
    در مدل `Book`، فیلد `language` را از نوع `CharField` با `choices` تعریف می‌کنیم. مقادیر مجاز: `'fa'` (فارسی)، `'en'` (انگلیسی)، `'ar'` (عربی). این کار باعث می‌شود فقط مقادیر مجاز قابل انتخاب باشند.

11. **تنظیم `unique` و `db_index`**  
    فیلد `isbn` در مدل `Book` را با `unique=True` تعریف می‌کنیم تا شماره ISBN تکراری نباشد. فیلد `title` را با `db_index=True` تعریف می‌کنیم تا جستجو بر اساس عنوان سریع‌تر شود.

12. **تنظیم `verbose_name` و `help_text`**  
    برای هر فیلد یک `verbose_name` فارسی و یک `help_text` تنظیم می‌کنیم. مثلاً `title = models.CharField(max_length=200, verbose_name='عنوان کتاب', help_text='عنوان کامل کتاب را وارد کنید')`. این مقادیر در پنل ادمین و فرم‌ها نمایش داده می‌شوند.

13. **اجرای migration و مشاهده تأثیر فیلدها در دیتابیس**  
    بعد از تعریف همه فیلدها، `makemigrations` و `migrate` را اجرا می‌کنیم. سپس با ابزار خط فرمان دیتابیس (psql یا mysql) ساختار جدول `shop_book` را می‌بینیم. مثلاً می‌بینیم که `price` به `numeric(10,2)` و `is_available` به `boolean` تبدیل شده است.

14. **تست رفتار فیلدها در پنل ادمین**  
    وارد `/admin/` می‌شویم. می‌بینیم که فیلد `bio` خالی قابل ذخیره است (چون `blank=True`)، فیلد `name` خالی نیست (چون `blank=False`)، و فیلد `language` یک dropdown با سه گزینه فارسی، انگلیسی و عربی نشان می‌دهد (چون `choices` تنظیم شده).

15. **تست کوئری‌های فیلتر بر اساس فیلدها در shell**  
    در `python manage.py shell`:
    - `Book.objects.filter(is_available=True)` → کتاب‌های موجود
    - `Book.objects.filter(price__lt=500000)` → کتاب‌های زیر ۵۰۰ هزار تومان
    - `Book.objects.filter(language='fa')` → کتاب‌های فارسی
    - `Book.objects.order_by('-published_date')` → مرتب‌سازی بر اساس تاریخ انتشار

16. **تغییر نوع یک فیلد و migration مجدد**  
    فیلد `stock` را از `IntegerField` به `PositiveIntegerField` تغییر می‌دهیم تا فقط اعداد مثبت قبول کند. `makemigrations` و `migrate` را اجرا می‌کنیم. این بار Django یک migration برای تغییر نوع ستون می‌سازد.

17. **افزودن یک فیلد جدید و بررسی migration**  
    فیلد `summary` را از نوع `TextField` با `blank=True` به `Book` اضافه می‌کنیم. `makemigrations` را اجرا می‌کنیم. Django از ما می‌پرسد چون فیلد جدید `null=True` ندارد و `default` هم ندارد. گزینه `Provide a one-off default` را انتخاب می‌کنیم و مقدار `''` می‌دهیم. سپس `migrate` را اجرا می‌کنیم.

18. **بررسی خطای ناشی از `null=True` روی فیلد رشته‌ای**  
    فیلد `title` را موقتاً با `null=True` تعریف می‌کنیم. `makemigrations` را اجرا می‌کنیم. Django هشدار می‌دهد که `null=True` روی `CharField` توصیه نمی‌شود. این هشدار را می‌بینیم و به `null=False` برمی‌گردانیم.

19. **تنظیم `db_column` برای تغییر نام ستون**  
    فیلد `isbn` را با `db_column='isbn_number'` تعریف می‌کنیم. `migrate` را اجرا می‌کنیم و در دیتابیس می‌بینیم که نام ستون به `isbn_number` تغییر کرده، ولی در کد پایتون همچنان `isbn` استفاده می‌شود.