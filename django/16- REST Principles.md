## سرفصل: REST Principles

### منابع آموزشی

**مستندات و مقالات معتبر:**
- [MDN – What is a REST API — مروری جامع بر اصول معماری REST و مفاهیم Resource و Endpoint](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/REST_framework_tutorial/1-_Serialization#introduction_to_rest_apis)
- [Wikipedia – REST — اصول REST به‌صورت کامل: Client-Server, Statelessness, Cacheability, Layered System, Uniform Interface](https://en.wikipedia.org/wiki/REST)
- [REST API Tutorial — معرفی Resource, HTTP Methods و Status Codes](https://restfulapi.net/)

**مستندات رسمی Django REST Framework:**
- [DRF – API Guide — مرجع کامل پیاده‌سازی REST API در Django](https://www.django-rest-framework.org/api-guide/requests/)
- [DRF – Tutorial — آموزش گام‌به‌گام ساخت REST API با Serializer و View](https://www.django-rest-framework.org/tutorial/1-serialization/)

**کتاب‌ها و مقالات تخصصی:**
- [RFC 7231 — مستند رسمی HTTP/1.1 که پایه REST است](https://datatracker.ietf.org/doc/html/rfc7231)
- [Roy Fielding’s dissertation — معماری REST و اصول آن از خالق REST](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` یک اپلیکیشن «کتابخانه دیجیتال» می‌سازیم. در این تمرین، یک RESTful API برای مدیریت کتاب‌ها، نویسندگان و امانت‌ها طراحی می‌کنیم. تمام اصول REST مانند شناسایی resourceها، statelessness، uniform interface و HATEOAS را در این API پیاده می‌کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت اصول معماری REST**  
   REST (Representational State Transfer) یک سبک معماری برای طراحی سیستم‌های توزیع‌شده است که شش محدودیت اصلی دارد: Client-Server (جداسازی کلاینت و سرور)، Statelessness (بدون حالت بودن)، Cacheability (قابلیت ذخیره‌سازی)، Layered System (سیستم لایه‌ای)، Uniform Interface (رابط یکنواخت) و Code on Demand (اختیاری). این طراحی باعث مقیاس‌پذیری، سادگی و قابلیت اطمینان APIها می‌شود.

2. **اصل Client-Server و جداسازی نگرانی‌ها**  
   در معماری REST، کلاینت (مرورگر، اپ موبایل) از سرور (API) جدا است. کلاینت فقط رابط کاربری را مدیریت می‌کند و سرور فقط ذخیره‌سازی و منطق داده را. در پروژه کتابخانه، کلاینت React/Vue از طریق HTTP به `api/books/` درخواست می‌دهد و سرور Django فقط JSON برمی‌گرداند. کلاینت هرگز به دیتابیس دسترسی مستقیم ندارد.

3. **Statelessness (بدون حالت بودن)**  
   هر درخواست از کلاینت به سرور باید تمام اطلاعات لازم برای پردازش آن درخواست را داشته باشد. سرور هیچ اطلاعاتی از جلسه قبلی نگه نمی‌دارد. در کتابخانه ما، هر درخواست `GET /api/books/` باید توکن احراز هویت را در هدر `Authorization` داشته باشد و سرور وضعیت قبلی کاربر را ذخیره نمی‌کند. اگر نیاز به session داریم، آن را در کلاینت (مثلاً localStorage) یا از طریق Token نگه می‌داریم.

4. **Cacheability (قابلیت ذخیره‌سازی)**  
   پاسخ‌های سرور باید به‌صراحت مشخص کنند که آیا قابل Cache هستند یا نه با استفاده از هدرهای `Cache-Control` و `Expires`. در کتابخانه ما، لیست کتاب‌ها (که زیاد تغییر نمی‌کند) را با `Cache-Control: max-age=3600` کش می‌کنیم، اما تعداد موجودی هر کتاب را با `Cache-Control: no-cache` از کش خارج می‌کنیم.

5. **Layered System (سیستم لایه‌ای)**  
   معماری REST اجازه می‌دهد لایه‌هایی مثل Load Balancer، Cache Proxy و API Gateway بین کلاینت و سرور قرار بگیرند. در پروژه ما، می‌توانیم یک Reverse Proxy (مثل Nginx) برای Cache کردن پاسخ‌ها و یک Load Balancer برای توزیع بار بین چند نمونه Django قرار دهیم. کلاینت هیچ‌وقت مستقیم به لایه دیتابیس متصل نمی‌شود.

6. **Uniform Interface (رابط یکنواخت)**  
   این اصل چهار زیرمجموعه دارد: شناسایی resourceها با URI، دستکاری resourceها از طریق representationها، پیام‌های self-descriptive و HATEOAS. همه APIها باید از یک الگوی ثابت پیروی کنند. در کتابخانه ما، همه resourceها با `/api/<resource-name>/` شناسایی می‌شوند و همه با JSON کار می‌کنند.

7. **شناسایی Resourceها با URI**  
   هر resource در REST یک URI منحصربه‌فرد دارد. در کتابخانه ما resourceها و URIهایشان به این صورت است:
   - `/api/books/` → مجموعه کتاب‌ها
   - `/api/books/1/` → کتاب شماره ۱
   - `/api/authors/` → مجموعه نویسندگان
   - `/api/authors/3/books/` → کتاب‌های نویسنده شماره ۳
   - `/api/loans/` → مجموعه امانت‌ها
   هر URI یک resource را مشخص می‌کند و با اسامی جمع (books, authors) نام‌گذاری می‌شود.

8. **Resource Manipulation via Representations**  
   در REST، کلاینت resourceها را مستقیماً دستکاری نمی‌کند، بلکه یک representation (نمایش) از آن‌ها را می‌فرستد. سرور وضعیت جدید را بر اساس آن representation اعمال می‌کند. مثلاً برای به‌روزرسانی یک کتاب، کلاینت یک JSON به این شکل به `PUT /api/books/1/` می‌فرستد:
   ```json
   {
       "title": "هری پاتر و سنگ جادو",
       "author": "ج. ک. رولینگ",
       "price": 250000
   }
   ```
   این JSON یک representation از وضعیت جدید منبع است و لزوماً شامل تمام فیلدها نیست (در PATCH) یا شامل همه است (در PUT).

9. **Self-Descriptive Messages**  
   هر پیام HTTP (درخواست و پاسخ) باید به‌قدر کافی اطلاعات در خود داشته باشد تا قابل فهم باشد. هدر `Content-Type` مشخص می‌کند که بدنه به چه فرمتی است (مثلاً `application/json`). هدر `Accept` مشخص می‌کند که کلاینت چه فرمتی را می‌پذیرد. خود URI مشخص می‌کند که روی کدام resource کار می‌شود.

10. **HATEOAS (Hypermedia as the Engine of Application State)**  
    یک اصل مهم REST که می‌گوید پاسخ API باید شامل لینک‌هایی باشد که کلاینت را به سایر اکشن‌های ممکن هدایت می‌کند. در کتابخانه ما، وقتی یک کتاب را دریافت می‌کنیم، پاسخ به این شکل است:
    ```json
    {
        "id": 1,
        "title": "هری پاتر و سنگ جادو",
        "links": {
            "self": "/api/books/1/",
            "author": "/api/authors/1/",
            "reviews": "/api/books/1/reviews/",
            "loan": "/api/loans/?book=1"
        }
    }
    ```
    این لینک‌ها به کلاینت می‌گویند که بعد از دیدن این کتاب می‌تواند به سراغ نویسنده برود یا نظرها را ببیند یا کتاب را امانت بگیرد. این کار API را self-discoverable می‌کند.

11. **پیاده‌سازی HATEOAS در Django REST Framework**  
    در DRF می‌توانیم با استفاده از `HyperlinkedRelatedField` و `HyperlinkedIdentityField` لینک‌های HATEOAS را در Serializer تولید کنیم. یک Serializer با لینک‌های hyperlinked تعریف می‌کنیم:
    ```python
    class BookSerializer(serializers.HyperlinkedModelSerializer):
        author = serializers.HyperlinkedRelatedField(
            view_name='author-detail',
            read_only=True
        )
        reviews = serializers.HyperlinkedRelatedField(
            view_name='review-list',
            read_only=True,
            many=True
        )
        class Meta:
            model = Book
            fields = ['id', 'title', 'author', 'reviews', 'url']
    ```
    در `urls.py` view_nameها را با `basename` تنظیم می‌کنیم تا لینک‌ها به درستی تولید شوند.

12. **طراحی یک API کاملاً RESTful برای کتابخانه**  
    جدول زیر نشان می‌دهد هر endpoint چه resourceای را مشخص می‌کند:

| Method | Endpoint | توضیح |
|--------|----------|-------|
| GET | `/api/books/` | لیست همه کتاب‌ها |
| POST | `/api/books/` | ایجاد کتاب جدید |
| GET | `/api/books/{id}/` | جزئیات یک کتاب |
| PUT | `/api/books/{id}/` | جایگزینی کامل یک کتاب |
| PATCH | `/api/books/{id}/` | به‌روزرسانی جزئی یک کتاب |
| DELETE | `/api/books/{id}/` | حذف یک کتاب |
| GET | `/api/books/{id}/reviews/` | نظرهای یک کتاب |
| POST | `/api/books/{id}/reviews/` | ثبت نظر برای کتاب |

    هر endpoint از Uniform Interface پیروی می‌کند و با HTTP Methodهای استاندارد کار می‌کند.

13. **تست Statelessness با ارسال درخواست‌های متوالی**  
    با استفاده از `httpie` یا `curl`، دو درخواست پشت سر هم به API می‌فرستیم:
    ```bash
    curl -H "Authorization: Token abc123" http://127.0.0.1:8000/api/books/
    curl -H "Authorization: Token abc123" http://127.0.0.1:8000/api/books/1/
    ```
    هر درخواست مستقل از درخواست قبلی پردازش می‌شود. اگر درخواست اول یک کتاب اضافه کرده بود، درخواست دوم نمی‌توانست از روی session اول بداند. هر بار باید تمام اطلاعات (توکن، body، هدف) همراه درخواست باشد.

14. **تست Cacheability با هدرهای HTTP**  
    با `curl -I` هدرهای پاسخ را بررسی می‌کنیم:
    ```bash
    curl -I http://127.0.0.1:8000/api/books/
    ```
    در هدرها به دنبال `Cache-Control` می‌گردیم. در DRF با `@cache_page` می‌توانیم کش کردن را فعال کنیم:
    ```python
    from django.views.decorators.cache import cache_page
    from django.utils.decorators import method_decorator

    class BookList(generics.ListAPIView):
        queryset = Book.objects.all()
        serializer_class = BookSerializer

        @method_decorator(cache_page(60 * 30))
        def get(self, request, *args, **kwargs):
            return super().get(request, *args, **kwargs)
    ```
    بعد از اولین درخواست، پاسخ در Cache ذخیره می‌شود و درخواست دوم سریع‌تر پاسخ می‌دهد.

15. **شناسایی Resourceهای تو در تو و Layered Design**  
    یک resource می‌تواند زیرمجموعه resource دیگر باشد. در کتابخانه ما، نظرها زیرمجموعه کتاب‌ها هستند و با URI تو‌در‌تو مشخص می‌شوند. از طرفی، امانت‌ها به کاربر و کتاب وابسته هستند. در طراحی لایه‌ای، مدل‌ها را در یک لایه، Serializerها را در لایه بعدی و Viewها را در لایه بالایی قرار می‌دهیم. هر لایه فقط با لایه مجاور ارتباط دارد. مثلاً View از Serializer استفاده می‌کند و Serializer از Model.