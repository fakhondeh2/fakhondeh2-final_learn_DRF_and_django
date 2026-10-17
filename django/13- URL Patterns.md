## سرفصل: الگوهای URL (URL Patterns)

### منابع آموزشی

**مستندات رسمی Django:**
- [URL dispatcher — بخش path converters و re_path](https://docs.djangoproject.com/en/5.2/topics/http/urls/#path-converters)
- [URL dispatcher — بخش include و namespace](https://docs.djangoproject.com/en/5.2/topics/http/urls/#including-other-urlconfs)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه‌ی `mysite` اپلیکیشن «فروشگاه کتاب» (shop) را داریم. در این تمرین الگوهای مسیر فروشگاه را حرفه‌ای‌تر می‌کنیم: از path converters مختلف (int, str, slug, uuid)، عبارت‌های منظم با `re_path`، includeهای تودرتو، namespace برای اپلیکیشن و پارامترهای اضافه استفاده می‌کنیم. هدف این است که بدانیم برای هر نوع آدرسی کدام روش مسیریابی مناسب است.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت path converters و سینتکس آن‌ها**  
   django در `path()` از جای‌گذارهای (converters) آماده استفاده می‌کند که علاوه بر گرفتن یک قطعه از مسیر، نوع داده‌اش را هم اعتبارسنجی می‌کنند. اگر آدرس با نوع تعیین‌شده تطبیق نکند، آن الگو رد می‌شود و Django به الگوی بعدی می‌رود (و در نهایت 404 می‌دهد). سینتکس کلی: `<converter:name>`.

2. **استفاده از `<int:...>` برای شناسه‌های عددی**  
   رایج‌ترین converter، `int` است که فقط عدد صحیح می‌پذیرد:
   ```python
   path('books/<int:pk>/', views.book_detail, name='book_detail'),
   ```
   آدرس `/shop/books/12/` پذیرفته می‌شود ولی `/shop/books/hello/` خیر. این یعنی ویو همیشه یک `int` واقعی دریافت می‌کند و نیازی به تبدیل دستی نداریم.

3. **استفاده از `<str:...>` برای بخش‌های متنی**  
   `str` هر رشته‌ی غیر از `/` را می‌پذیرد و مقدار را به‌صورت رشته پاس می‌دهد:
   ```python
   path('category/<str:category_name>/', views.category_books, name='category_books'),
   ```
   برای آدرس‌هایی مثل `/shop/category/fiction/` مناسب است. دقت کنید `str` مقدار را از نظر «عدد بودن» محدود نمی‌کند؛ برای همین در صورت نیاز اعتبارسنجی داخل ویو انجام می‌شود.

4. **استفاده از `<slug:...>` برای slugها**  
   converter با نام `slug` فقط رشته‌های سازگار با قالب slug (حروف، ارقام، خط تیره و زیرخط) را می‌پذیرد:
   ```python
   path('books/<slug:slug>/', views.book_by_slug, name='book_by_slug'),
   ```
   اگر آدرس حاوی فاصله یا نویسه‌ی خاص مثل «!» باشد، الگو رد می‌شود. این کار برای آدرس‌های خوانای سئویی (مثل `/shop/books/harry-potter/`) عالی است.

5. **استفاده از `<uuid:...>` برای شناسه‌های یکتا**  
   `uuid` فقط رشته‌هایی که قالب UUID استاندارد دارند را می‌پذیرد:
   ```python
   path('orders/<uuid:tracking_id>/', views.order_detail, name='order_detail'),
   ```
   آدرس معتبر مثل `550e8400-e29b-41d4-a716-446655440000`. این الگو برای مدل‌هایی که فیلد `UUIDField` دارند (مثل کد رهگیری) استفاده می‌شود و مزیتش این است که نمی‌توان با حدس زدن اعداد، به داده‌ی دیگری رسید.

6. **چند پارامتر در یک مسیر**  
   در یک الگو می‌توان چند جای‌گذار داشت که به‌ترتیب به پارامترهای ویو می‌رسند:
   ```python
   path('reports/<int:year>/<int:month>/', views.monthly_report, name='monthly_report'),
   ```
   و در ویو: `def monthly_report(request, year, month): ...`. حالا آدرس `/shop/reports/1403/11/` دو عدد صحیح تحویل ویو می‌دهد.

7. **عبارت‌های منظم با `re_path()`**  
   وقتی الگوهای آماده کافی نباشند، می‌توانیم با `re_path` و عبارت منظم مسیر تعریف کنیم. مثلاً نام یک نویسنده که فقط حروف کوچک و خط تیره دارد:
   ```python
   from django.urls import re_path

   re_path(r'^authors/(?P<slug>[0-9a-z-]+)/$', views.author_detail),
   ```
   قوانین regex به‌صورت کامل اعمال می‌شوند و باید خودمان ابتدا (`^`) و انتهای مسیر (`$`) را مشخص کنیم.

8. **گروه‌های نام‌دار در `re_path`**  
   برای اینکه پارامترهای regex به‌صورت کلمه‌ای به ویو برسند، از گروه‌های نام‌دار (named groups) استفاده می‌کنیم:
   ```python
   re_path(r'^archive/(?P<year>[0-9]{4})/(?P<name>[\w-]+)/$', views.archive, name='archive'),
   ```
   ویو باید پارامترهای `year` و `name` را بگیرد. نکته: در `re_path` مقدار پارامتر همیشه رشته است؛ پس اگر `year` را لازم داریم باید در ویو `int(year)` کنیم.

9. **include تودرتو (Nested includes)**  
   `include` را می‌توان لایه‌لایه داشت تا urls هر ماژول خیلی تمیز بماند. مثلاً مسیرهای بخش «ادمین فروشگاه» را در فایل `shop/admin_urls.py` می‌گذاریم:
   ```python
   path('shop/admin/', include('shop.admin_urls')),
   ```
   و داخل `admin_urls.py` مسیرهای آن بخش را تعریف می‌کنیم. هر `include` یک پیشوند جدا می‌کند و به همین ترتیب می‌توان چند لایه ساخت. این روش برای پروژه‌های بزرگ که چند تیم روی ماژول‌های مختلف کار می‌کنند ضروری است.

10. **اعمال namespace برای اپلیکیشن**  
    با namespace می‌توان به مسیرهای هر اپلیکیشن «فضای نام» داد تا اگر دو اپ مسیرهایی با نام یکسان داشتند (مثل `book_detail` در دو اپ)، تداخل پیش نیاید:
    ```python
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    ```
    حالا در پروژه، این مسیرها با پیشوند `shop:` شناخته می‌شوند، مثل `shop:book_detail`.

11. **دسترسی به مسیرهای namespace داخل تمپلیت و ویو**  
    بعد از تعریف namespace، همه‌ی ارجاع‌ها باید از طریق آن انجام شود. در تمپلیت:
    ```html
    {% url 'shop:book_detail' book.pk %}
    ```
    و در ویو:
    ```python
    return redirect('shop:book_detail', pk=book.pk)
    ```
    اگر namespace را فراموش کنیم، خطای `NoReverseMatch` می‌گیریم. این موضوع در سرفصل «Reverse URL Lookup» کامل‌تر بررسی می‌شود.

12. **پاس دادن پارامترهای اضافه با dict در `path()`**  
    آرگومان سوم تابع `path()` (بعد از ویو) می‌تواند یک dict باشد که به‌عنوان کوئری‌استرینگ یا context اضافی به ویو منتقل می‌شود:
    ```python
    path('books/', views.book_list, {'featured': True}, name='book_list_featured'),
    ```
    ویو پارامتر اضافه می‌گیرد: `def book_list(request, featured=False): ...`. این روش برای چند مسیر که به یک ویو با تنظیمات متفاوت وصل می‌شوند مفید است.

13. **ترتیب قواعد و برخورد الگوها**  
    ترتیب تعریف الگوها خیلی مهم است. مثلاً اگر `<str:category_name>` را قبل از `books/new/` تعریف کنیم، درخواست `books/new/` با category تطبیق می‌یابد و ویوی اشتباه صدا زده می‌شود. قانون ساده: از خاص به عام تعریف کنید؛ مسیرهای ثابت اول، بعد مسیرهای پارامتری، بعد regexها.

14. **اشکال‌زدایی الگوهای پیچیده**  
    برای پیدا کردن مشکل regexها، می‌توانیم با `python manage.py shell` الگو را مستقیم تست کنیم:
    ```python
    from django.urls import reverse, resolve

    match = resolve('/shop/archive/1403/book-title/')
    print(match.func, match.kwargs)  # ویو و پارامترهای استخراج‌شده
    ```
    با `resolve` می‌بینیم یک آدرس با کدام الگو تطبیق یافته و چه پارامترهایی به ویو می‌رسد؛ بهترین ابزار برای اشکال‌زدایی‌ایست.

15. **تمرین جامع: طراحی آدرس‌های تمیز فروشگاه**  
    مسیرهای فروشگاه را با ترکیب همه‌ی یادگرفته‌ها بازطراحی کنید:
    - کتاب با `slug` (`books/<slug:slug>/`)
    - آرشیو انتشارات به‌صورت سال و ماه (`archive/<int:year>/<int:month>/`)
    - جزئیات سفارش با `uuid` (`orders/<uuid:pk>/`)
    - namespace برای کل اپ (مثلاً `shop:books`)
    - یک regex با گروه نام‌دار برای کد تخفیف (`discount/code/<...>/`)
    
    بعد از هر تغییر، با چند آدرس مختلف در مرورگر و `resolve` در shell بررسی کنید که هر آدرس به ویوی درست برخورد می‌کند.