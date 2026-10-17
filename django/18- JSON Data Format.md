## سرفصل: JSON Data Format

### منابع آموزشی

**مستندات رسمی و مراجع استاندارد:**
- [JSON.org — معرفی کامل JSON، syntax، ساختار object و array، انواع داده](https://www.json.org/json-en.html)
- [Wikipedia – JSON — تاریخچه، syntax، مقایسه با XML و کاربردها](https://en.wikipedia.org/wiki/JSON)
- [ECMA-404 — استاندارد رسمی JSON توسط Ecma](https://ecma-international.org/publications-and-standards/standards/ecma-404/)

**مستندات JSON Schema:**
- [JSON Schema — مستند رسمی: تعریف Schema، Validation، انواع داده و قالب‌ها](https://json-schema.org/learn/getting-started-step-by-step)
- [JSON Schema Reference — مرجع کامل کلمات کلیدی: type, properties, required, enum, pattern](https://json-schema.org/understanding-json-schema/)

**مستندات Python:**
- [Python json module — مستند رسمی: json.dumps, json.loads, JSONEncoder, JSONDecoder](https://docs.python.org/3/library/json.html)

**مستندات Django REST Framework:**
- [DRF – Parsers — نحوه Parse کردن JSON در DRF با JSONParser](https://www.django-rest-framework.org/api-guide/parsers/)
- [DRF – Renderers — نحوه خروجی JSON با JSONRenderer و Browsable API](https://www.django-rest-framework.org/api-guide/renderers/)

---

### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` و اپلیکیشن «کتابخانه دیجیتال»، تبادل داده بین کلاینت و سرور با فرمت JSON انجام می‌شود. در این تمرین، JSON را از پایه می‌نویسیم، با کتابخانه `json` پایتون کار می‌کنیم، Serialization و Deserialization را انجام می‌دهیم، ساختارهای تو‌در‌تو را مدیریت می‌کنیم و با JSON Schema داده‌ها را اعتبارسنجی می‌کنیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت JSON Syntax و انواع داده**  
   JSON (JavaScript Object Notation) یک فرمت سبک برای تبادل داده است که بر اساس زیرمجموعه‌ای از JavaScript تعریف شده است. انواع داده در JSON عبارتند از:
   - **String**: `"متن"` (باید حتماً داخل دابل کوتیشن باشد)
   - **Number**: `42`, `3.14`, `-7` (اعداد صحیح و اعشاری، بدون تفاوت بین int و float)
   - **Boolean**: `true` یا `false`
   - **Null**: `null`
   - **Array**: `[1, 2, 3]` (لیست مرتب از مقادیر)
   - **Object**: `{"key": "value"}` (مجموعه‌ای از key/value pairها)
   
   توجه: کوتیشن تکی ('') در JSON مجاز نیست و کلیدهای object حتماً باید داخل دابل کوتیشن باشند.

2. **نوشتن JSON به‌صورت دستی برای یک کتاب**  
   یک کتاب را به‌صورت دستی در قالب JSON می‌نویسیم:
   ```json
   {
       "id": 1,
       "title": "هری پاتر و سنگ جادو",
       "isbn": "978-0747532699",
       "price": 250000.00,
       "in_stock": true,
       "published_date": "1997-06-26",
       "author": {
           "id": 1,
           "name": "ج. ک. رولینگ",
           "birth_year": 1965
       },
       "tags": ["fantasy", "magic", "adventure"],
       "reviews_count": 0
   }
   ```
   این JSON شامل انواع مختلف داده و یک ساختار تو‌در‌تو (author درون book) است.

3. **Serialization — تبدیل Python Object به JSON**  
   Serialization فرآیند تبدیل یک شیء پایتون (مثل dict, list, object) به رشته JSON است. از `json.dumps()` استفاده می‌کنیم:
   ```python
   import json

   book = {
       "id": 1,
       "title": "هری پاتر و سنگ جادو",
       "price": 250000.00,
       "in_stock": True,
       "tags": ["fantasy", "magic"]
   }

   json_string = json.dumps(book, ensure_ascii=False, indent=4)
   print(json_string)
   ```
   پارامتر `ensure_ascii=False` اجازه می‌دهد کاراکترهای فارسی بدون \u escape چاپ شوند. پارامتر `indent=4` خروجی را خوانا می‌کند. `json.dumps()` برای دیکشنری‌ها و لیست‌های پایتون به‌خوبی کار می‌کند اما برای اشیاء سفارشی نیاز به Encoder دارد.

4. **Deserialization — تبدیل JSON به Python Object**  
   Deserialization فرآیند معکوس است: تبدیل رشته JSON به دیکشنری یا لیست پایتون. از `json.loads()` استفاده می‌کنیم:
   ```python
   import json

   json_string = '{"id": 1, "title": "هری پاتر", "price": 250000, "in_stock": true}'
   book_dict = json.loads(json_string)

   print(book_dict["title"])       # هری پاتر
   print(type(book_dict["price"])) # <class 'int'>
   print(book_dict["in_stock"])    # True (تبدیل به bool پایتون شده)
   ```
   توجه کنید که `true` و `false` در JSON به `True` و `False` پایتون تبدیل می‌شوند و `null` به `None`.

5. **کار با فایل‌های JSON — json.dump و json.load**  
   برای خواندن و نوشتن مستقیم از/به فایل از `json.dump()` و `json.load()` استفاده می‌کنیم:
   ```python
   import json

   books = [
       {"id": 1, "title": "هری پاتر", "price": 250000},
       {"id": 2, "title": "ارباب حلقه‌ها", "price": 350000}
   ]

   # نوشتن به فایل
   with open("books.json", "w", encoding="utf-8") as f:
       json.dump(books, f, ensure_ascii=False, indent=4)

   # خواندن از فایل
   with open("books.json", "r", encoding="utf-8") as f:
       loaded_books = json.load(f)

   print(len(loaded_books))  # 2
   ```
   `json.dump()` مستقیماً به شیء فایل می‌نویسد و `json.load()` از شیء فایل می‌خواند.

6. **مدیریت ساختارهای تو‌در‌تو (Nested JSON)**  
   داده‌های واقعی اغلب تو‌در‌تو هستند. یک کتاب با نویسنده و نظرات:
   ```python
   import json

   book_with_details = {
       "id": 1,
       "title": "هری پاتر و سنگ جادو",
       "author": {
           "name": "ج. ک. رولینگ",
           "bio": "نویسنده انگلیسی"
       },
       "reviews": [
           {"user": "ali", "rating": 5, "comment": "عالی بود"},
           {"user": "sara", "rating": 4, "comment": "خوب بود"}
       ],
       "metadata": {
           "page_count": 309,
           "language": "en",
           "translations": ["fa", "ar", "fr"]
       }
   }

   # دسترسی به مقادیر تو‌در‌تو
   print(book_with_details["author"]["name"])
   print(book_with_details["reviews"][0]["rating"])
   print(book_with_details["metadata"]["translations"][1])
   ```
   برای دسترسی به مقادیر تو‌در‌تو از chain indexing استفاده می‌کنیم. هر سطح از nesting با یک براکت جدید باز می‌شود.

7. **JSON Schema Basics — تعریف Schema برای کتاب**  
   JSON Schema یک زبان برای توصیف ساختار JSON است. با آن می‌توانیم مشخص کنیم یک JSON معتبر چه فیلدهایی باید داشته باشد. یک Schema برای کتاب:
   ```json
   {
       "$schema": "http://json-schema.org/draft-07/schema#",
       "title": "Book",
       "type": "object",
       "properties": {
           "id": {"type": "integer", "minimum": 1},
           "title": {"type": "string", "minLength": 1},
           "isbn": {"type": "string", "pattern": "^[0-9-]{10,17}$"},
           "price": {"type": "number", "minimum": 0},
           "in_stock": {"type": "boolean"},
           "author": {
               "type": "object",
               "properties": {
                   "id": {"type": "integer"},
                   "name": {"type": "string"}
               },
               "required": ["name"]
           }
       },
       "required": ["id", "title", "price", "author"]
   }
   ```
   کلمه کلیدی `required` فیلدهای اجباری را مشخص می‌کند. `type` نوع داده را تعیین می‌کند. `pattern` یک regex برای اعتبارسنجی رشته است. `minimum` و `maximum` محدوده اعداد را مشخص می‌کنند.

8. **اعتبارسنجی JSON با استفاده از JSON Schema**  
   با کتابخانه `jsonschema` پایتون می‌توانیم JSON را اعتبارسنجی کنیم:
   ```python
   import json
   import jsonschema
   from jsonschema import validate

   schema = {
       "type": "object",
       "properties": {
           "id": {"type": "integer"},
           "title": {"type": "string"},
           "price": {"type": "number", "minimum": 0}
       },
       "required": ["id", "title"]
   }

   # JSON معتبر
   valid_book = {"id": 1, "title": "کتاب", "price": 100000}
   validate(instance=valid_book, schema=schema)  # بدون خطا

   # JSON نامعتبر (فیلد title وجود ندارد)
   invalid_book = {"id": 1, "price": 50000}
   try:
       validate(instance=invalid_book, schema=schema)
   except jsonschema.exceptions.ValidationError as e:
       print(f"خطای اعتبارسنجی: {e.message}")
   ```
   نصب کتابخانه: `pip install jsonschema`. `validate()` اگر JSON معتبر باشد `None` برمی‌گرداند و اگر نامعتبر باشد `ValidationError` پرتاب می‌کند.

9. **Serialization سفارشی با JSONEncoder**  
   وقتی می‌خواهیم اشیاء پایتونی که قابل سریالایز نیستند (مثل datetime, Decimal, Model objects) را به JSON تبدیل کنیم، باید از `JSONEncoder` سفارشی استفاده کنیم:
   ```python
   import json
   from datetime import datetime
   from decimal import Decimal

   class CustomEncoder(json.JSONEncoder):
       def default(self, obj):
           if isinstance(obj, datetime):
               return obj.isoformat()
           if isinstance(obj, Decimal):
               return float(obj)
           if isinstance(obj, set):
               return list(obj)
           return super().default(obj)

   data = {
       "title": "کتاب",
       "created_at": datetime.now(),
       "price": Decimal("250000.50"),
       "tags": {"fantasy", "magic"}
   }

   json_string = json.dumps(data, cls=CustomEncoder, ensure_ascii=False, indent=4)
   print(json_string)
   ```
   متد `default()` باید شیء غیرقابل سریالایز را به نوع قابل سریالایز تبدیل کند یا خطا بدهد.

10. **Serialization و Deserialization در Django REST Framework**  
    در DRF، Serializerها به‌طور خودکار JSON را به Python dict و بالعکس تبدیل می‌کنند:
    ```python
    from rest_framework import serializers

    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ['id', 'title', 'price', 'is_available']

    # Serialization: Book object → JSON
    book = Book.objects.get(id=1)
    serializer = BookSerializer(book)
    json_data = serializer.data  # یک OrderedDict (قابل تبدیل به JSON با json.dumps)

    # Deserialization: JSON → Book object
    json_input = '{"title": "کتاب جدید", "price": 150000, "is_available": true}'
    serializer = BookSerializer(data=json.loads(json_input))
    if serializer.is_valid():
        book = serializer.save()  # ایجاد کتاب جدید در دیتابیس
    ```
    DRF `Serializer` متد `is_valid()` را برای اعتبارسنجی داده‌ها و `save()` را برای ذخیره‌سازی فراهم می‌کند.

11. **مدیریت Null و Missing Fields در JSON**  
    در JSON، `null` به معنی عدم وجود مقدار است و عدم حضور یک فیلد به معنی وجود نداشتن آن فیلد است. تفاوت این دو در Deserialization مهم است:
    ```python
    import json

    # فیلد price وجود ندارد
    data1 = '{"id": 1, "title": "کتاب"}'

    # فیلد price وجود دارد اما null است
    data2 = '{"id": 1, "title": "کتاب", "price": null}'

    dict1 = json.loads(data1)  # {'id': 1, 'title': 'کتاب'}
    dict2 = json.loads(data2)  # {'id': 1, 'title': 'کتاب', 'price': None}

    print("price" in dict1)  # False
    print("price" in dict2)  # True
    print(dict2["price"])    # None
    ```
    در DRF، `allow_null=True` در فیلد Serializer اجازه می‌دهد مقدار null معتبر باشد و `required=False` اجازه می‌دهد فیلد در ورودی وجود نداشته باشد.

12. **تبدیل QuerySet به JSON با Django's Serializer**  
    خود Django یک serializer داخلی برای تبدیل QuerySet به JSON دارد:
    ```python
    from django.core.serializers import serialize
    import json

    books = Book.objects.all()
    json_data = serialize('json', books, indent=4)
    # خروجی: "[{"model": "shop.book", "pk": 1, "fields": {"title": "...", ...}}]"

    # برای کنترل بیشتر، از values() استفاده می‌کنیم
    books_list = list(Book.objects.values('id', 'title', 'price'))
    json_string = json.dumps(books_list, ensure_ascii=False, indent=4)
    ```
    `serialize('json', ...)` خروجی شامل `model` و `pk` و `fields` می‌دهد. اما روش دوم با `values()` و `json.dumps()` کنترل بیشتری روی ساختار خروجی دارد.

13. **کار با JSON Lines (NDJSON)**  
    JSON Lines فرمتی است که هر خط یک JSON object مستقل است. برای داده‌های حجیم و log files بسیار مناسب است:
    ```python
    import json

    books = [
        {"id": 1, "title": "هری پاتر"},
        {"id": 2, "title": "ارباب حلقه‌ها"}
    ]

    # نوشتن به صورت JSON Lines
    with open("books.jsonl", "w", encoding="utf-8") as f:
        for book in books:
            f.write(json.dumps(book, ensure_ascii=False) + "\n")

    # خواندن JSON Lines
    with open("books.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            book = json.loads(line.strip())
            print(book["title"])
    ```
    هر خط یک JSON کامل است. این فرمت حافظه کمتری مصرف می‌کند و برای stream پردازش مناسب‌است.

14. **تست JSON در DRF Browsable API**  
    DRF یک Browsable API ارائه می‌دهد که در مرورگر قابل مشاهده است. وقتی به `http://127.0.0.1:8000/api/books/` در مرورگر می‌رویم:
    - بخش بالایی: فرم HTML برای آزمایش POST, PUT, PATCH
    - بخش پایینی: داده JSON خام (Raw data)
    - می‌توانیم بین `application/json` و `text/html` در هدر `Accept` سوئیچ کنیم
    
    با `curl -H "Accept: application/json"` فقط JSON دریافت می‌کنیم.
    با `curl -H "Accept: text/html"` نسخه HTML (Browsable API) دریافت می‌کنیم.
    
    این ویژگی به توسعه‌دهنده کمک می‌کند JSON تولیدی را مستقیماً در مرورگر ببیند و اعتبارسنجی کند.