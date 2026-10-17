## سرفصل: Migrations در Django (Django Database Migrations)

### منابع آموزشی

**مستندات رسمی Django:**
- [Django – Migrations — راهنمای کامل مدیریت migrationها](https://docs.djangoproject.com/en/5.2/topics/migrations/)
- [Django – Migration operations — مرجع عملیات‌های migration (AddField, RunPython و ...)](https://docs.djangoproject.com/en/5.2/ref/migration-operations/)
- [Django – Migrations commands — دستورات makemigrations, migrate, sqlmigrate, showmigrations](https://docs.djangoproject.com/en/5.2/ref/django-admin/#django-admin-makemigrations)

**مطالب تکمیلی:**
- [Django – Data migrations — نوشتن migration داده‌ای](https://docs.djangoproject.com/en/5.2/topics/migrations/#data-migrations)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در فروشگاه کتاب `mysite` مدل‌هایمان را چند بار تغییر داده‌ایم. می‌خواهیم دقیقاً بفهمیم migration چیست، چطور ساخته می‌شود، چطور روی دیتابیس اعمال می‌شود و اگر اشتباه کردیم چطور برگردانیم. همچنین می‌خواهیم داده‌ی موجود را با یک migration داده‌ای پر کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **Migration چیست؟**  
   Migration یک فایل پایتونی است که تغییرات مدل‌ها را به تغییرات دیتابیس ترجمه می‌کند. Django مدل‌های شما را با آخرین migration مقایسه می‌کند و فایل‌هایی می‌سازد که «چه چیزی در دیتابیس باید عوض شود» را توصیف می‌کنند. بدون migration، دیتابیس شما با مدل‌ها هم‌خوان نمی‌شود.

2. **ساخت migration با `makemigrations`**  
   بعد از تغییر مدل، `python manage.py makemigrations` را اجرا کنید. Django فایل migration جدید در پوشه‌ی `migrations/` اپ می‌سازد. این فایل هنوز روی دیتابیس اثر نگذاشته؛ فقط توصیف تغییر است. خروجی دستور را ببینید که می‌گوید چه عملیاتی انجام می‌شود.

3. **اعمال migration با `migrate`**  
   با `python manage.py migrate` فایل‌های migration روی دیتابیس اعمال می‌شوند. Django یک جدول داخلی به نام `django_migrations` دارد که می‌داند کدام migrationها قبلاً اجرا شده‌اند. دوباره اجرا کنید؛ می‌بینید که می‌گوید «No migrations to apply».

4. **مشاهده‌ی محتوای فایل migration**  
   فایل ساخته‌شده را باز کنید. می‌بینید یک کلاس `Migration` با دو لیست `dependencies` (وابستگی به migrationهای قبلی) و `operations` (عملیات‌هایی مثل `AddField` یا `CreateModel`). این فایل کد پایتونی است و می‌توانید آن را بخوانید و بفهمید.

5. **دیدن SQL با `sqlmigrate`**  
   با `python manage.py sqlmigrate shop 0002` می‌توانید SQLی که این migration اجرا می‌کند را ببینید، بدون اینکه اجرا شود. این ابزار برای یادگیری و دیباگ عالی است. ببینید `AddField` به چه SQLی ترجمه شده است.

6. **مشاهده‌ی وضعیت با `showmigrations`**  
   `python manage.py showmigrations` فهرست همه‌ی migrationها را با علامت `[X]` (اجراشده) یا `[ ]` (اجرا نشده) نشان می‌دهد. این دستور برای دیدن اینکه کجا گیر کرده‌اید ضروری است.

7. **برگرداندن migration (Rollback)**  
   با `python manage.py migrate shop 0001` می‌توانید به migration قبلی برگردید. Django عملیات را برعکس انجام می‌دهد (مثلاً جدول اضافه‌شده را حذف می‌کند). توجه: اگر migration داده را حذف کرده باشد، برگرداندن، داده را برنمی‌گرداند. همیشه در محیط تست امتحان کنید.

8. **برگرداندن همه‌ی migrationهای یک اپ**  
   با `python manage.py migrate shop zero` همه‌ی migrationهای اپ shop برگردانده می‌شوند. این کار جدول‌های آن اپ را حذف می‌کند. در محیط توسعه مفید است اما در production باید با احتیاط انجام شود.

9. **migrationهای هم‌نام و ترتیب شماره‌ها**  
   هر migration یک شماره‌ی ترتیبی دارد (مثل `0001_initial`, `0002_add_field`). شماره‌ها ترتیب اجرا را تعیین می‌کنند. اگر چند نفر روی یک پروژه کار کنند، ممکن است شماره‌ها تداخل کنند؛ در این حالت باید migrationها را ادغام یا دوباره بسازید.

10. **تغییر نام فیلد**  
    اگر نام فیلد را عوض کنید، Django به‌طور پیش‌فرض فکر می‌کند فیلد قدیمی حذف و فیلد جدید اضافه شده. برای اینکه داده از دست نرود، هنگام `makemigrations` به سؤال Django پاسخ دهید که «تغییر نام» است یا اینکه از `RenameField` دستی استفاده کنید. این نکته‌ی مهمی برای حفظ داده است.

11. **افزودن فیلد غیرقابل‌خالی به جدول موجود**  
    اگر فیلدی با `null=False` و بدون `default` به مدل اضافه کنید، `makemigrations` از شما مقدار پیش‌فرض می‌پرسد. می‌توانید یک مقدار یک‌بارمصرف بدهید یا در مدل `default` تعریف کنید. اگر `default` بگذارید، دیگر پرسیده نمی‌شود.

12. **migration داده‌ای با `RunPython`**  
    گاهی باید داده را تغییر دهید نه ساختار را. یک migration خالی بسازید (`makemigrations --empty shop`) و با `RunPython` یک تابع پایتونی بنویسید که روی دیتابیس کار کند. مثلاً همه‌ی کتاب‌ها را «موجود» کنید. تابع هم forward (اعمال) و هم backward (برگشت) می‌گیرد.

13. **نوشتن تابع forward و backward**  
    تابع forward منطق اصلی است و backward باید برعکس آن را انجام دهد (یا اگر ممکن نیست، `migrations.RunPython.noop` بدهید). بدون backward، برگرداندن migration خطا می‌دهد. برای تغییرات داده‌ای، همیشه فکر کنید چطور برگردانده می‌شود.

14. **نکته‌ی مهم در migration داده‌ای**  
    در migration داده‌ای، از مدل واقعی (`from shop.models import Book`) استفاده نکنید؛ چون مدل ممکن است در آینده تغییر کند و migration بشکند. به‌جایش از `apps.get_model('shop', 'Book')` استفاده کنید تا نسخه‌ی مدل در لحظه‌ی آن migration را بگیرید.

15. **ادغام migrationها با `squashmigrations`**  
    اگر migrationها زیاد شدند، می‌توانید با `python manage.py squashmigrations shop 0001 0010` آن‌ها را در یک migration ادغام کنید. این کار تاریخچه را تمیز می‌کند اما باید با احتیاط انجام شود چون migrationهای دیگر ممکن است به آن‌ها وابسته باشند.

16. **مشکل migrationهای ناهمگام در تیم**  
    وقتی چند نفر هم‌زمان migration می‌سازند، ممکن است دو migration با یک شماره ساخته شود و خطای «conflicting migrations» بگیرید. راه‌حل `python manage.py makemigrations --merge` است که دو شاخه را ادغام می‌کند. بهتر است قبل از merge با تیم هماهنگ کنید.

17. **اجرای migration در محیط production**  
    در production، migration را با احتیاط و معمولاً در یک مرحله‌ی جدا از deploy اجرا کنید. برای تغییرات سنگین (مثل اضافه‌کردن index روی جدول بزرگ) ممکن است دیتابیس قفل شود. همیشه قبل از اجرا بکاپ بگیرید و روی محیط تست امتحان کنید.

18. **تست migrationها**  
    با `python manage.py makemigrations --check --dry-run` می‌توانید در CI بررسی کنید که همه‌ی تغییرات مدل migration دارند یا نه. اگر خروجی چیزی نشان داد، یعنی کسی مدل را عوض کرده اما migration نساخته. این چک جلوی خطاهای محیط production را می‌گیرد.

19. **تمرین تکمیلی: چرخه‌ی کامل migration**  
    این سناریو را کامل انجام دهید: یک فیلد `discount_percent` به مدل Book اضافه کنید، `makemigrations` و `migrate` بزنید، با `sqlmigrate` SQL را ببینید، سپس یک migration داده‌ای بنویسید که مقدار این فیلد را برای همه‌ی کتاب‌های موجود صفر کند. بعد migration را برگردانید (`migrate shop <شماره‌ی قبل>`) و ببینید چه اتفاقی می‌افتد. در پایان `showmigrations` را بزنید و وضعیت را بررسی کنید.
