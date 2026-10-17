## سرفصل: Signals

### منابع آموزشی

**مستندات رسمی Django:**
- [Signals — مرجع کامل سیستم Signals، نحوه تعریف، اتصال و ارسال سیگنال‌ها](https://django.readthedocs.io/en/5.2.x/topics/signals/index.html)
- [Built-in Signals — سیگنال‌های پیش‌ساخته Django شامل pre_save، post_save، pre_delete و post_delete](https://django.readthedocs.io/en/5.2.x/ref/signals.html)

**مستندات رسمی DRF:**
- [Django Signals در مستندات DRF — یکپارچه‌سازی Signalها با Serializerها و ویوها](https://www.django-rest-framework.org/community/tutorials/)

---
### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. می‌خواهیم از Signalهای Django برای انجام خودکار کارهای جانبی مثل لاگ‌گیری هنگام ایجاد کتاب، پاک‌سازی فایل‌ها هنگام حذف، و ارسال اعلان هنگام ثبت سفارش استفاده کنیم. همچنین یک Signal سفارشی برای رویدادهای تجاری (ثبت سفارش) می‌سازیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت Signal و نقش آن در Django**  
   Signal یک الگوی Observer است که به بخش‌های مختلف برنامه اجازه می‌دهد وقتی یک رویداد در جای دیگر رخ می‌دهد، مطلع شوند. مثلاً وقتی یک مدل ذخیره می‌شود (`post_save`)، می‌توانیم کاری مثل ارسال ایمیل یا پاک کردن کش انجام دهیم. Signalها کد را از مدل‌ها و ویوها جدا نگه می‌دارند و انسجام کد را بالا می‌برند.

2. **ساخت Receiver با دکوراتور `@receiver` برای `post_save` مدل `Book`**  
   یک فایل جدید `shop/signals.py` می‌سازیم. در آن یک تابع به نام `log_book_creation` تعریف می‌کنیم و با دکوراتور `@receiver(post_save, sender=Book)` آن را به Signal `post_save` متصل می‌کنیم. داخل تابع، اگر `created` برابر `True` بود، یک پیام لاگ می‌نویسیم: `logger.info(f"Book '{instance.title}' created with id {instance.pk}")`. این تابع هر بار که یک کتاب جدید ساخته می‌شود، پیام لاگ ثبت می‌کند.

3. **ثبت Signal در پیکربندی اپ (`ready()` در `apps.py`)**  
   برای اینکه Signalها بارگذاری شوند، باید آن‌ها را در متد `ready()` کلاس `AppsConfig` ایمپورت کنیم. در `shop/apps.py`، متد `ready()` را override می‌کنیم و در آن می‌نویسیم `from . import signals`. این کار ensures می‌کند که وقتی اپ راه‌اندازی می‌شود، Signalها ثبت شوند.

4. **ساخت Receiver با `connect()` به‌جای دکوراتور**  
   روش دیگر برای اتصال Receiver، استفاده از متد `connect()` روی Signal است. در `signals.py`، یک تابع `handle_book_delete` تعریف می‌کنیم و آن را با `post_delete.connect(handle_book_delete, sender=Book)` وصل می‌کنیم. این روش برای موقعیت‌هایی مفید است که می‌خواهیم Receiver را به‌صورت شرطی و داینامیک وصل کنیم.

5. **پیاده‌سازی `pre_delete` برای پاک‌سازی فایل‌ها**  
   در Receiver `pre_delete` برای مدل `Book`، قبل از حذف کتاب، چک می‌کنیم که آیا فیلد `cover_image` (یا هر فیلد `ImageField` / `FileField`) مقدار دارد یا نه. اگر دارد، خودکار فایل مربوطه را از دیسک حذف می‌کنیم تا فایل‌های بی‌استفاده روی سرور باقی نمانند. برای این کار از `instance.cover_image.path` و `os.remove()` استفاده می‌کنیم.

6. **بررسی شیء `instance` و وضعیت `created` در `post_save`**  
   Signal `post_save` سه آرگومان مهم دارد: `sender` (کلاس مدل)، `instance` (نمونه ذخیره‌شده) و `created` (بولی که نشان می‌دهد این ثبت جدید است یا به‌روزرسانی). در یک Receiver، بررسی می‌کنیم که اگر `created` است، یک اقدام انجام دهیم (مثلاً ایمیل خوش‌آمدگویی) و اگر `created` نیست (به‌روزرسانی)، اقدام دیگری (مثلاً به‌روزرسانی ایندکس جستجو).

7. **ساخت یک Signal سفارشی با `Signal` کلاس**  
   در `shop/signals.py` یک Signal سفارشی به نام `order_placed = Signal()` تعریف می‌کنیم. این Signal هیچ `sender` پیش‌فرضی ندارد. هدف این است که وقتی یک سفارش جدید ثبت می‌شود (در ویو سفارش)، این Signal را صدا بزنیم تا کارهای جانبی مثل ارسال ایمیل تأیید، به‌روزرسانی موجودی و لاگ‌گیری انجام شوند.

8. **ارسال Signal سفارشی با `send()`**  
   در یک ویو یا سرویس، بعد از ثبت سفارش، Signal را با `order_placed.send(sender=Order, order=order, user=request.user)` ارسال می‌کنیم. متد `send()` یک لیست از tupleهای `(receiver, response)` برمی‌گرداند. آرگومان‌های اضافی (`order` و `user`) به Receiverها پاس داده می‌شوند.

9. **ساخت Receiver برای Signal سفارشی `order_placed`**  
   برای `order_placed` سه Receiver می‌سازیم:
   - `send_order_confirmation_email`: یک ایمیل تأیید برای کاربر ارسال می‌کند.
   - `update_inventory`: موجودی کتاب‌های سفارش‌داده‌شده را کاهش می‌دهد.
   - `log_order`: جزئیات سفارش را در دیتابیس یا فایل لاگ ثبت می‌کند.

10. **اتصال و قطع اتصال داینامیک Signalها**  
    گاهی نیاز داریم Receiver را موقتاً غیرفعال کنیم. با `post_save.disconnect(receiver, sender=Book)` می‌توانیم یک Receiver را قطع کنیم. بعداً با `post_save.connect(receiver, sender=Book)` دوباره وصل می‌کنیم. این کار در تست‌ها و سناریوهای bulk import مفید است، جایی که نمی‌خواهیم Signalها اجرا شوند.

11. **استفاده از `m2m_changed` برای روابط ManyToMany**  
    Signal `m2m_changed` وقتی فعال می‌شود که یک رابطه ManyToMany تغییر کند. مثلاً در مدل `Book` یک فیلد `categories` از نوع `ManyToManyField` داریم. با `@receiver(m2m_changed, sender=Book.categories.through)` هر بار که دسته‌بندی کتاب تغییر می‌کند، می‌توانیم کش مربوطه را بی‌اعتبار کنیم.

12. **محدود کردن Signal به یک مدل خاص با پارامتر `sender`**  
    اگر Receiver را بدون `sender` تعریف کنیم، برای ALL مدل‌ها صدا زده می‌شود. بهتر است همیشه `sender` را مشخص کنیم. در `signals.py` یک Receiver عمومی `post_save` می‌سازیم که `sender=None` دارد، لاگ می‌گیرد و در توضیح می‌گوییم که این فقط برای آزمایش است، برای محیط تولید باید روی مدل خاص محدود شود.

13. **تست Signalها با `django.test.TestCase`**  
    یک فایل `shop/tests/test_signals.py` می‌سازیم. در یک تست، یک `Book` جدید ایجاد می‌کنیم و با `self.assertEqual(len(mail.outbox), 1)` بررسی می‌کنیم که Signal `order_placed` ایمیل ارسال کرده است. همچنین با Mock کردن Receiverها، می‌توانیم تست کنیم که Signalها درست وصل شده‌اند.

14. **استفاده از `django.dispatch.disconnect` برای جلوگیری از حلقه بی‌نهایت**  
    اگر یک `post_save` Signal خودش مدل را دوباره ذخیره کند (مثلاً آپدیت یک فیلد)، باعث فراخوانی مجدد Signal و حلقه بی‌نهایت می‌شود. راه حل: Receiver را با `post_save.disconnect()` قطع کنیم، تغییر را اعمال کنیم، و دوباره وصل کنیم. این سناریو را پیاده‌سازی می‌کنیم و تست می‌کنیم.

15. **بررسی کارایی Signalها و avoid overuse**  
    Signalها ابزار قدرتمندی هستند، اما استفاده بی‌رویه از آن‌ها کد را غیرقابل پیش‌بینی می‌کند (اثر جانبی پنهان). یک اصل مهم: هر Signal باید یک کار خاص و مشخص انجام دهد. Signalها را مستند کنیم و در `signals.py` با کامنت توضیح دهیم که هر Receiver چه کاری انجام می‌دهد و چه مدلی آن را فعال می‌کند.