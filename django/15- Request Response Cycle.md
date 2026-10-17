## سرفصل: چرخه‌ی درخواست و پاسخ (Request-Response Cycle)

### منابع آموزشی

**مستندات رسمی Django:**
- [Request and response objects — مرجع کامل HttpRequest و HttpResponse](https://docs.djangoproject.com/en/5.2/ref/request-response/)
- [Middleware — مرجع کامل میدلورها و ترتیب اجرا](https://docs.djangoproject.com/en/5.2/topics/http/middleware/)

**راهنماهای استقرار:**
- [WSGI — راهنمای استقرار با Gunicorn و WSGI](https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/)
- [ASGI — راهنمای استقرار با Uvicorn/Daphne و async](https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه‌ی `mysite` اپلیکیشن «فروشگاه کتاب» (shop) را داریم. در این تمرین سفر یک درخواست را از لحظه‌ی ورود به سرور تا رسیدن پاسخ به مرورگر دنبال می‌کنیم، میدلورهای سفارشی می‌سازیم و با WSGI و ASGI آشنا می‌شویم. هدف این است که بدانیم وقتی کاربر آدرسی را باز می‌کند، در پشت صفحه دقیقاً چه اتفاقی می‌افتد — این دانش برای دیباگ و بهینه‌سازی حیاتی است.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت چرخه‌ی کامل و لایه‌های آن**  
   مسیر یک درخواست به این شکل است:
   
   `درخواست مرورگر → سرور WSGI/ASGI → میدلورها (فاز درخواست) → URL resolver → ویو → رندر تمپلیت/پاسخ → میدلورها (فاز پاسخ) → مرورگر`
   
   هر لایه فقط یک مسئولیت دارد و خروجی لایه‌ی قبلی، ورودی لایه‌ی بعدی است. این تصویر ذهنی، نیمی از راه است.

2. **نقطه‌ی ورود: WSGI و ASGI**  
   سرور توسعه (`runserver`) و سرورهای عملیاتی، Django را از طریق `wsgi.py` (همگام) یا `asgi.py` (ناهمگام) صدا می‌زنند. در `wsgi.py` این اپ ساخته می‌شود:
   ```python
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
   درخواستِ رسیده با قواعد WSGI به یک `environ` تبدیل می‌شود و Django از آن شیء `request` می‌سازد.

3. **فهرست MIDDLEWARE و ترتیب آن**  
   در `settings.py` لیست `MIDDLEWARE` را باز کنید. ترتیب مهم است: هنگام ورود، میدلورها از بالا به پایین اجرا می‌شوند و هنگام خروج پاسخ، از پایین به بالا. مثلاً `SecurityMiddleware`، `SessionMiddleware` و `CsrfViewMiddleware` را به همین ترتیب قرار داده‌اند.

4. **ساخت اولین میدلور سفارشی**  
   یک میدلور در سبک مدرن، تابع یا کلاسی است که یک «گام بعدی» (`get_response`) می‌گیرد:
   ```python
   class MyMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           # فاز درخواست
           response = self.get_response(request)  # اجرای بقیه‌ی زنجیره و ویو
           # فاز پاسخ
           return response
   ```
   هر کاری که قبل از `get_response` بنویسیم، در ورود؛ و هر کاری بعد از آن، در خروج اجرا می‌شود. سپس میدلور را در `MIDDLEWARE` ثبت می‌کنیم.

5. **فاز درخواست: تغییر درخواست در میدلور**  
   در فاز ورود می‌توانیم به `request` جزئیات اضافه کنیم تا همه‌ی ویوها از آن استفاده کنند. مثلاً ثبت محدوده‌ی IP یا اتصال یک attribute به درخواست:
   ```python
   def __call__(self, request):
       request.client_ip = request.META.get('REMOTE_ADDR')
       return self.get_response(request)
   ```
   حالا در هر ویو به `request.client_ip` دسترسی داریم.

6. **توزیع درخواست: URL resolution و فراخوانی ویو**  
   بعد از میدلورها، Django آدرس را با `urlpatterns` تطبیق می‌دهد (`resolve`)، ویو و پارامترها را پیدا می‌کند و ویو را صدا می‌زند. در FBV یعنی فراخوانی تابع، و در CBV یعنی `as_view()` که متد مناسب (مثل `get` یا `post`) را بر اساس `request.method` انتخاب می‌کند.

7. **رندر تمپلیت و تولید پاسخ**  
   اگر ویو از `render` استفاده کند، `Template` بارگذاری می‌شود و با context ترکیب و یک `HttpResponse` ساخته می‌شود:
   ```python
   response = render(request, 'shop/book_list.html', {'books': books})
   ```
   در این لحظه پاسخ، یک شیء پایتونی است با header و content. اجرای تمپلیت، آخرین بخش «تولید محتوا»ست.

8. **فاز پاسخ: اجرای میدلورها به‌صورت معکوس**  
   پاسخِ ساخته‌شده حالا از پایین `MIDDLEWARE` به بالا از همه‌ی میدلورها رد می‌شود. برای اثبات این موضوع، در میدلور خود بعد از `get_response` یک `print` بگذارید و ببینید چه زمانی نسبت به آغاز درخواست اجرا می‌شود. به این ساختار «پیاز» می‌گویند: درخواست از لایه‌ها رد می‌شود داخل می‌رود و پاسخ از همان جاده برمی‌گردد.

9. **افزودن هدر به همه‌ی پاسخ‌ها در میدلور**  
   یک کاربرد رایج میدلور، افزودن هدر امنیتی یا تحلیلی به همه‌ی پاسخ‌هاست:
   ```python
   def __call__(self, request):
       response = self.get_response(request)
       response['X-App-Version'] = '1.0.0'
       response['X-Frame-Options'] = 'DENY'
       return response
   ```
   هدرها را در بخش Network مرورگر ببینید. بعضی از همین هدرها را میدلورهای پیش‌فرض Django اضافه می‌کنند.

10. **مدیریت استثناها در میدلور با `process_exception`**  
    در سبک کلاسی، می‌توان متد `process_exception` را تعریف کرد که اگر در درخواست خطایی بیفتد، اجرا شود:
    ```python
    def process_exception(self, request, exception):
        return HttpResponse('خطایی رخ داد', status=500)
    ```
    اینجاست که میدلور می‌تواند خطا را ثبت (log) کند، پیام بهتری برگرداند یا آن را به سرویس رهگیری خطا بفرستد.

11. **WSGI در برابر ASGI و ویوهای async**  
    WSGI برای درخواست‌های همگام (sync) است و برای هر درخواست یک فراخوانی ساده انجام می‌دهد. ASGI از async پشتیبانی می‌کند، یعنی Django می‌تواند درخواست را در حالی که منتظر I/O است رها کند و کار دیگری بکند. برای تعریف ویوی async:
    ```python
    async def my_view(request):
        data = await fetch_something()
        return HttpResponse(data)
    ```
    تفاوت عملی این دو با یک تست درخواست‌های هم‌زمان مشخص می‌شود.

12. **میدلور زمان‌سنج (Timing Middleware)**  
    برای دیدن زمان واقعی چرخه، یک میدلور می‌سازیم که مدت اجرا را اندازه بگیرد:
    ```python
    import time

    class TimingMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            start = time.time()
            response = self.get_response(request)
            response['X-Request-Duration'] = f'{time.time() - start:.3f}'
            return response
    ```
    حالا با چند درخواست، مقدار `X-Request-Duration` را مقایسه کنید؛ یک ابزار ساده و کاربردی برای پایش اولیه‌ی عملکرد.

13. **لاگ‌کردن چرخه**  
    بهتر است هر درخواست را با جزئیات ثبت کنیم. با logging استاندارد پایتون:
    ```python
    import logging
    logger = logging.getLogger(__name__)

    def __call__(self, request):
        logger.info(f'{request.method} {request.path} — {request.user}')
        response = self.get_response(request)
        logger.info(f'status={response.status_code}')
        return response
    ```
    حالا در کنسول توسعه، مسیر هر درخواست و وضعیت پاسخ را می‌بینید و چرخه به چشم می‌آید.

14. **پاسخ‌های خطای سراسری: handler404 و handler500**  
    در پایان چرخه، اگر هیچ الگویی تطبیق نخورد، Django به `handler404` پناه می‌برد و اگر ویو خطای غیرقابل‌کنترل بدهد، `handler500`. هر دو را در `mysite/urls.py` به ویوهای سفارشی وصل کنید و یک خطای آزمایشی در یک ویو بسازید، سپس ببینید پاسخ نهایی از میدلورها و handlerها چطور ساخته می‌شود.

15. **رسم نمودار چرخه برای فروشگاه**  
    در نهایت، برای صفحه‌ی `books/` فروشگاه، کامل‌ترین مسیر ممکن را بنویسید:
    
    `GET /shop/books/ → ASGI/WSGI → میدلورها (فاز ورود) → resolve → BookListView.get() → get_queryset → render('book_list.html') → HttpResponse → میدلورها (فاز خروج) → مرورگر`
    
    این نمودار را برای یک درخواست POST (مثل افزودن نظر) هم بنویسید و تفاوت مسیر را مشخص کنید. داشتن این تصویر، دیباگ هر مشکلی را آسان‌تر می‌کند.