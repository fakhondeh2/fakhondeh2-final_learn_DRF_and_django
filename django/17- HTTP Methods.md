## سرفصل: HTTP Methods

### منابع آموزشی

**مستندات رسمی و مقالات مرجع:**
- [MDN – HTTP Request Methods — مرجع کامل تمام متدهای HTTP با توضیح، مثال و جدول](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [RFC 7231 — مستند رسمی HTTP/1.1: Semantics and Content — تعریف GET, POST, PUT, DELETE, PATCH](https://datatracker.ietf.org/doc/html/rfc7231)
- [MDN – HTTP Messages — ساختار درخواست و پاسخ HTTP، Headers و Body](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages)

**مستندات Django REST Framework:**
- [DRF – Views — نحوه تعریف Viewها با متدهای مختلف HTTP در DRF](https://www.django-rest-framework.org/api-guide/views/)
- [DRF – Generic Views — Viewهای از پیش‌ساخته برای GET, POST, PUT, PATCH, DELETE](https://www.django-rest-framework.org/api-guide/generic-views/)

**آموزش‌های تکمیلی:**
- [REST API Tutorial – HTTP Methods — بررسی Idempotency و Safe Methods با مثال](https://restfulapi.net/http-methods/)
- [HTTP Status Codes — لیست کامل کدهای وضعیت HTTP](https://httpstatuses.io/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` و اپلیکیشن «کتابخانه دیجیتال» که طراحی کردیم، حالا HTTP Methodهای مختلف را با ابزار `curl` و `httpie` آزمایش می‌کنیم. هدف این است که تفاوت GET, POST, PUT, PATCH و DELETE را در عمل ببینیم، خاصیت Idempotency را بررسی کنیم و ساختار درخواست/پاسخ را با هدرها و بدنه تحلیل کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت HTTP Methodهای اصلی و کاربرد هر کدام**  
   پنج متد اصلی HTTP که در REST APIها استفاده می‌شوند عبارتند از: GET (بازیابی داده)، POST (ایجاد منبع جدید)، PUT (جایگزینی کامل منبع)، PATCH (به‌روزرسانی جزئی منبع) و DELETE (حذف منبع). هر متد یک معنای مشخص دارد و باید به همان کاربرد محدود شود. مثلاً GET نباید باعث تغییر در دیتابیس شود.

2. **مفهوم Safe Methods (متدهای ایمن)**  
   متدهای GET, HEAD, OPTIONS و TRACE «ایمن» (Safe) محسوب می‌شوند، یعنی اجرای آن‌ها هیچ اثری روی وضعیت سرور نمی‌گذارد. فرستادن صدها درخواست GET به `/api/books/` فقط داده را برمی‌گرداند و هیچ کتابی اضافه یا حذف نمی‌کند. این ویژگی به Cache کردن پاسخ‌ها کمک می‌کند.

3. **مفهوم Idempotency (خاصیت یک‌سان‌تأثیری)**  
   یک متد Idempotent است اگر چند بار اجرای متوالی آن همان اثر یک بار اجرای آن را داشته باشد. PUT و DELETE و GET و HEAD و OPTIONS و TRACE idempotent هستند. POST idempotent نیست. اگر یک POST به `/api/books/` دو بار ارسال شود، دو کتاب متفاوت ایجاد می‌شوند. اما DELETE یک کتاب مشخص، چه یک بار اجرا شود چه ده بار، نتیجه نهایی یکسان است (کتاب حذف شده است).

4. **GET — بازیابی داده با curl**  
   با GET فهرست کتاب‌ها را دریافت می‌کنیم:
   ```bash
   curl -X GET http://127.0.0.1:8000/api/books/
   ```
   پاسخ شامل HTTP Status Code 200 (OK) و یک بدنه JSON با لیست کتاب‌هاست. هدرها شامل `Content-Type: application/json` هستند. GET باید همیشه فقط داده را برگرداند و هیچ effect side نداشته باشد.

5. **POST — ایجاد منبع جدید**  
   یک کتاب جدید با POST ایجاد می‌کنیم:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/books/ \
        -H "Content-Type: application/json" \
        -d '{"title": "کتاب جدید", "author": 1, "price": 150000}'
   ```
   پاسخ 201 (Created) برمی‌گردد. هدر `Location` شامل URI منبع جدید است: `/api/books/5/`. POST idempotent نیست – اگر این دستور دو بار اجرا شود، دو کتاب با ID متفاوت ایجاد می‌شوند.

6. **PUT — جایگزینی کامل منبع**  
   با PUT یک کتاب را به‌طور کامل جایگزین می‌کنیم:
   ```bash
   curl -X PUT http://127.0.0.1:8000/api/books/1/ \
        -H "Content-Type: application/json" \
        -d '{"title": "عنوان جدید", "author": 2, "price": 200000}'
   ```
   PUT تمام فیلدهای منبع را با مقادیر جدید جایگزین می‌کند. اگر فیلدی در JSON نباشد، بسته به پیاده‌سازی یا خالی می‌شود یا خطا می‌دهد. PUT idempotent است – دو بار اجرای آن نتیجه یکسان دارد. اگر منبع وجود نداشته باشد، برخی پیاده‌سازی‌ها آن را ایجاد می‌کنند (201 Created).

7. **PATCH — به‌روزرسانی جزئی منبع**  
   با PATCH فقط یک فیلد از کتاب را تغییر می‌دهیم:
   ```bash
   curl -X PATCH http://127.0.0.1:8000/api/books/1/ \
        -H "Content-Type: application/json" \
        -d '{"price": 180000}'
   ```
   برخلاف PUT که کل منبع را جایگزین می‌کند، PATCH فقط فیلدهای داده‌شده را تغییر می‌دهد. بقیه فیلدها دست‌نخورده باقی می‌مانند. PATCH idempotent نیست مگر اینکه به‌صورت خاص پیاده‌سازی شود (مثلاً با اعمال شرطی).

8. **DELETE — حذف منبع**  
   یک کتاب را حذف می‌کنیم:
   ```bash
   curl -X DELETE http://127.0.0.1:8000/api/books/1/
   ```
   پاسخ 204 (No Content) برمی‌گردد و بدنه خالی است. DELETE idempotent است – بار اول کتاب حذف می‌شود (204)، بار دوم و بعد چون کتاب وجود ندارد، 404 (Not Found) برمی‌گردد، اما وضعیت نهایی یکسان است (کتاب وجود ندارد).

9. **تست Idempotency PUT — اجرای متوالی یک PUT**  
   PUT را دو بار پشت سر هم اجرا می‌کنیم:
   ```bash
   curl -X PUT http://127.0.0.1:8000/api/books/2/ \
        -H "Content-Type: application/json" \
        -d '{"title": "کتاب ثابت", "author": 1, "price": 100000}'
   curl -X PUT http://127.0.0.1:8000/api/books/2/ \
        -H "Content-Type: application/json" \
        -d '{"title": "کتاب ثابت", "author": 1, "price": 100000}'
   ```
   هر دو بار کتاب شماره ۲ را به همان مقادیر تنظیم می‌کند. بعد از اجرای دوم، کتاب دقیقاً همان وضعیت بار اول را دارد. این یعنی PUT idempotent است.

10. **تست Non-Idempotency POST — اجرای متوالی یک POST**  
    POST را دو بار اجرا می‌کنیم:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/books/ \
         -H "Content-Type: application/json" \
         -d '{"title": "کتاب تکراری", "author": 1, "price": 50000}'
    curl -X POST http://127.0.0.1:8000/api/books/ \
         -H "Content-Type: application/json" \
         -d '{"title": "کتاب تکراری", "author": 1, "price": 50000}'
    ```
    دو کتاب با IDهای متفاوت (مثلاً ۱۰ و ۱۱) اما با محتوای یکسان ایجاد می‌شوند. این یعنی POST idempotent نیست. برای جلوگیری از ایجاد داده تکراری باید در سرور از شناسه‌های یکتا یا Idempotency-Key استفاده کرد.

11. **بررسی کدهای وضعیت HTTP برای هر متد**  
    هر متد HTTP کد وضعیت متفاوتی برمی‌گرداند:
    | Method | Success Code | Error Codes |
    |--------|-------------|-------------|
    | GET | 200 OK | 404 Not Found, 400 Bad Request |
    | POST | 201 Created | 400 Bad Request, 409 Conflict |
    | PUT | 200 OK یا 201 Created | 400 Bad Request, 404 Not Found |
    | PATCH | 200 OK | 400 Bad Request, 404 Not Found |
    | DELETE | 204 No Content | 404 Not Found |
    
    با `curl -v` هدرها و کد وضعیت را مشاهده می‌کنیم:
    ```bash
    curl -v -X DELETE http://127.0.0.1:8000/api/books/999/
    ```
    که 404 Not Found برمی‌گرداند چون کتاب با ID 999 وجود ندارد.

12. **تحلیل ساختار Request و Response Headers**  
    در `curl -v` خروجی کامل هدرها را می‌بینیم:
    ```
    > GET /api/books/ HTTP/1.1
    > Host: 127.0.0.1:8000
    > User-Agent: curl/8.2.1
    > Accept: */*
    
    < HTTP/1.1 200 OK
    < Content-Type: application/json
    < Content-Length: 345
    < Date: Thu, 10 Oct 2026 12:00:00 GMT
    < Server: WSGIServer/0.2
    ```
    درخواست شامل Method, URI, Headers و گاهی Body است. پاسخ شامل Status Line, Headers و Body است. Headers مثل `Content-Type` (فرمت داده)، `Content-Length` (اندازه بدنه) و `Date` (زمان سرور) اطلاعات حیاتی برای پردازش پیام هستند.

13. **طراحی Endpoint با Method Mapping صحیح**  
    در Django REST Framework، هر ViewSet می‌تواند چندین متد را پشتیبانی کند. جدول زیر mapping صحیح را نشان می‌دهد:
    | Action در ViewSet | HTTP Method | Endpoint مثال |
    |------------------|-------------|---------------|
    | `list` | GET | `/api/books/` |
    | `create` | POST | `/api/books/` |
    | `retrieve` | GET | `/api/books/1/` |
    | `update` | PUT | `/api/books/1/` |
    | `partial_update` | PATCH | `/api/books/1/` |
    | `destroy` | DELETE | `/api/books/1/` |
    
    یک ViewSet در DRF به این صورت تعریف می‌شود:
    ```python
    class BookViewSet(viewsets.ModelViewSet):
        queryset = Book.objects.all()
        serializer_class = BookSerializer
    ```
    این ViewSet به‌طور خودکار GET, POST, PUT, PATCH و DELETE را روی endpointهای مناسب پشتیبانی می‌کند.

14. **مقایسه عملی PUT و PATCH در Shell**  
    در `python manage.py shell` با استفاده از DRF's test client تفاوت PUT و PATCH را بررسی می‌کنیم:
    ```python
    from rest_framework.test import APIRequestFactory
    factory = APIRequestFactory()

    # PUT: باید تمام فیلدها را بفرستیم
    put_request = factory.put('/api/books/1/', {
        'title': 'کتاب کامل', 'author': 1, 'price': 300000
    }, format='json')

    # PATCH: فقط فیلدهای تغییر کرده را می‌فرستیم
    patch_request = factory.patch('/api/books/1/', {
        'price': 250000
    }, format='json')
    ```
    PUT مقدار `price` را به ۳۰۰۰۰۰ تغییر می‌دهد و اگر `title` و `author` را نفرستاده بودیم، احتمالاً آن‌ها را خالی می‌کرد. PATCH فقط `price` را به ۲۵۰۰۰۰ تغییر می‌دهد و بقیه فیلدها دست‌نخورده می‌مانند.

15. **بررسی Response Codes برای حالات خاص**  
    حالت‌های مختلف را با curl تست می‌کنیم:
    ```bash
    # درخواست GET به منبع نامعتبر → 404
    curl -X GET http://127.0.0.1:8000/api/books/invalid/

    # درخواست POST با داده ناقص → 400
    curl -X POST http://127.0.0.1:8000/api/books/ \
         -H "Content-Type: application/json" \
         -d '{}'

    # درخواست DELETE روی منبع حذف‌شده → 404
    curl -X DELETE http://127.0.0.1:8000/api/books/1/
    curl -X DELETE http://127.0.0.1:8000/api/books/1/

    # درخواست PUT روی منبع جدید → 201 (در برخی پیاده‌سازی‌ها)
    curl -X PUT http://127.0.0.1:8000/api/books/999/ \
         -H "Content-Type: application/json" \
         -d '{"title": "upsert", "author": 1, "price": 100}'
    ```
    تحلیل می‌کنیم که کدام کدها برای کدام سناریوها مناسب هستند و چرا.