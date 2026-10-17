## سرفصل: Validation Errors

### منابع آموزشی

**مستندات رسمی DRF:**
- [Serializers — اعتبارسنجی در Serializerها، فیلد-سطح و object-سطح و custom validators](https://www.django-rest-framework.org/api-guide/serializers/#validation)
- [Fields — پارامترهای اعتبارسنجی فیلدها مثل max_length، validators و error_messages](https://www.django-rest-framework.org/api-guide/fields/)

**مستندات رسمی Django:**
- [Validators — مرجع کامل validators داخلی Django و نحوه ساخت custom validator](https://django.readthedocs.io/en/5.2.x/ref/validators.html)

---
### تمرین عملی (روی یک کار واقعی)

**مثال واقعی:** در پروژه `mysite` اپلیکیشن «فروشگاه کتاب» را داریم. می‌خواهیم برای API ثبت کتاب و ثبت سفارش، اعتبارسنجی‌های دقیق (field-level و object-level) پیاده‌سازی کنیم. همچنین یک Validator کلاس‌بندی شده برای قیمت می‌سازیم و خطاهای اعتبارسنجی را با فرمت یکسان به کلاینت برمی‌گردانیم.

**تیتر کارها و توضیح هر کدام در این مثال:**

1. **شناخت اعتبارسنجی در Serializer و متد `is_valid()`**  
   متد `is_valid(raise_exception=True)` بررسی می‌کند که آیا داده‌های ارسالی به Serializer معتبرند یا نه. اگر `raise_exception=True` باشد، در صورت نامعتبر بودن داده‌ها یک `ValidationError` raise می‌کند. این متد شامل سه لایه اعتبارسنجی است: فیلد-سطح (validate_<field_name>)، object-سطح (validate()) و validators. بررسی می‌کنیم که `errors` در Serializer چه ساختاری دارد.

2. **اعتبارسنجی فیلد-سطح برای فیلد `price`**  
   در Serializer `BookSerializer`، یک متد `validate_price(self, value)` اضافه می‌کنیم:
   ```python
   def validate_price(self, value):
       if value < 1000:
           raise serializers.ValidationError("قیمت کتاب نمی‌تواند کمتر از ۱۰۰۰ تومان باشد.")
       if value > 50_000_000:
           raise serializers.ValidationError("قیمت کتاب نمی‌تواند بیش از ۵۰ میلیون تومان باشد.")
       return value
   ```
   این متد مطمئن می‌شود قیمت در بازه منطقی قرار دارد.

3. **اعتبارسنجی فیلد-سطح برای فیلد `email`**  
   در Serializer `CustomerSerializer`، یک متد `validate_email(self, value)` اضافه می‌کنیم که بررسی کند ایمیل از یک دامنه معتبر است:
   ```python
   def validate_email(self, value):
       if not value.endswith(('.com', '.ir', '.org')):
           raise serializers.ValidationError("ایمیل باید با دامنه معتبر پایان یابد.")
       return value
   ```
   این متد از regex هم می‌تواند استفاده کند.

4. **اعتبارسنجی object-سطح: بررسی تداخل تاریخ‌ها**  
   در Serializer سفارش `OrderSerializer`، متد `validate(self, data)` را پیاده‌سازی می‌کنیم:
   ```python
   def validate(self, data):
       if data['checked_in'] and data['checked_out']:
           if data['checked_in'] >= data['checked_out']:
               raise serializers.ValidationError(
                   "تاریخ ورود باید قبل از تاریخ خروج باشد."
               )
       return data
   ```
   این اعتبارسنجی به فیلد خاصی مربوط نیست، بلکه به رابطه بین چند فیلد مربوط می‌شود. خطای اینجا به کلید `non_field_errors` اضافه می‌شود.

5. **ساخت یک Custom Validator کلاس‌بندی شده برای قیمت**  
   یک کلاس `PriceValidator` به عنوان `Validator` می‌سازیم:
   ```python
   class PriceValidator:
       def __init__(self, min_value=1000, max_value=50_000_000):
           self.min_value = min_value
           self.max_value = max_value

       def __call__(self, value):
           if value < self.min_value:
               raise serializers.ValidationError(f"قیمت نمی‌تواند از {self.min_value} کمتر باشد.")
           if value > self.max_value:
               raise serializers.ValidationError(f"قیمت نمی‌تواند از {self.max_value} بیشتر باشد.")

       def __repr__(self):
           return f"PriceValidator(min={self.min_value}, max={self.max_value})"
   ```
   سپس از این کلاس در فیلد `price` استفاده می‌کنیم:
   ```python
   price = serializers.DecimalField(
       max_digits=10, decimal_places=0,
       validators=[PriceValidator(min_value=2000)]
   )
   ```

6. **ساخت Custom Validator تابعی برای `isbn`**  
   یک تابع ساده به نام `validate_isbn` می‌نویسیم که بررسی کند ISBN طول ۱۳ رقم دارد و فقط شامل اعداد است:
   ```python
   def validate_isbn(value):
       if not value.isdigit() or len(value) != 13:
           raise serializers.ValidationError("ISBN باید ۱۳ رقم عددی باشد.")
   ```
   این Validator را به فیلد `isbn` در Serializer اضافه می‌کنیم.

7. **سفارشی‌سازی پیام خطا با `default_error_messages`**  
   اگر یک فیلد DRF داریم، می‌توانیم `error_messages` را در تعریف فیلد تنظیم کنیم:
   ```python
   email = serializers.EmailField(
       error_messages={
           'invalid': 'ایمیل واردشده معتبر نیست. لطفاً یک ایمیل معتبر وارد کنید.',
           'blank': 'وارد کردن ایمیل الزامی است.',
           'required': 'فیلد ایمیل را خالی نگذارید.',
       }
   )
   ```
   یا در کلاس Serializer با `default_error_messages` متادیتا، پیام‌های خطا را به فارسی سفارشی می‌کنیم.

8. **پیاده‌سازی Unique Validator برای `isbn`**  
   اگر کاربر کتابی با `isbn` تکراری ثبت کند، خطای IntegrityError دیتابیس رخ می‌دهد. برای جلوگیری، متد `validate_isbn` را در Serializer می‌نویسیم که بررسی کند این isbn قبلاً وجود ندارد:
   ```python
   def validate_isbn(self, value):
       if Book.objects.filter(isbn=value).exclude(pk=self.instance.pk if self.instance else None).exists():
           raise serializers.ValidationError("کتابی با این شماره ISBN قبلاً ثبت شده است.")
       return value
   ```

9. **مدیریت خطاهای اعتبارسنجی در `exception_handler` جهانی**  
   در `custom_exception_handler`، اگر `ValidationError` باشد، ساختار خطا را به‌صورت زیر استاندارد می‌کنیم:
   ```python
   if isinstance(exc, ValidationError):
       response.data = {
           'error_code': 'validation_error',
           'messages': response.data,
           'status_code': 400,
       }
   ```
   این کار باعث می‌شود همه خطاهای اعتبارسنجی ساختار یکسانی داشته باشند.

10. **تشخیص خطاهای فیلد-سطح در مقابل non-field خطاها**  
    وقتی `validate()` خطا می‌دهد، خطا به `non_field_errors` اضافه می‌شود. وقتی `validate_<field>()` خطا می‌دهد، خطا در کلید مربوط به آن فیلد قرار می‌گیرد. در `custom_exception_handler`، بررسی می‌کنیم که آیا `response.data` یک دیکشنری با کلیدهای فیلدهاست یا یک لیست (برای non-field errors). بر این اساس، ساختار پاسخ را تنظیم می‌کنیم.

11. **استفاده از `UniqueValidator` و `UniqueTogetherValidator`**  
    DRF دارای Validatorهای آماده `UniqueValidator` و `UniqueTogetherValidator` است:
    ```python
    from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

    class BookSerializer(serializers.ModelSerializer):
        isbn = serializers.CharField(
            validators=[UniqueValidator(queryset=Book.objects.all())]
        )

        class Meta:
            validators = [
                UniqueTogetherValidator(
                    queryset=Book.objects.all(),
                    fields=['title', 'author']
                )
            ]
    ```
    این کار از ثبت کتاب تکراری با عنوان و نویسنده یکسان جلوگیری می‌کند.

12. **تست Validation Errors با APIClient**  
    یک تست جامع می‌نویسیم:
    ```python
    def test_validation_errors(self):
        # قیمت کمتر از حد مجاز
        response = self.client.post('/api/books/', {'price': 500, ...}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('price', response.data['messages'])

        # ایزبن تکراری
        response = self.client.post('/api/books/', {'isbn': '1234567890123', ...}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('این ISBN قبلاً ثبت شده است', str(response.data))
    ```
    بررسی می‌کنیم که فرمت خطا برای کلاینت قابل فهم و استاندارد است.

13. **پیام خطای چندزبانه (Internationalization)**  
    برای تبدیل پیام‌های خطا به فارسی، از `django.utils.translation` استفاده می‌کنیم:
    ```python
    from django.utils.translation import gettext_lazy as _

    class CustomDetailSerializer(serializers.Serializer):
        price = serializers.DecimalField(
            max_digits=10, decimal_places=0,
            error_messages={
                'invalid': _('قیمت واردشده معتبر نیست.'),
                'max_value': _('قیمت نمی‌تواند بیش از ۵۰ میلیون باشد.'),
            }
        )
    ```
    این روش برای پروژه‌های چندزبانه ضروری است.

14. **اعتبارسنجی شرطی (Conditional Validation)**  
    اگر یک فیلد فقط در شرایط خاصی الزامی است، در متد `validate()` بررسی می‌کنیم. مثلاً برای خرید آنلاین، فیلد `card_number` اگر `payment_method` برابر `online` بود الزامی است:
    ```python
    def validate(self, data):
        if data.get('payment_method') == 'online' and not data.get('card_number'):
            raise serializers.ValidationError({'card_number': 'برای پرداخت آنلاین، شماره کارت الزامی است.'})
        return data
    ```
    این نوع اعتبارسنجی شیء-سطح به‌صورت شرطی روی فیلدها خطا می‌دهد.

15. **بررسی رفتار Serializer در زمان `partial_update` (PATCH)**  
    وقتی از `partial=True` استفاده می‌کنیم (برای PATCH)، اعتبارسنجی فقط روی فیلدهای ارسال‌شده انجام می‌شود. تست می‌کنیم که یک PATCH با قیمت جدید بدون ارسال `title` کار می‌کند و اعتبارسنجی `title` را رد نمی‌کند. همچنین بررسی می‌کنیم که Validatorهای فیلد `isbn` فقط روی فیلدهای موجود در داده اعمال می‌شوند.