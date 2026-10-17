## سرفصل: جستجوی معکوس URL (Reverse URL Lookup)

### منابع آموزشی

**مستندات رسمی Django:**
- [URL dispatcher — بخش Reverse resolution of URLs و توابع reverse/url](https://docs.djangoproject.com/en/5.2/topics/http/urls/#reverse-resolution-of-urls)

**مقالات آموزشی:**
- [Simple Is Better Than Complex – Working with Django URLs — مثال‌های reverse و namespace](https://simpleisbetterthancomplex.com/article/2016/08/31/working-with-django-urls-in-a-better-way.html)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه‌ی `mysite` اپلیکیشن «فروشگاه کتاب» (shop) را داریم. تا اینجا مسیرها را نام‌گذاری کردیم و namespace یاد گرفتیم. در این تمرین «جستجوی معکوس» (reverse) را پیاده می‌کنیم: به‌جای نوشتن مستقیم آدرس در کد، آدرس را از روی نام و namespace می‌سازیم. هدف این است که پروژه را طوری بنویسیم که با تغییر آدرس‌ها، هیچ لینکی در کد نشکند.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **مشکل لینک‌های هاردکد و معرفی reverse**  
   اگر در کد بنویسیم `href="/shop/books/3/"`، به محض تغییر مسیرها، این لینک می‌شکند و مجبوریم همه‌ی کدها را جستجو و عوض کنیم. راه‌حل «جستجوی معکوس» است: مسیرها را با نام می‌شناسیم و آدرس را از روی نام می‌سازیم. Django همین کار را در هنگام ساخت لینک انجام می‌دهد: `reverse('book_detail', args=[3])` خروجی می‌دهد `/shop/books/3/`.

2. **تست `reverse()` در shell**  
   قبل از استفاده در کد، در `python manage.py shell` امتحان می‌کنیم:
   ```python
   from django.urls import reverse

   print(reverse('book_list'))        # /shop/books/
   print(reverse('book_detail', args=[5]))   # /shop/books/5/
   ```
   اینجا «reverse» یعنی معکوسِ حلِ URL: به‌جای تطبیق آدرس با الگو، الگو را گرفته و برعکس آدرس می‌سازیم.

3. **پاس دادن پارامترها با `args` و `kwargs`**  
   برای مسیرهای پارامتری دو روش داریم: `args` (لیست به‌ترتیب) و `kwargs` (دیکشنری با نام پارامتر):
   ```python
   reverse('monthly_report', args=[1403, 11])
   reverse('monthly_report', kwargs={'year': 1403, 'month': 11})
   ```
   هر دو خروجی یکسان می‌دهند. قانون: نام‌ها در `kwargs` باید دقیقاً با نام پارامترهای الگوی مسیر یکی باشند.

4. **reverse با namespace**  
   وقتی از namespace استفاده کرده‌ایم، باید نام مسیر را با پیشوند namespace صدا بزنیم:
   ```python
   print(reverse('shop:book_detail', args=[3]))
   ```
   اگر namespace را فراموش کنیم، خطای `NoReverseMatch` می‌گیریم. در پروژه‌های بزرگ که چند اپ مسیرهای هم‌نام دارند، بدون namespace ابهام ایجاد می‌شود.

5. **برعکسِ reverse: تابع `resolve()`**  
   `resolve` عکسِ `reverse` است: یک آدرس می‌گیرد و نام ویو و پارامترها را برمی‌گرداند:
   ```python
   from django.urls import resolve

   match = resolve('/shop/books/5/')
   print(match.url_name)      # book_detail
   print(match.namespace)     # shop
   print(match.kwargs)        # {'pk': 5}
   ```
   این تابع برای میدلورها و اشکال‌زدایی کاربرد زیادی دارد.

6. **هدایت (redirect) با نام مسیر در ویوها**  
   در ویوها، متداول‌ترین استفاده از reverse از طریق شورت‌کات `redirect` است:
   ```python
   from django.shortcuts import redirect

   def after_payment(request, order_id):
       ...
       return redirect('shop:order_detail', order_id=order_id)
   ```
   `redirect` وقتی یک string به آن بدهیم که با نام مسیر تطبیق یابد، خودش reverse می‌کند.

7. **استفاده از `{% url %}` در تمپلیت‌ها**  
   در تمپلیت، تگ `{% url %}` همان نقش `reverse` را دارد و لینک را بدون هاردکد کردن می‌سازد:
   ```html
   <a href="{% url 'book_list' %}">لیست کتاب‌ها</a>
   ```
   این تگ پرکاربردترین روش لینک‌سازی در همه‌ی پروژه‌های Django است.

8. **`{% url %}` با پارامتر و namespace**  
   برای مسیرهای پارامتری، مقدار پارامتر را بعد از نام مسیر می‌دهیم:
   ```html
   {% url 'shop:book_detail' book.pk %}
   <a href="{% url 'shop:book_detail' pk=book.pk %}">جزئیات</a>
   ```
   هر دو شکل معتبر است. پارامترها می‌توانند متغیر خودِ تمپلیت باشند یا مقادیر ثابت.

9. **خطای `NoReverseMatch` و رفع آن**  
   وقتی نام مسیر یا namespace اشتباه باشد، در مرورگر خطای `NoReverseMatch` می‌بینیم. برای یافتن اشکال:
   - فهرست همه‌ی مسیرهای پروژه را با `python manage.py show_urls` (اگر کتابخانه‌ی django-extensions نصب است) یا بررسی دستی `urls.py` ببینید.
   - نام کامل را با namespace بنویسید: `shop:book_detail`.
   - چک کنید تعداد و نام پارامترها دقیقاً با الگو یکی است.
   
   این خطا در توسعه‌ی اولیه بسیار رایج است و سریع رفع می‌شود.

10. **استفاده از reverse در متد `get_absolute_url` مدل**  
    برای اینکه هر شیء بداند آدرس «صفحه‌ی خودش» چیست، متد `get_absolute_url` را در مدل اضافه می‌کنیم:
    ```python
    class Book(models.Model):
        ...
        def get_absolute_url(self):
            return reverse('shop:book_detail', kwargs={'pk': self.pk})
    ```
    حالا در هر ویو و تمپلیت با `{{ book.get_absolute_url }}` یا `redirect(book)` می‌توانیم مستقیم به صفحه‌ی فردی دسترسی پیدا کنیم.

11. **`reverse_lazy` برای attributeهای کلاس**  
    در CBV وقتی `success_url` را با `reverse` بسازیم، خطا می‌گیریم چون در هنگام تعریف کلاس هنوز URLconf بارگذاری کامل نشده است. باید از `reverse_lazy` استفاده کنیم که تا لحظه‌ی استفاده، معکوس‌سازی را به‌تعویق می‌اندازد:
    ```python
    from django.urls import reverse_lazy

    class BookCreateView(CreateView):
        model = Book
        fields = ['title', 'author', 'price']
        success_url = reverse_lazy('shop:book_list')
    ```
    `reverse_lazy` برای همه‌ی attributeها و تنظیمات سراسری که در زمان import اجرا می‌شوند، انتخاب درست است.

12. **تمرین جامع: پاکسازی پروژه‌ی فروشگاه از لینک‌های هاردکد**  
    کل پروژه را برای لینک‌های هاردکد جستجو کنید (مثل `/shop/books/`) و همه را با `{% url %}` در تمپلیت‌ها و `reverse`/`redirect` در ویوها جایگزین کنید. سپس برای تمرین، یک آدرس را عوض کنید (مثلاً `books/` را به `catalogue/`) و ببینید که با یک‌بار ویرایش مسیر و بدون دست‌زدن به لینک‌ها، همه‌ی سایت به‌درستی کار می‌کند. این دقیقاً ارزش عملی جستجوی معکوس است.