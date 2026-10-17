> **هدف:** درک عمیق مفاهیم احراز هویت و مجوزدهی و پیاده‌سازی عملی آن‌ها در DRF.
> **ساختار:** برای هر مبحث، ابتدا یک توضیح کوتاه و سپس **۱۰ تسک عملی** ارائه شده است. پاسخ هیچ تسکی داده نشده است.

---

## ۱) Session Authentication

**مفهوم:** احراز هویت مبتنی بر کوکی که در آن سرور یک `sessionid` در کوکی مرورگر ذخیره می‌کند و وضعیت کاربر را در دیتابیس (یا کش) نگه می‌دارد.

### تسک‌ها
1. پروژه‌ای بساز که در آن endpoint ورود با `django.contrib.auth.views.LoginView` کار کند و بعد از لاگین، کوکی `sessionid` در پاسخ قابل مشاهده باشد.
2. تنظیمات `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE` را طوری پیکربندی کن که در محیط production امن باشد.
3. یک endpoint به نام `whoami` بساز که فقط برای کاربران لاگین‌شده، اطلاعات پایه‌ی کاربر را برگرداند.
4. `SessionAuthentication` را در `DEFAULT_AUTHENTICATION_CLASSES` قرار بده و بررسی کن که درخواست بدون کوکی چه کدی برمی‌گرداند.
5. یک custom backend برای احراز هویت بنویس که کاربر را با ایمیل (به‌جای username) لاگین کند.
6. endpoint خروج (`logout`) را طوری پیاده کن که session کاملاً پاک شود و کوکی منقضی گردد.
7. مدت اعتبار session را به ۳۰ دقیقه کاهش بده و رفتار sliding expiration را فعال/غیرفعال کن.
8. یک تست بنویس که ثابت کند بعد از logout، درخواست به endpoint محافظت‌شده با خطای 403 برگردد.
9. مکانیزمی پیاده کن که session کاربران غیرفعال (`is_active=False`) به‌صورت خودکار باطل شود.
10. تفاوت رفتار Session Authentication را با Basic Authentication در برابر درخواست‌های stateful و stateless مستند کن (فقط تحلیل، بدون کد اجباری).

---

## ۲) JWT (JSON Web Token)

**مفهوم:** توکن امضاشده و بدون‌وضعیت که شامل header، payload و signature است و معمولاً برای احراز هویت stateless استفاده می‌شود.

### تسک‌ها
1. با استفاده از `djangorestframework-simplejwt` endpointهای `token/` و `token/refresh/` را راه‌اندازی کن.
2. یک access token تولید کن و بخش‌های header و payload آن را با ابزار (مثل jwt.io) تحلیل و مستند کن.
3. زمان انقضای access token را به ۵ دقیقه و refresh token را به ۱ روز کاهش بده.
4. یک claim سفارشی مثل `role` یا `email` به payload اضافه کن.
5. `SIGNING_KEY` و `ALGORITHM` را در تنظیمات جدا کن و از الگوریتم HS256 به RS256 مهاجرت کن.
6. یک permission class بنویس که فقط توکن‌هایی با claim مشخص (مثلاً `is_staff=true`) را بپذیرد.
7. بررسی کن اگر توکن دستکاری شود (تغییر یک کاراکتر در signature)، چه خطایی برگردانده می‌شود.
8. توکن‌ها را در `localStorage` و در `httpOnly cookie` ذخیره کن و مزایا/معایب امنیتی هرکدام را مستند کن.
9. یک blacklist برای توکن‌های باطل‌شده راه‌اندازی کن و توکن یک کاربر را پس از logout باطل کن.
10. یک view محافظت‌شده بساز که فقط با هدر `Authorization: Bearer <token>` کار کند و در غیر این صورت 401 برگرداند.

---

## ۳) RBAC (Role-Based Access Control)

**مفهوم:** دسترسی بر اساس نقشی که به کاربر تخصیص داده می‌شود (مثل Admin، Editor، Viewer).

### تسک‌ها
1. مدل‌های `Role` و `UserRole` طراحی کن و رابطه‌ی many-to-many بین کاربر و نقش برقرار کن.
2. سه نقش `admin`, `editor`, `viewer` بساز و به هر کاربر حداقل یک نقش بده.
3. یک permission class به نام `HasRole` بنویس که لیستی از نقش‌های مجاز بگیرد.
4. endpoint مربوط به «حذف مقاله» را فقط برای نقش `admin` باز بگذار.
5. endpoint «ویرایش مقاله» را برای `admin` و `editor` باز بگذار.
6. endpoint «مشاهده مقاله» را برای همه‌ی نقش‌ها باز بگذار.
7. بررسی کن که کاربر بدون نقش، به هیچ‌کدام از endpointهای محافظت‌شده دسترسی نداشته باشد.
8. مکانیزمی پیاده کن که یک کاربر بتواند در زمان واحد فقط یک نقش فعال داشته باشد (active role).
9. یک decorator یا mixin بساز که چک کردن نقش را در سطح view ساده‌تر کند.
10. جدولی از نقش‌ها × دسترسی‌ها بساز و آن را در قالب مستندات پروژه قرار بده.

---

## ۵) Password Hashing

**مفهوم:** ذخیره‌ی امن رمز عبور با الگوریتم‌های یک‌طرفه مثل PBKDF2، Argon2، bcrypt.

### تسک‌ها
1. بررسی کن Django به‌صورت پیش‌فرض از چه الگوریتمی استفاده می‌کند (`PASSWORD_HASHERS`).
2. `Argon2` را نصب و به‌عنوان hasher پیش‌فرض تنظیم کن.
3. یک user بساز و مقدار ستون `password` را در دیتابیس بررسی کن (بدون افشای مقدار واقعی).
4. تابع `set_password` و `check_password` را جداگانه تست کن.
5. مهاجرت (rehash) کاربران قدیمی از PBKDF2 به Argon2 را با `update_session_auth_hash` پیاده کن.
6. یک validator سفارشی بنویس که رمزهای تکراری رایج (مثل `123456`) را رد کند.
7. یک validator بنویس که ترکیب حرف بزرگ، کوچک، عدد و علامت را الزامی کند.
8. بررسی کن که آیا رمز کاربران در لاگ‌ها یا پاسخ‌های API جایی افشا می‌شود یا نه.
9. یک endpoint `change-password` بساز که رمز فعلی را تأیید و سپس رمز جدید را ذخیره کند.

---

## ۶) Refreshing Token

**مفهوم:** تولید مجدد access token بدون نیاز به لاگین مجدد کاربر، با استفاده از refresh token.

### تسک‌ها
1. یک access token با عمر کوتاه (۱ دقیقه) بساز و بعد از انقضا، درخواست بفرست و خطا را ثبت کن.
2. با استفاده از refresh token، یک access token جدید بگیر.
3. بررسی کن که بعد از refresh، مقدار `jti` تغییر می‌کند یا نه.
4. rotation را فعال کن؛ یعنی هر بار refresh، یک refresh token جدید صادر شود.
5. refresh token قدیمی را blacklist کن و بررسی کن که دیگر قابل استفاده نیست.
6. یک endpoint `logout` بساز که refresh token را باطل کند.
7. مدت اعتبار refresh token را به‌صورت sliding تمدید کن (هر بار استفاده، عمر تمدید شود).
8. مکانیزمی پیاده کن که در صورت سرقت refresh token، همه‌ی توکن‌های آن کاربر باطل شوند.
9. یک تست بنویس که چرخه‌ی کامل login → access → expire → refresh → access جدید را پوشش دهد.

---

## ۷) CSRF (Cross-Site Request Forgery)

**مفهوم:** حمله‌ای که در آن سایت مهاجم از اعتبار کوکی کاربر برای ارسال درخواست ناخواسته استفاده می‌کند.

### تسک‌ها
1. یک endpoint POST با `SessionAuthentication` بساز و بدون ارسال CSRF token درخواست بفرست؛ خطا را ثبت کن.
2. CSRF token را در قالب کوکی به کلاینت بده و از کلاینت آن را در هدر `X-CSRFToken` بفرست.
3. بررسی کن که `CsrfViewMiddleware` در `MIDDLEWARE` فعال است و اثرش را مستند کن.
4. برای یک API عمومی (مثل login)، با `@csrf_exempt` معافیت ایجاد کن و دلیلش را توضیح بده.
5. تفاوت رفتار CSRF در `SessionAuthentication` و `JWTAuthentication` را تحلیل کن.
6. تنظیمات `CSRF_COOKIE_SECURE`, `CSRF_COOKIE_HTTPONLY`, `CSRF_TRUSTED_ORIGINS` را پیکربندی کن.
7. یک endpoint بساز که برای درخواست‌های `GET` نیازی به CSRF نداشته باشد اما برای `POST` داشته باشد.
8. بررسی کن که `SameSite=Lax/Strict` چه تأثیری روی CSRF دارد.
9. یک تست بنویس که ثابت کند درخواست بدون CSRF token با کد 403 رد می‌شود.

---

## ۸) CORS (Cross-Origin Resource Sharing)

> نکته: در متن سؤال «SORS» نوشته شده بود؛ منظور همان **CORS** است.

**مفهوم:** مکانیزمی در مرورگر که تعیین می‌کند کدام دامنه‌ها اجازه‌ی دسترسی به منابع سرور را دارند.

### تسک‌ها
1. `django-cors-headers` را نصب و به `INSTALLED_APPS` اضافه کن.
2. `CORS_ALLOWED_ORIGINS` را طوری تنظیم کن که فقط `http://localhost:3000` اجازه داشته باشد.
3. یک درخواست از دامنه‌ی غیرمجاز بفرست و پاسخ مرورگر را ثبت کن.
4. تفاوت `CORS_ALLOW_ALL_ORIGINS` و `CORS_ALLOWED_ORIGINS` را مستند کن.
5. `CORS_ALLOW_CREDENTIALS = True` را فعال کن و بررسی کن که چرا نمی‌توان آن را با `ALLOW_ALL_ORIGINS` ترکیب کرد.
6. هدرهای سفارشی (مثل `X-CSRFToken`) را به `CORS_ALLOW_HEADERS` اضافه کن.
7. متدهای مجاز را فقط به `GET, POST, OPTIONS` محدود کن.
8. رفتار preflight request (`OPTIONS`) را با ابزار developer tools مرورگر تحلیل کن.
9. یک middleware سفارشی بنویس که هدر `Access-Control-Allow-Origin` را شرطی اضافه کند.
10. تفاوت CORS و CSRF را در یک جدول مقایسه‌ای مستند کن (یکی مرورگری، یکی سروری).
