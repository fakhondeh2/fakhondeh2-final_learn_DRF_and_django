## سرفصل: ویوهای مبتنی بر تابع (Function-Based Views)

### منابع آموزشی

**مستندات رسمی Django:**
- [Writing views — مرجع کامل ویوها، HttpRequest و شورت‌کات‌های render/redirect](https://docs.djangoproject.com/en/5.2/topics/http/views/)
- [Request and response objects — مرجع کامل HttpRequest و HttpResponse](https://docs.djangoproject.com/en/5.2/ref/request-response/)

**آموزش‌های گام‌به‌گام:**
- [MDN – Django Tutorial Part 5: Creating our home page — ساخت ویو و تست درخواست‌ها](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Home_page)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه‌ی `mysite` اپلیکیشن «فروشگاه کتاب» (shop) را داریم. در این تمرین همه‌ی ویوهای موردنیاز فروشگاه را به‌صورت تابعی (Function-Based View) می‌نویسیم: صفحه‌ی اصلی، لیست کتاب‌ها، جزئیات کتاب، فرم جستجو و فرم افزودن نظر. هدف این است که با اجزای اصلی یک ویو — یعنی دریافت درخواست (HttpRequest) و تولید پاسخ (HttpResponse) — به‌طور کامل آشنا شویم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت ویو و امضای تابع**  
   ویو در Django یک تابع (یا هر callable) پایتونی است که یک `HttpRequest` می‌گیرد و یک `HttpResponse` برمی‌گرداند. Django همه‌ی جزئیات HTTP (متادیتا، داده‌ی فرم، کوکی و...) را در شیء `request` جمع می‌کند و آن را به تابع ما پاس می‌دهد:
   ```python
   def my_view(request):
       return HttpResponse('پاسخ')
   ```

2. **ساخت اولین ویو تابعی برای صفحه‌ی اصلی**  
   در `shop/views.py` تابع `index` را می‌نویسیم که پیام خوش‌آمد فروشگاه را برمی‌گرداند:
   ```python
   from django.http import HttpResponse

   def index(request):
       return HttpResponse('<h1>به فروشگاه کتاب خوش آمدید</h1>')
   ```
   و آن را با `path('', views.index)` به مسیر ریشه وصل می‌کنیم.

3. **HttpResponse با هدر و کد وضعیت سفارشی**  
   `HttpResponse` را می‌توان با هدرهای HTTP و کد وضعیت ساخت. `request` و `response` هر دو مثل دیکشنری در دسترس هستند:
   ```python
   response = HttpResponse('محتوای صفحه')
   response['X-Request-From'] = 'Django'
   response.status_code = 201
   ```
   این تمرین برای درک این که «پاسخ» فقط یک رشته‌ی HTML نیست، مهم است و پایه‌ی کار بعدی با DRF خواهد بود.

4. **رندر کردن تمپلیت با `render()`**  
   اجازه دهید پاسخ را از یک فایل تمپلیت تولید کنیم. شورت‌کات `render` تمپلیت را می‌خواند، با context ترکیب می‌کند و یک `HttpResponse` می‌سازد:
   ```python
   from django.shortcuts import render

   def index(request):
       return render(request, 'shop/index.html', {'shop_name': 'کتاب‌سرا'})
   ```
   فایل `shop/index.html` را می‌سازیم و داخل آن با `{{ shop_name }}` نام فروشگاه را نشان می‌دهیم.

5. **پاس دادن context به تمپلیت**  
   در ویو `book_list` همه‌ی کتاب‌ها را از دیتابیس می‌خوانیم و به تمپلیت می‌دهیم:
   ```python
   def book_list(request):
       books = Book.objects.all()
       return render(request, 'shop/book_list.html', {'books': books})
   ```
   در تمپلیت با حلقه‌ی `{% for book in books %}` کتاب‌ها را چاپ می‌کنیم. این همان الگوی کلاسیک MVT است: ویو داده را آماده می‌کند و تمپلیت آن را نمایش می‌دهد.

6. **تفکیک GET و POST با `request.method`**  
   هر شیء `request` یک attribute به نام `method` دارد که نوع درخواست را می‌گوید (مثل `GET` یا `POST`). یک ویو می‌تواند بر اساس متد رفتار متفاوتی داشته باشد:
   ```python
   def search(request):
       if request.method == 'POST':
           return HttpResponse('جستجوی POST')
       return HttpResponse('جستجوی GET')
   ```
   در عمل فرم‌های HTML معمولاً GET را برای جستجو و POST را برای ارسال داده‌ی تغییردهنده استفاده می‌کنند.

7. **دریافت پارامترهای مسیر در ویو**  
   پارامترهایی که در urls تعریف می‌شوند، به‌عنوان آرگومان به تابع می‌رسند. در مسیر `path('books/<int:pk>/', views.book_detail)` تابع باید پارامتر `pk` را بگیرد:
   ```python
   def book_detail(request, pk):
       book = get_object_or_404(Book, pk=pk)
       return render(request, 'shop/book_detail.html', {'book': book})
   ```
   این نحوه‌ی «پارامتر گرفتن» از مسیر، یکی از مهم‌ترین کارهای عملی ویوهاست.

8. **خواندن query string با `request.GET`**  
   وقتی کاربر درخواستی مثل `/shop/search/?q=python` می‌فرستد، داده‌ها در `request.GET` قرار می‌گیرند. `request.GET` یک `QueryDict` است که شبیه دیکشنری کار می‌کند، اما برای گرفتن مقدار نبوده بهتر است از `.get()` استفاده کنیم:
   ```python
   def search(request):
       q = request.GET.get('q', '')   # اگر q نیامده بود، رشته‌ی خالی
       books = Book.objects.filter(title__icontains=q) if q else Book.objects.none()
       return render(request, 'shop/search.html', {'books': books, 'q': q})
   ```
   این ویو فرم جستجوی ساده‌ی فروشگاه را پیاده می‌کند.

9. **پردازش POST با `request.POST`**  
   برای فرم‌ها، داده‌ی ارسالی در `request.POST` قرار می‌گیرد. یک ویو برای «افزودن نظر به کتاب» می‌سازیم که داده‌ی فرم را بخواند و یک `Review` بسازد:
   ```python
   if request.method == 'POST':
       rating = request.POST.get('rating')
       comment = request.POST.get('comment')
       Review.objects.create(book=book, rating=rating, comment=comment)
   ```
   نکته: داده‌ی رشته‌ای را قبل از ذخیره، به نوع درست تبدیل کنید (مثلاً `rating` را `int` کنید).

10. **دسترسی به `request.FILES` برای فایل‌ها**  
    اگر فرمی فایل آپلود کند، فایل‌ها در `request.FILES` و جدا از `request.POST` قرار می‌گیرند. برای مثال برای آپلود جلد کتاب:
    ```python
    cover = request.FILES.get('cover')
    if cover:
        book.cover = cover
        book.save()
    ```
    این بخش همیشه دیده نمی‌شود، اما بخشی از شناخت کامل request است.

11. **الگوی Post/Redirect/Get و شورت‌کات `redirect()`**  
    بعد از موفقیت‌آمیز بودن POST، هرگز همان ویو را دوباره رندر نکنید؛ اگر کاربر صفحه را refresh کند، فرم دوباره ارسال می‌شود و داده‌ی تکراری ساخته می‌شود. به‌جای آن با `redirect` کاربر را به یک مسیر دیگر بفرستید:
    ```python
    from django.shortcuts import redirect

    return redirect('book_detail', pk=book.pk)
    ```
    شورت‌کات `redirect` می‌تواند یک name، یک مسیر یا شیءی که متد `get_absolute_url` دارد را بگیرد.

12. **مدیریت خطاها: `get_object_or_404` و `raise Http404`**  
    در ویوهایی که بر اساس پارامتر آدرس، یک شیء را واکشی می‌کنند، اگر پیدا نشد باید 404 بدهیم. نسخه‌ی دستی:
    ```python
    from django.http import Http404

    def book_detail(request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404('کتاب پیدا نشد')
        return render(request, 'shop/book_detail.html', {'book': book})
    ```
    یک‌خطی‌اش همان `get_object_or_404` است که دیدید؛ هم‌خانواده‌ی `get_list_or_404` برای لیست‌ها هم هست.

13. **پاسخ‌های خطا مثل `HttpResponseNotFound`**  
    گاهی به‌جای exception، می‌خواهیم صریح کد وضعیت بدهیم. کلاس‌هایی مثل `HttpResponseNotFound`، `HttpResponseRedirect` و `HttpResponseBadRequest` هستند:
    ```python
    return HttpResponseNotFound('این صفحه وجود ندارد')
    ```
    یا معادلش: `HttpResponse('متن', status=404)`. آشنایی با کدهای وضعیت، پایه‌ی کار بعدی با DRF است.

14. **محدودسازی دسترسی با `login_required` و دکوراتورها**  
    ویوها را می‌توان با دکوراتورها پوشاند. مثلاً برای اینکه صفحه‌ی «افزودن کتاب» فقط برای کاربران واردشده باشد:
    ```python
    from django.contrib.auth.decorators import login_required

    @login_required
    def add_book(request):
        ...
    ```
    کاربر مهمان به صفحه‌ی لاگین هدایت می‌شود و بعد از ورود، دوباره به همان صفحه برمی‌گردد. این نمونه‌ای از قدرت دکوراتورها در FBV است.

15. **تست ویوها در مرورگر و بررسی رفتار درخواست**  
    همه‌ی ویوهای ساخته‌شده را با سرور توسعه تست می‌کنیم: صفحه‌ی اصلی، لیست کتاب‌ها، جزئیات کتاب با شناسه‌های مختلف، جستجو با `?q=...`، افزودن نظر و صفحه‌ی 404 برای کتاب ناموجود. در بخش Network مرورگر (کلید F12) متد و کد وضعیت هر درخواست را بررسی کنید تا رابطه‌ی بین کد ویو و رفتار HTTP را با چشم ببینید.