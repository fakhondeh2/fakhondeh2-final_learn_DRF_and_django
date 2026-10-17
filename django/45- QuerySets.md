## سرفصل: QuerySetها در Django (Django QuerySets)

### منابع آموزشی

**مستندات رسمی Django:**
- [Django – Making queries — ساخت کوئری با all, filter, exclude, get و Q objects](https://docs.djangoproject.com/en/5.2/topics/db/queries/)
- [Django – QuerySet API reference — مرجع کامل متدهای QuerySet و field lookups](https://docs.djangoproject.com/en/5.2/ref/models/querysets/)
- [Django – Aggregation — aggregation و annotate با Count, Sum, Avg, Max, Min](https://docs.djangoproject.com/en/5.2/topics/db/aggregation/)

**مطالب تکمیلی:**
- [Django – QuerySet methods — فهرست کامل متدها با توضیح](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#methods-that-return-new-querysets)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در فروشگاه کتاب `mysite` داده‌های کتاب‌ها، نویسنده‌ها و نظرها را داریم. می‌خواهیم گزارش‌ها و لیست‌های مختلف بسازیم: کتاب‌های زیر یک قیمت، پرفروش‌ترین نویسنده‌ها، کتاب‌هایی که نظر دارند و... . همه‌ی این‌ها با QuerySet انجام می‌شود. هدف این است که QuerySet را به‌عنوان زبان پرس‌وجوی Django به‌خوبی یاد بگیریم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **QuerySet چیست و چرا مهم است؟**  
   QuerySet یک شیء پایتونی است که نماینده‌ی یک پرس‌وجوی دیتابیس است. وقتی آن را می‌سازید، هنوز هیچ کوئری به دیتابیس نمی‌رود؛ فقط وقتی نتیجه را مصرف کنید (مثلاً حلقه بزنید یا لیستش کنید)، کوئری اجرا می‌شود. این «ارزیابی تنبل» (lazy) امکان زنجیره‌کردن متدها را می‌دهد.

2. **گرفتن همه‌ی رکوردها با `all()`**  
   `Book.objects.all()` یک QuerySet از همه‌ی کتاب‌ها برمی‌گرداند. هنوز کوئری نرفته است. سعی کنید در shell یک QuerySet بسازید و بعد `print` کنید تا ببینید SQL آن چیست. برای دیدن SQL، `str(queryset.query)` را چاپ کنید.

3. **فیلتر کردن با `filter()`**  
   `Book.objects.filter(is_available=True)` فقط کتاب‌های موجود را می‌دهد. می‌توانید چند شرط را پشت سر هم بگذارید که با AND ترکیب می‌شوند. `filter` یک QuerySet جدید برمی‌گرداند، پس می‌توانید زنجیره کنید.

4. **حذف کردن با `exclude()`**  
   `exclude` عکس `filter` است: رکوردهایی که شرط را ندارند برمی‌گرداند. `Book.objects.exclude(language='fa')` همه‌ی کتاب‌های غیرفارسی را می‌دهد. ترکیب `filter` و `exclude` برای کوئری‌های دقیق ضروری است.

5. **گرفتن یک رکورد با `get()`**  
   `get()` دقیقاً یک رکورد برمی‌گرداند. اگر هیچ رکوردی پیدا نشود `DoesNotExist` و اگر چند رکورد پیدا شود `MultipleObjectsReturned` می‌دهد. پس فقط وقتی استفاده کنید که مطمئنید شرط یکتا است. در ویوها معمولاً `get_object_or_404` بهتر است.

6. **Lookupهای فیلد (`__exact`, `__contains`, `__gt`, `__lt`, `__in`)**  
   با `__` می‌توانید نوع مقایسه را عوض کنید: `price__gt=100000` (بزرگ‌تر)، `title__contains='پاتر'` (شامل)، `price__in=[100, 200]` (در لیست)، `published_date__year=2020`. فهرست کامل lookupها در مستندات QuerySet API است. هرکدام را در shell امتحان کنید.

7. **Lookup روی فیلدهای رابطه‌ای**  
   می‌توانید روی رابطه‌ها هم فیلتر بزنید: `Book.objects.filter(author__name='رولینگ')`. هر `__` یک پرش در رابطه است. حتی می‌توانید چند سطح بروید: `Book.objects.filter(author__profile__city='تهران')`. این قدرت اصلی ORM است.

8. **ترتیب‌دهی با `order_by()`**  
   `Book.objects.order_by('-published_date')` نزولی و `order_by('price')` صعودی مرتب می‌کند. با چند فیلد می‌توانید ترتیب ثانویه بدهید: `order_by('language', '-price')`. برای حذف ترتیب پیش‌فرض، `order_by()` بدون آرگومان را صدا بزنید.

9. **محدودکردن تعداد با Slicing**  
   QuerySet قابل برش است: `Book.objects.all()[:10]` ده رکورد اول را می‌دهد و `[5:10]` رکوردهای ۵ تا ۱۰. برش معادل `LIMIT/OFFSET` در SQL است. توجه کنید که بعد از برش نمی‌توانید `filter` کنید.

10. **حذف تکراری‌ها با `distinct()`**  
    وقتی روی رابطه‌ای فیلتر می‌زنید، ممکن است رکوردها تکراری شوند. `distinct()` آن‌ها را یکتا می‌کند. مثلاً `Book.objects.filter(author__name__contains='ر').distinct()`. این متد در کوئری‌های پیچیده‌ی رابطه‌ای خیلی به کار می‌آید.

11. **کوچک‌کردن تعداد کوئری با `select_related`**  
    وقتی به فیلدهای یک ForeignKey یا OneToOne دسترسی می‌زنید، Django یک کوئری جدا می‌زند. اگر در لیست به نویسنده‌ی هر کتاب دسترسی بزنید، برای هر کتاب یک کوئری می‌خورد (مشکل N+1). با `select_related('author')` همه را در یک JOIN می‌گیرید.

12. **کوچک‌کردن تعداد کوئری با `prefetch_related`**  
    برای روابط ManyToMany و رابطه‌ی معکوس، `select_related` کار نمی‌کند؛ باید از `prefetch_related` استفاده کنید. این متد کوئری‌ها را جدا می‌زند اما نتایج را در پایتون به هم می‌چسباند. مثال: `Book.objects.prefetch_related('reviews')`.

13. **شمارش با `count()`**  
    `Book.objects.count()` تعداد رکوردها را می‌دهد. نکته‌ی مهم: از `len(queryset)` استفاده نکنید چون همه‌ی رکوردها را از دیتابیس می‌کشد؛ `count()` فقط یک `SELECT COUNT` می‌زند. این تفاوت در جدول‌های بزرگ مهم است.

14. **بررسی وجود با `exists()`**  
    `Book.objects.filter(...).exists()` یک بولین برمی‌گرداند و از `count() > 0` سریع‌تر است. برای چک‌کردن وجود رکورد قبل از ساخت، بهترین گزینه است. کد را خودتان بنویسید و در shell تست کنید.

15. **Q objects برای شرط‌های پیچیده**  
    برای OR و NOT، از `Q` استفاده کنید: `from django.db.models import Q` سپس `Book.objects.filter(Q(price__lt=100000) | Q(is_available=True))`. با `~` نقیض می‌گیرید: `~Q(language='fa')`. بدون Q، ترکیب OR ممکن نیست.

16. **F expressions برای مقایسه‌ی فیلد با فیلد**  
    `from django.db.models import F` به شما اجازه می‌دهد یک فیلد را با فیلد دیگر مقایسه کنید: `Book.objects.filter(stock__gt=F('sold'))`. همچنین می‌توانید مقدار فیلد را در دیتابیس به‌روز کنید: `Book.objects.update(price=F('price') * 1.1)`. این کار بدون خواندن و نوشتن در پایتون انجام می‌شود.

17. **تجمیع با `aggregate()`**  
    `Book.objects.aggregate(Avg('price'))` میانگین قیمت را در یک دیکشنری می‌دهد. توابع `Count`، `Sum`، `Avg`، `Max`، `Min` را می‌توانید استفاده کنید. این متد یک مقدار کلی برمی‌گرداند، نه QuerySet.

18. **گروه‌بندی با `annotate()`**  
    `annotate` به هر رکورد یک مقدار محاسبه‌شده اضافه می‌کند. مثلاً `Author.objects.annotate(num_books=Count('book'))` تعداد کتاب هر نویسنده را می‌دهد. سپس می‌توانید با `filter(num_books__gt=0)` روی آن فیلتر کنید. تفاوت annotate و aggregate همین است: annotate روی هر رکورد، aggregate روی کل.

19. **ترکیب annotate و order_by برای گزارش**  
    پرفروش‌ترین نویسنده‌ها را بسازید: `Author.objects.annotate(total=Sum('book__price')).order_by('-total')`. این الگو برای داشبورد و گزارش‌گیری بسیار پرکاربرد است.

20. **تمرین تکمیلی: گزارش‌های فروشگاه**  
    با QuerySet این گزارش‌ها را بسازید: (۱) کتاب‌های موجود زیر ۲۰۰ هزار تومان مرتب بر اساس قیمت، (۲) نویسندگانی که بیشتر از ۲ کتاب دارند با تعداد کتاب‌هایشان، (۳) کتاب‌هایی که میانگین امتیاز نظرهایشان بالای ۴ است، (۴) مجموع ارزش موجودی (قیمت × تعداد) کل فروشگاه. هر کوئری را اول در shell بنویسید، SQL آن را ببینید، و بعد تعداد کوئری‌هایش را با `select_related` و `prefetch_related` بهینه کنید.
