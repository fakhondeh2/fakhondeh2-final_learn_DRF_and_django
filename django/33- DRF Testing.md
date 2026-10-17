## سرفصل: DRF Testing

### منابع آموزشی

**مستندات رسمی Django REST Framework:**
- [Testing — راهنمای کامل تست در DRF، APITestCase، APIClient و ابزارهای تست](https://www.django-rest-framework.org/api-guide/testing/)

**مستندات رسمی Django:**
- [Testing Django Applications — راهنمای جامع تست در Django](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [Testing Tools — ابزارهای تست Django، TestCase و Client](https://docs.djangoproject.com/en/5.2/topics/testing/tools/)

**ابزارهای مرتبط:**
- [Coverage.py — اندازه‌گیری پوشش تست](https://coverage.readthedocs.io/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. برای مدل‌های `Author`، `Book` و `Review` چندین View و ViewSet با DRF ساخته‌ایم. حالا می‌خواهیم برای همه این ViewSetها تست بنویسیم تا مطمئن شویم APIها درست کار می‌کنند. هدف این است که یاد بگیریم با `APITestCase` و `APIClient` تست‌های قابل اعتماد بنویسیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت APITestCase و تفاوت آن با TestCase استاندارد**  
   `APITestCase` در DRF یک کلاس پایه برای تست است که از `django.test.TestCase` ارث می‌برد. تفاوت اصلی آن در این است که یک `APIClient` به‌طور خودکار در دسترس قرار می‌دهد. `APIClient` بر خلاف `Client` استاندارد Django، از content negotiation پشتیبانی می‌کند و می‌تواند داده‌ها را به فرمت JSON سریالایز کند.

2. **ساختار فایل تست و Convention نام‌گذاری**  
   در اپلیکیشن `shop` یک فایل به نام `tests/` (به‌صورت پکیج) یا `tests.py` می‌سازیم. نام کلاس‌های تست معمولاً با `Test` شروع می‌شود (مثلاً `TestBookAPI`) و هر متد با `test_` شروع می‌شود. Django به‌طور خودکار متدهایی که با `test_` شروع می‌شوند را پیدا و اجرا می‌کند.

3. **نوشتن اولین تست با APITestCase**  
   یک کلاس `TestBookAPI(APITestCase)` می‌سازیم. در متد `test_get_books_list` از `self.client.get('/api/books/')` استفاده می‌کنیم و وضعیت پاسخ را با `self.assertEqual(response.status_code, 200)` بررسی می‌کنیم. همچنین محتوای پاسخ JSON را با `response.json()` بررسی می‌کنیم.

4. **استفاده از setUp برای ایجاد داده‌های تست**  
   متد `setUp` را override می‌کنیم. در آن یک نویسنده و دو کتاب ایجاد می‌کنیم تا در همه تست‌ها در دسترس باشند. با `setUpTestData` (از TransactionTestCase) می‌توانیم داده‌ها را یک بار برای کلاس ایجاد کنیم تا سرعت تست بالاتر رود. تفاوت `setUp` و `setUpTestData` را بررسی می‌کنیم.

5. **تست GET برای لیست و جزئیات**  
   دو تست می‌نویسیم: یکی برای `GET /api/books/` که لیست کتاب‌ها را برگرداند و بررسی کند که کتاب‌های ایجادشده در setUp در پاسخ موجود هستند. دومی برای `GET /api/books/{id}/` که یک کتاب خاص را برگرداند و فیلدهای آن را بررسی کند.

6. **تست POST برای ایجاد**  
   یک تست `test_create_book` می‌نویسیم که با `self.client.post('/api/books/', data, format='json')` یک کتاب جدید ایجاد کند. داده‌ها را به‌صورت دیکشنری ارسال می‌کنیم. وضعیت ۲۰۱ (Created) را تأیید می‌کنیم و بررسی می‌کنیم که کتاب جدید در دیتابیس وجود دارد.

7. **تست PUT برای به‌روزرسانی کامل**  
   یک تست `test_update_book` می‌نویسیم که یک کتاب موجود را با `self.client.put('/api/books/{id}/', data, format='json')` به‌روز کند. وضعیت ۲۰۰ را تأیید می‌کنیم و بررسی می‌کنیم که فیلد title در دیتابیس تغییر کرده است.

8. **تست DELETE برای حذف**  
   یک تست `test_delete_book` می‌نویسیم که با `self.client.delete('/api/books/{id}/')` یک کتاب را حذف کند. وضعیت ۲۰۴ (No Content) را تأیید می‌کنیم و سپس با `self.assertFalse(Book.objects.filter(id=book_id).exists())` بررسی می‌کنیم که کتاب از دیتابیس حذف شده است.

9. **تست احراز هویت با force_authenticate**  
   یک تست می‌نویسیم که برای دسترسی به یک View نیاز به احراز هویت دارد. با `self.client.force_authenticate(user=some_user)` یک کاربر را احراز هویت می‌کنیم. سپس بررسی می‌کنیم که درخواست بدون احراز هویت به ۴۰۱ (Unauthorized) و با احراز هویت به ۲۰۰ می‌رسد.

10. **تست سناریوهای مجوز (Permissions)**  
    یک کاربر عادی و یک کاربر ادمین می‌سازیم. تست می‌کنیم که کاربر عادی نمی‌تواند کتاب حذف کند (۴۰۳) اما ادمین می‌تواند. این کار با `force_authenticate(user=normal_user)` و بررسی وضعیت ۴۰۳ انجام می‌شود.

11. **استفاده از RequestFactory برای تست‌های ایزوله**  
    `RequestFactory` یک ابزار است که اشیای HttpRequest می‌سازد بدون اینکه آن‌ها را از طریق میان‌افزارها عبور دهد. این ابزار برای تست‌های واحد (unit test) که فقط یک تابع خاص View را تست می‌کنند مفید است. مثلاً `factory = RequestFactory()` و `request = factory.get('/api/books/')`. سپس View را مستقیماً صدا می‌زنیم.

12. **تست ارسال داده نامعتبر**  
    یک تست می‌نویسیم که داده‌های نامعتبر (مثلاً `price` به‌صورت رشته) به POST ارسال کند. وضعیت ۴۰۰ (Bad Request) را بررسی می‌کنیم و مطمئن می‌شویم که پاسخ شامل خطاهای اعتبارسنجی است. محتوای خطا را با `assertIn` بررسی می‌کنیم.

13. **اجرای تست‌ها و مشاهده خروجی**  
    تست‌ها را با `python manage.py test shop.tests` اجرا می‌کنیم. خروجی شامل تعداد تست‌های اجراشده و نتیجه هر کدام است. از پرچم `-v 2` برای نمایش جزئی‌تر استفاده می‌کنیم. تست‌های failed و خطاها را بررسی می‌کنیم.

14. **اندازه‌گیری پوشش تست (Coverage)**  
    با `coverage run manage.py test shop.tests` و سپس `coverage report` درصد پوشش کد را می‌بینیم. با `coverage html` یک گزارش HTML می‌سازیم و در مرورگر باز می‌کنیم. هدف می‌گذاریم که حداقل ۸۰٪ از کد Views و Serializersها تحت پوشش تست باشند.