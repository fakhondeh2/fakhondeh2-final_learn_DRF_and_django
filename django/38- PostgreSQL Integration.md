## سرفصل: PostgreSQL Integration

### منابع آموزشی

**مستندات رسمی Django:**
- [PostgreSQL notes — تنظیمات خاص PostgreSQL در Django، ایندکس‌ها، فیلدهای خاص و توابع](https://django.readthedocs.io/en/5.2.x/ref/databases.html#postgresql-notes)
- [Database Indexes — نحوه تعریف ایندکس‌ها در مدل‌ها با db_index و Meta.indexes](https://django.readthedocs.io/en/5.2.x/ref/models/indexes.html)
- [Migrations with RunSQL — اجرای SQL خام در migrations](https://django.readthedocs.io/en/5.2.x/ref/migration-operations.html#runsql)

**مستندات psycopg2:**
- [psycopg2 Documentation — راهنمای نصب و پیکربندی اداپتور PostgreSQL برای Python](https://www.psycopg.org/docs/)

**مستندات django-db-connection-pool:**
- [django-db-connection-pool — پیکربندی Connection Pooling برای PostgreSQL در Django](https://github.com/altairbow/django-db-connection-pool)

---
### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. می‌خواهیم دیتابیس پیش‌فرض SQLite را به PostgreSQL تغییر دهیم، ایندکس‌ها را برای بهبود کارایی اضافه کنیم، Connection Pooling را فعال کنیم و یک Stored Procedure ساده با Migration ایجاد کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **نصب psycopg2**  
   ابتدا بسته `psycopg2-binary` را با `pip install psycopg2-binary` نصب می‌کنیم. این بسته اداپتور Python به PostgreSQL است. در محیط تولید معمولاً `psycopg2` (بدون binary) استفاده می‌شود که از کد منبع کامپایل می‌شود. بررسی می‌کنیم که نصب با `python -c "import psycopg2; print(psycopg2.__version__)"` موفق است.

2. **نصب PostgreSQL و ایجاد دیتابیس**  
   با `sudo apt install postgresql` PostgreSQL را نصب می‌کنیم. با `sudo -u postgres psql` وارد shell می‌شویم. دیتابیس `bookstore` و کاربر `bookstore_user` را با رمز ایجاد می‌کنیم: `CREATE DATABASE bookstore; CREATE USER bookstore_user WITH PASSWORD 'secret'; GRANT ALL PRIVILEGES ON DATABASE bookstore TO bookstore_user;`.

3. **پیکربندی `DATABASES` در `settings.py`**  
   تنظیمات `DATABASES` را برای PostgreSQL تغییر می‌دهیم:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'bookstore',
           'USER': 'bookstore_user',
           'PASSWORD': 'secret',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
   سپس `python manage.py migrate` را اجرا می‌کنیم تا جداول در PostgreSQL ساخته شوند. همه جداول قبلی از SQLite به PostgreSQL منتقل می‌شوند.

4. **انتقال داده از SQLite به PostgreSQL با `dumpdata` و `loaddata`**  
   ابتدا از دیتابیس فعلی (SQLite) با `python manage.py dumpdata > db.json` خروجی می‌گیریم. بعد از تغییر تنظیمات به PostgreSQL، با `python manage.py loaddata db.json` داده‌ها را بارگذاری می‌کنیم. بررسی می‌کنیم که تعداد رکوردها در پنل ادمین با قبل برابر است.

5. **ایجاد ایندکس ساده با `db_index=True`**  
   در مدل `Book`، فیلد `isbn` را که معمولاً جستجوی دقیق روی آن انجام می‌شود، با `db_index=True` ایندکس می‌کنیم. یک مایگریشن جدید می‌سازیم و اجرا می‌کنیم. در shell با `python manage.py sqlmigrate shop 00XX` دستور `CREATE INDEX` PostgreSQL را مشاهده می‌کنیم.

6. **ایجاد ایندکس ترکیبی با `Meta.indexes`**  
   در کلاس `Meta` مدل `Book`، یک ایندکس ترکیبی اضافه می‌کنیم:
   ```python
   indexes = [
       models.Index(fields=['price', 'published_date'], name='idx_price_date'),
       models.Index(fields=['author', 'title'], name='idx_author_title'),
   ]
   ```
   ایندکس ترکیبی روی دو فیلد (`price` و `published_date`) باعث می‌شود کوئری‌هایی که هر دو فیلد را فیلتر می‌کنند، سریع‌تر اجرا شوند.

7. **بررسی ایندکس‌ها در PostgreSQL**  
   با `python manage.py dbshell` وارد shell PostgreSQL می‌شویم. با دستور `\di` همه ایندکس‌ها را لیست می‌کنیم. با `\d shop_book` ساختار جدول و ایندکس‌های مدل `Book` را می‌بینیم. با `SELECT * FROM pg_indexes WHERE tablename = 'shop_book';` جزئیات هر ایندکس را مشاهده می‌کنیم.

8. **نصب و پیکربندی Connection Pooling با `django-db-connection-pool`**  
   بسته `django-db-connection-pool` را نصب می‌کنیم. در `settings.py`، `ENGINE` را به `postgresql_pool` تغییر می‌دهیم و تنظیمات Pool را اضافه می‌کنیم:
   ```python
   DATABASES['default']['POOL_SETTINGS'] = {
       'max_pool_size': 10,
       'min_pool_size': 2,
       'pool_name': 'bookstore_pool',
       'timeout': 60,
   }
   ```
   Connection Pooling تعداد اتصالات هم‌زمان به دیتابیس را مدیریت می‌کند و از ایجاد اتصال جدید برای هر درخواست جلوگیری می‌کند.

9. **مدیریت چند Schema در PostgreSQL**  
   در PostgreSQL می‌توانیم از چند Schema استفاده کنیم. یک Schema جدید به نام `inventory` با `CREATE SCHEMA inventory;` ایجاد می‌کنیم. در مدل `Book` با استفاده از `Meta.db_table = 'inventory.book'` جدول را در Schema مشخص قرار می‌دهیم. این روش برای جداسازی منطقی ماژول‌های بزرگ کاربرد دارد.

10. **افزودن `Meta.constraints` با CheckConstraint**  
    یک محدودیت سطح جدول اضافه می‌کنیم تا قیمت کتاب همیشه مثبت باشد:
    ```python
    constraints = [
        models.CheckConstraint(
            check=models.Q(price__gt=0),
            name='price_positive'
        )
    ]
    ```
    این محدودیت در سطح دیتابیس اعمال می‌شود و از ورود داده‌های نامعتبر جلوگیری می‌کند.

11. **اجرای SQL خام با `RunSQL` در Migration**  
    یک فایل Migration خالی با `python manage.py makemigrations shop --empty` می‌سازیم. در آن، یک Stored Procedure ساده با `RunSQL` تعریف می‌کنیم که کتاب‌های پرفروش را برمی‌گرداند:
    ```python
    operations = [
        RunSQL(
            "CREATE OR REPLACE FUNCTION get_bestsellers(limit INT) "
            "RETURNS TABLE(id INT, title VARCHAR) AS $$ "
            "BEGIN "
            "  RETURN QUERY SELECT b.id, b.title FROM shop_book b "
            "  ORDER BY b.sold_count DESC LIMIT limit; "
            "END; "
            "$$ LANGUAGE plpgsql;",
            reverse_sql="DROP FUNCTION IF EXISTS get_bestsellers(INT);"
        ),
    ]
    ```

12. **بررسی کارایی با `EXPLAIN ANALYZE`**  
    در `dbshell`، یک کوئری پیچیده مثل `SELECT * FROM shop_book WHERE price > 100000 ORDER BY published_date DESC;` را با `EXPLAIN ANALYZE` اجرا می‌کنیم. خروجی را تحلیل می‌کنیم: `Seq Scan` نشان‌دهنده Full Table Scan است، `Index Scan` نشان‌دهنده استفاده از ایندکس است. اگر `Seq Scan` دیدیم، ایندکس مناسب اضافه می‌کنیم.

13. **بهینه‌سازی کوئری‌های کند با `connection.queries`**  
    در Django، با `from django.db import connection` و `print(connection.queries)` می‌توانیم همه کوئری‌های اجراشده در یک درخواست را ببینیم. یک ویو داریم که کتاب‌های یک نویسنده را با `prefetch_related` یا `select_related` می‌گیرد. تعداد کوئری‌ها را قبل و بعد از بهینه‌سازی مقایسه می‌کنیم. با `EXPLAIN ANALYZE` روی آن‌ها، تأثیر `select_related` را می‌بینیم.

14. **تنظیم Timezone و Encoding در PostgreSQL**  
    در `settings.py`، `TIME_ZONE = 'Asia/Tehran'` و `USE_TZ = True` را تنظیم می‌کنیم. در PostgreSQL، تایم‌zone دیتابیس را با `SHOW timezone;` بررسی می‌کنیم. Encoding را با `SHOW server_encoding;` بررسی می‌کنیم (باید `UTF8` باشد). اگر نیاز به تغییر است، دیتابیس را با Encoding مناسب می‌سازیم: `CREATE DATABASE bookstore WITH ENCODING 'UTF8' LC_COLLATE 'fa_IR.UTF-8';`.

15. **پشتیبان‌گیری و بازیابی دیتابیس**  
    با `pg_dump -U bookstore_user bookstore > backup.sql` از دیتابیس پشتیبان می‌گیریم. برای بازیابی از `psql -U bookstore_user -d bookstore_new < backup.sql` استفاده می‌کنیم. این فرآیند را به‌عنوان یک task دوره‌ای (با cron) تنظیم می‌کنیم و فایل پشتیبان را فشرده می‌کنیم: `pg_dump ... | gzip > backup_$(date +%Y%m%d).sql.gz`.