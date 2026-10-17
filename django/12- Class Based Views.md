## سرفصل: ویوهای مبتنی بر کلاس (Class-Based Views)

### منابع آموزشی

**مستندات رسمی Django:**
- [Class-based views — مقدمه، مزایا و راهنمای استفاده از کلاس‌های عمومی](https://docs.djangoproject.com/en/5.2/topics/class-based-views/)
- [Generic display views — مرجع TemplateView، ListView و DetailView](https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-display/)
- [Generic editing views — مرجع CreateView، UpdateView و DeleteView](https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-editing/)

**وب‌سایت کمکی:**
- [CCBV (Classy Class-Based Views) — نمایش همه‌ی attributeها و متدهای هر کلاس](https://ccbv.co.uk/)

**آموزش‌های گام‌به‌گام:**
- [MDN – Django Tutorial Part 6: Generic list and detail views — ساخت ListView و DetailView با مثال](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Generic_views)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه‌ی `mysite` اپلیکیشن «فروشگاه کتاب» (shop) را داریم. ویوهای فروشگاه را که قبلاً تابعی نوشتیم، حالا با ویوهای مبتنی بر کلاس (CBV) بازنویسی می‌کنیم: صفحه‌ی اصلی، لیست کتاب‌ها، جزئیات کتاب، افزودن کتاب، ویرایش کتاب و حذف کتاب. هدف این است که با کلاس‌های عمومی Django و نحوه‌ی سفارشی‌سازی attributeها و متدهایشان کار کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت ویو مبتنی بر کلاس و مقایسه با FBV**  
   CBV به‌جای تابع، یک کلاس است و هر متد HTTP (مثل `get` و `post`) یک متد جداگانه در کلاس دارد. Django متد متناسب با متد درخواست را صدا می‌زند. وراثت و اشتراک‌گذاری باعث می‌شود کد کم‌تر و ساختارمندتر باشد. ساده‌ترین حالت استفاده از کلاس‌های از پیش ساخته‌ای است که Django ارائه می‌دهد.

2. **ساخت اولین CBV با `TemplateView`**  
   `TemplateView` فقط یک تمپلیت را رندر می‌کند و برای صفحات ایستا عالی است:
   ```python
   from django.views.generic import TemplateView

   class HomeView(TemplateView):
       template_name = 'shop/home.html'
   ```
   و در urls: `path('', HomeView.as_view(), name='home')`. با `as_view()` از کلاس یک تابع ساخته می‌شود که urlpatterns می‌تواند بپذیرد.

3. **سفارشی‌سازی attributeهای کلاس**  
   در CBV بیشتر رفتارها با attributeها تنظیم می‌شود. `template_name`، `model`، `queryset` و `context_object_name` از مهم‌ترین‌ها هستند. مقداردهی به آن‌ها، جایگزین همان کاری است که در FBV داخل تابع انجام می‌دادیم:
   ```python
   class BookListView(ListView):
       model = Book
       template_name = 'shop/book_list.html'
       context_object_name = 'books'
   ```
   با `context_object_name` مشخص می‌کنیم داده در تمپلیت با چه نامی در دسترس باشد (پیش‌فرض `object_list` است).

4. **افزودن داده‌ی بیشتر به context با `get_context_data`**  
   گاهی علاوه بر لیست اصلی، داده‌های دیگری هم باید به تمپلیت برسد. متد `get_context_data` را override می‌کنیم:
   ```python
   class BookListView(ListView):
       model = Book
       template_name = 'shop/book_list.html'

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['total_books'] = Book.objects.count()
           return context
   ```
   صدا زدن `super()` را فراموش نکنید؛ وگرنه متغیر اصلی (`object_list` یا `books`) در context نخواهد بود.

5. **سفارشی‌سازی queryset با `get_queryset`**  
   برای فیلتر کردن، به‌جای attribute ثابت، متد `get_queryset` را override می‌کنیم؛ مخصوصاً وقتی فیلتر به داده‌ی درخواست بستگی دارد:
   ```python
   class BookListView(ListView):
       model = Book
       template_name = 'shop/book_list.html'

       def get_queryset(self):
           return Book.objects.available().order_by('-published_date')
   ```
   اینجا از Manager سفارشی `available()` که در سرفصل‌های قبل ساختیم استفاده می‌کنیم.

6. **ساخت `DetailView` برای صفحه‌ی جزئیات کتاب**  
   کلاس `DetailView` یک شیء واحد را بر اساس پارامتر مسیر (مثل `pk`) واکشی می‌کند و در context با نام پیش‌فرض `object` قرار می‌دهد:
   ```python
   class BookDetailView(DetailView):
       model = Book
       template_name = 'shop/book_detail.html'
   ```
   در urls: `path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail')`. اگر کتاب پیدا نشود، خودش 404 برمی‌گرداند.

7. **محدودسازی `DetailView` با override کردن `get_queryset`**  
   در `DetailView` هم می‌توان `get_queryset` را override کرد تا فقط کتاب‌های خاصی قابل نمایش باشند:
   ```python
   class BookDetailView(DetailView):
       model = Book
       template_name = 'shop/book_detail.html'

       def get_queryset(self):
           return Book.objects.available()
   ```
   حالا اگر کسی آدرس مستقیم یک کتابِ ناموجود را باز کند، 404 می‌گیرد؛ رفتار امن‌تری نسبت به نمایش صفحه‌ی خالی.

8. **ساخت `CreateView` برای افزودن کتاب**  
   کلاس `CreateView` هم فرم را می‌سازد، هم اعتبارسنجی می‌کند و هم رکورد جدید را ذخیره می‌کند:
   ```python
   from django.views.generic.edit import CreateView

   class BookCreateView(CreateView):
       model = Book
       fields = ['title', 'author', 'price', 'published_date']
       template_name = 'shop/book_form.html'
       success_url = reverse_lazy('book_list')
   ```
   با `fields` مشخص می‌کنیم کدام فیلدها در فرم ظاهر شوند. برای `success_url` از `reverse_lazy` استفاده می‌کنیم نه `reverse`؛ چون urlpatterns هنگام تعریف کلاس هنوز کامل بارگذاری نشده است.

9. **تعیین مقصد موفقیت با `success_url` و `get_absolute_url`**  
   دو روش برای مقصد بعد از ذخیره‌ی موفق وجود دارد: attribute به نام `success_url`، یا دادن متد `get_absolute_url` به مدل:
   ```python
   class Book(models.Model):
       ...
       def get_absolute_url(self):
           from django.urls import reverse
           return reverse('book_detail', kwargs={'pk': self.pk})
   ```
   وقتی مدل این متد را داشته باشد، CBV به‌طور خودکار به آن مسیر redirect می‌کند و دیگر به `success_url` نیاز نیست.

10. **override کردن `form_valid` برای منطق پس از ذخیره**  
    اگر بعد از معتبر بودن فرم کاری لازم داریم، `form_valid` را override می‌کنیم. مثلاً کاربرِ واردشده را به کتاب نسبت می‌دهیم (فرض کنید مدل `Book` فیلد `added_by` دارد):
    ```python
    class BookCreateView(CreateView):
        model = Book
        fields = ['title', 'author', 'price']
        template_name = 'shop/book_form.html'

        def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.added_by = self.request.user
            self.object.save()
            return super().form_valid(form)
    ```
    `super().form_valid(form)` همان redirect به `get_absolute_url` را انجام می‌دهد.

11. **ساخت `UpdateView` برای ویرایش**  
    `UpdateView` مثل CreateView است، با این تفاوت که شیء موجود را از پارامتر مسیر می‌گیرد، فرم را با داده‌ی فعلی پر می‌کند و تغییرات را ذخیره می‌کند:
    ```python
    class BookUpdateView(UpdateView):
        model = Book
        fields = ['title', 'price', 'stock']
        template_name = 'shop/book_form.html'
    ```
    مسیر: `path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update')`. چون `success_url` نداریم، از `get_absolute_url` مدل استفاده می‌شود.

12. **ساخت `DeleteView` برای حذف با تأیید**  
    `DeleteView` اول یک صفحه‌ی تأیید نشان می‌دهد و بعد از ارسال POST، رکورد را حذف می‌کند. حذف مستقیم از طریق GET کار درستی نیست:
    ```python
    class BookDeleteView(DeleteView):
        model = Book
        template_name = 'shop/book_confirm_delete.html'
        success_url = reverse_lazy('book_list')
    ```
    تمپلیت تأیید باید یک فرم با دکمه‌ی «حذف» داشته باشد که با POST ارسال شود. مسیر: `path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete')`.

13. **محدودسازی دسترسی با `LoginRequiredMixin`**  
    در CBV به‌جای دکوراتور `login_required` از mixinها استفاده می‌کنیم. mixinها باید در سمت چپِ کلاس اصلی نوشته شوند:
    ```python
    from django.contrib.auth.mixins import LoginRequiredMixin

    class BookCreateView(LoginRequiredMixin, CreateView):
        model = Book
        fields = ['title', 'author', 'price']
        template_name = 'shop/book_form.html'
    ```
    به این ترتیب کاربر مهمان به صفحه‌ی لاگین هدایت می‌شود. mixinها متدهای کلاس اصلی را گسترش می‌دهند و ترتیب نوشتن آن‌ها مهم است.

14. **درک زنجیره‌ی وراثت با وب‌سایت CCBV**  
    به وب‌سایت ccbv.co.uk بروید و مثلاً `DetailView` را جستجو کنید. می‌بینید که `DetailView` از `SingleObjectTemplateResponseMixin`، `BaseDetailView` و... می‌آید و هر متد (`get`، `get_object`، `get_context_data`) در کدام کلاس تعریف شده است. این ابزار بهترین مرجع برای این است که بفهمیم چه چیزی را override کنیم.

15. **بازنویسی کامل ویوهای فروشگاه به CBV و مقایسه‌ی حجم کد**  
    همه‌ی ویوهای تابعی فروشگاه (صفحه‌ی اصلی، لیست، جزئیات، افزودن، ویرایش و حذف) را به کلاس‌های عمومی تبدیل کنید و urls را با `as_view()` به‌روزرسانی کنید. سپس تعداد خط‌های دو نسخه را کنار هم مقایسه کنید: نسخه‌ی CBV به‌طور محسوسی کوتاه‌تر است و منطق تکراری (فرم، اعتبارسنجی، 404) حذف شده است. جایی که به سفارشی‌سازی عمیق نیاز دارید، همان‌جاها را با override متدها دوباره شخصی‌سازی کنید.