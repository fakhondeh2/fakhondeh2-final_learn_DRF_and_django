## سرفصل: احراز هویت مبتنی بر Session

### منابع آموزشی

**مستندات رسمی Django REST Framework:**
- [Authentication — مرجع کامل انواع احراز هویت شامل SessionAuthentication و نحوه تنظیم `DEFAULT_AUTHENTICATION_CLASSES`](https://www.django-rest-framework.org/api-guide/authentication/)
- [SessionAuthentication — جزئیات رفتار CSRF و کارکرد این backend در DRF](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication)

**مستندات رسمی Django:**
- [Authentication System — ورود و خروج کاربر، session framework و میدلورهای درگیر](https://docs.djangoproject.com/en/stable/topics/auth/)
- [CSRF Protection — نحوه کار توکن CSRF و `ensure_csrf_cookie`](https://docs.djangoproject.com/en/stable/ref/csrf/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. بخش اعظم فروشگاه در مرورگر استفاده می‌شود و مدیر فروشگاه می‌خواهد از همان سیستم کاربری Django (پنل ادمین و کوکی‌ها) برای ورود به API هم استفاده کند. حالا می‌خواهیم ورود مبتنی بر Session را برای API فعال کنیم، ویوهای ورود/خروج بسازیم و موضوع «بصری» آن یعنی CSRF را از نزدیک بررسی کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت Session Authentication و تفاوت آن با Token**  
   در این روش، کاربر مثل پنل ادمین وارد می‌شود و Django یک session روی سرور ذخیره می‌کند؛ سپس یک کوکی به نام `sessionid` در مرورگر کاربر قرار می‌گیرد. هر درخواست بعدی با این کوکی می‌آید و سرور با نگاه به `session` می‌فهمد چه کسی است. در مقابل، در روش Token، یک رشته توکن مستقل از session به کلاینت داده می‌شود. Session با stateful بودن و Token با stateless بودن شناخته می‌شود.

2. **افزودن `SessionAuthentication` به تنظیمات**  
   در `REST_FRAMEWORK`، مقدار `DEFAULT_AUTHENTICATION_CLASSES` را تنظیم می‌کنیم تا حتماً شامل `rest_framework.authentication.SessionAuthentication` باشد: `['rest_framework.authentication.SessionAuthentication', 'rest_framework.authentication.BasicAuthentication']`. حالا DRF هر درخواست را با session کاربر بررسی می‌کند.

3. **درک رفتار CSRF در `SessionAuthentication`**  
   نکته مهم: وقتی کاربر از طریق session احراز هویت می‌شود، درخواست‌های `POST`، `PUT`، `PATCH` و `DELETE` باید توکن CSRF هم داشته باشند. DRF برای جابجایی با Browsable API به‌صورت ضمنی `csrf_exempt` نمی‌کند؛ بلکه این backend است که حالت عدم اعمال را مدیریت می‌کند و فقط وقتی `csrf_exempt` بودن لازم است که احراز هویت کامل نباشد. برای درخواست‌های واقعی مرورگر، توکن CSRF باید ارسال شود.

4. **ساخت ویو ورود (`login`) برای API**  
   یک ویو `LoginView` می‌نویسیم که فرم با `username` و `password` دریافت می‌کند، با `django.contrib.auth.authenticate` کاربر را اعتبارسنجی می‌کند و با `django.contrib.auth.login` وارد می‌کند. اگر موفق بود پیام «ورود موفق» و اگر ناموفق بود خطای `400 Bad Request` برمی‌گردانیم. این ویو را با `@api_view` یا از جنس `APIView` می‌سازیم.

5. **ساخت ویو خروج (`logout`)**  
   ویو `LogoutView` می‌سازیم که با `django.contrib.auth.logout` جلسه را پایان دهد. در DRF، logout با `@api_view(['POST'])` تعریف می‌کنیم (نه GET) تا از الگوی CSRF و idioms استفاده کنیم. بعد از خروج، کوکی `sessionid` بی‌اعتبار می‌شود و دسترسی به endpointهای محافظت‌شده دیگر ممکن نیست.

6. **افزودن مسیرها به `urls.py`**  
   به `urlpatterns` دو مسیر `api/auth/login/` و `api/auth/logout/` اضافه می‌کنیم که به ویوهای ساخته‌شده وصل می‌شوند. برای تست راحت‌تر، لیست کتاب‌ها را موقتاً با `IsAuthenticated` محافظت می‌کنیم تا قبل و بعد از ورود تفاوت را ببینیم.

7. **تست ورود از طریق Browsable API**  
   در مرورگر آدرس `/api/books/` را باز می‌کنیم. DRF بالای صفحه دکمه «Log in» را نشان می‌دهد که به صفحه لاگین Django می‌رود. بعد از وارد کردن اعتبارنامه، به سمت API برمی‌گردیم و حالا درخواست‌های POST هم مجاز می‌شوند. این یکپارچگی با پنل ادمین مهم‌ترین مزیت Session Authentication است.

8. **بررسی کوکی `sessionid` و رفتار بدون ورود**  
   با ابزار توسعه‌دهنده مرورگر، کوکی `sessionid` را بعد از ورود می‌بینیم. سپس از یک پنجره ناشناس (یا با logout) درخواست یک endpoint محافظت‌شده می‌دهیم و پاسخ `403 Forbidden` را می‌بینیم چون `SessionAuthentication` بدون session، کاربر را anonymous در نظر می‌گیرد و باید `IsAuthenticated` هم فعال باشد تا `401` بدهد.

9. **گرفتن توکن CSRF با `ensure_csrf_cookie`**  
   برای کلاینتی که SPA است (مثل React یا Vue)، به توکن CSRF نیاز داریم. یک ویو ساده می‌سازیم که دکوراتور `@ensure_csrf_cookie` دارد تا در اولین بازدید، DRF کوکی `csrftoken` را ست کند. سپس کلاینت مقدار این کوکی را می‌خواند و در هدر `X-CSRFToken` درخواست‌های بعدی می‌فرستد.

10. **ارسال درخواست ورود با curl و مدیریت کوکی و CSRF**  
    با curl سناریوی کامل را اجرا می‌کنیم:
    - `curl -c cookies.txt http://localhost:8000/api/auth/login/` → دریافت کوکی `csrftoken`
    - `curl -b cookies.txt -c cookies.txt -H "X-CSRFToken: <token>" -d "username=ali&password=secret" http://localhost:8000/api/auth/login/` → ورود و دریافت `sessionid`
    - `curl -b cookies.txt http://localhost:8000/api/books/` → دسترسی با session
    این تمرین نشان می‌دهد توکن CSRF دقیقاً کجا و چطور استفاده می‌شود.

11. **ترکیب `SessionAuthentication` با Permissions**  
    برای اینکه احراز هویت به تنهایی درخواست را مجاز نکند، `permission_classes = [IsAuthenticated]` را روی ویوها تنظیم می‌کنیم. حالا بدون ورود `401 Unauthorized` و بعد از ورود `200 OK` می‌گیریم. در بعضی ویوها مثل لیست کتاب‌ها، `IsAuthenticatedOrReadOnly` می‌گذاریم تا مشاهده عمومی باشد ولی تغییر فقط با ورود ممکن شود.

12. **محدود کردن `SessionAuthentication` به ویوهای خاص**  
    اگر فقط بعضی قسمت‌ها (مثلاً پنل مدیریت فروشگاه) باید با session کار کنند و بقیه API با JWT یا Token، به‌جای تنظیم سراسری، در همان ویوهای خاص `authentication_classes = [SessionAuthentication]` را تنظیم می‌کنیم. به این ترتیب می‌توان چند مکانیزم را در یک پروژه کنار هم داشت.

13. **بررسی مزایا و معایب Session Authentication**  
    مزایا: یکپارچگی کامل با پنل ادمین Django، سادگی برای پیلوت وب، قابلیت logout از سمت سرور (اعتبارسنجی فوری)، و امنیت خوب با کوکی `HttpOnly`. معایب: stateful است و برای Scaling افقی به shared session store نیاز دارد، برای موبایل/کلاینت‌های غیرمرورگری مناسب نیست، نیازمند مدیریت CSRF است و stateless بودن REST را نقض می‌کند.

14. **تست کامل با `APIClient` در Django Test**  
    در فایل `tests.py` با `APIClient` تست می‌نویسیم. `client.login(username='ali', password='secret')` session را شبیه‌سازی می‌کند؛ سپس `GET` به یک endpoint محافظت‌شده `200` و بعد از `client.logout()` همان درخواست `401` برمی‌گرداند. همچنین تست می‌کنیم که ویو ورود با رمز غلط `400` بدهد و کوکی `sessionid` تنظیم نشود.