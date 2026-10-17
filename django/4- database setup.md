## سرفصل: Database Setup

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` می‌خواهیم از دیتابیس پیش‌فرض SQLite شروع کنیم، آن را بشناسیم، سپس به PostgreSQL مهاجرت کنیم و در نهایت داده‌ها را در پنل ادمین ببینیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت تنظیمات پیش‌فرض دیتابیس**  
   فایل `settings.py` را باز می‌کنیم. بخش `DATABASES` را می‌بینیم. به طور پیش‌فرض `ENGINE` روی `django.db.backends.sqlite3` و `NAME` روی `BASE_DIR / 'db.sqlite3'` تنظیم شده است.

2. **بررسی فایل `db.sqlite3`**  
   بعد از اولین `migrate`، یک فایل به نام `db.sqlite3` در ریشه پروژه ساخته می‌شود. این فایل خود دیتابیس است.

3. **اجرای `migrate` اولیه**  
   دستور `python manage.py migrate` را اجرا می‌کنیم. این دستور جداول پیش‌فرض Django (کاربران، sessionها و…) را در دیتابیس SQLite می‌سازد.

4. **ایجاد superuser**  
   با `python manage.py createsuperuser` یک کاربر ادمین می‌سازیم. سپس وارد پنل ادمین (`/admin/`) می‌شویم و می‌بینیم کاربر ساخته شده در دیتابیس ذخیره شده است.

5. **نصب PostgreSQL روی سیستم**  
   PostgreSQL را روی سیستم نصب می‌کنیم. سپس با ابزار خط فرمان یا GUI یک دیتابیس خالی به نام `mysite_db` می‌سازیم.

6. **نصب درایور PostgreSQL برای پایتون**  
   بسته `psycopg2-binary` را نصب می‌کنیم. این درایور به Django اجازه می‌دهد با PostgreSQL ارتباط برقرار کند.

7. **تغییر `DATABASES` در `settings.py`**  
   بخش `DATABASES` را از SQLite به PostgreSQL تغییر می‌دهیم. مقادیر `ENGINE`، `NAME`، `USER`، `PASSWORD`، `HOST` و `PORT` را مطابق دیتابیس PostgreSQL خود تنظیم می‌کنیم.

8. **بررسی صحت تنظیمات با `check --database default`**  
   دستور `python manage.py check --database default` را اجرا می‌کنیم. اگر تنظیمات درست باشد، خطایی نمایش داده نمی‌شود.

9. **اجرای migrate روی PostgreSQL**  
   دوباره `python manage.py migrate` را اجرا می‌کنیم. این بار جداول در PostgreSQL ساخته می‌شوند، نه در SQLite.

10. **مشاهده جداول در PostgreSQL**  
    با ابزار خط فرمان PostgreSQL یا GUI، وارد دیتابیس `mysite_db` می‌شویم. جداولی مثل `auth_user`، `django_session` و… را می‌بینیم که Django ساخته است.

11. **ایجاد superuser جدید در PostgreSQL**  
    چون دیتابیس عوض شده، superuser قبلی در PostgreSQL وجود ندارد. دوباره `createsuperuser` را اجرا می‌کنیم و ادمین جدید در PostgreSQL ساخته می‌شود.

12. **تست نهایی**  
    سرور را اجرا می‌کنیم، وارد `/admin/` می‌شویم و با کاربر جدید لاگین می‌کنیم. داده‌ها حالا در PostgreSQL ذخیره می‌شوند.