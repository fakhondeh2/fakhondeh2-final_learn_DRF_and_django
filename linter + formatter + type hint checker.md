## 🧐 Flake8 — پلیس کد

### 💡 مفهوم
Flake8 یک **لینتر** است؛ یعنی کد شما را **بدون اجرا** تحلیل می‌کند و خطاهای سبک نوشتاری، باگ‌های احتمالی و مشکلات ساختاری را پیدا می‌کند. این ابزار در واقع سه ابزار را زیر یک سقف جمع کرده: `pycodestyle` (بررسی سبک PEP 8)، `Pyflakes` (پیدا کردن خطاهای منطقی) و `mccabe` (بررسی پیچیدگی کد).

نصب: `pip install flake8`
اجرا: `flake8 path/to/file.py`

---

### تأمل در مثال: کد واقعی

به این کد نگاه کنید. Flake8 چه چیزهایی در آن می‌بیند؟

```python
import os
import sys

def calc(x,y):return x+y+1
```

**پیام‌های Flake8:**

| خطا | توضیح |
|------|-------|
| `F401 'os' imported but unused` | کتابخانه `os` را import کردی ولی استفاده نکردی |
| `F401 'sys' imported but unused` | این یکی هم همینطور |
| `E302 expected 2 blank lines, found 1` | قبل از تعریف تابع باید دو خط خالی باشد |
| `E231 missing whitespace after ','` | بعد از کاما در `x,y` فاصله ندادی |

**نکته تأملی:** Flake8 فقط **گزارش** می‌دهد. تصمیم نهایی با شماست. ولی این گزارش‌ها معمولاً واقعاً به کیفیت کد کمک می‌کنند.

---

### 🧠 شبیه‌سازی: تمرین «شکارچی خطا»

**سناریو:** شما یک Flake8 هستید. کد زیر را بخوانید و **بدون اجرا** بگویید چه خطاهایی دارد:

```python
import math

def Area_Circle(r):
    area = math.pi * r * r
    return area

def show_result():
    print(Area_Circle(5))
    print(Area_Circle(10) )
```

**تمرین:** حداقل **۴ خطا** پیدا کنید. به این موارد دقت کنید:
- آیا خطوط خالی کافی بین توابع وجود دارد؟
- آیا نام‌گذاری تابع با سبک پایتون (snake_case) همخوانی دارد؟
- آیا فاصله اضافی در `print(Area_Circle(10) )` دیده می‌شود؟


## 🎨 Black — آرایشگر کد

### 💡 مفهوم
Black یک **فرمتر** است؛ یعنی کد شما را **به‌صورت خودکار** مرتب می‌کند تا از یک سبک ثابت پیروی کند. Black «تسلیم‌ناپذیر» است — یعنی تنظیمات بسیار محدودی دارد و تقریباً هیچ چانه‌زنی نمی‌پذیرد. فلسفه‌اش این است: «سبک من، سبک نهایی است.»

نصب: `pip install black`
اجرا: `black path/to/file.py`
بررسی بدون تغییر: `black --check .`

---

### تأمل در مثال: قبل و بعد از Black

**کد قبل از فرمت (آشفته):**

```python
def calculate_sum(a,b,c):
    result=a+b+c;return result

def print_message(msg,times):
    for i in range(times): print(msg)
```

**کد بعد از فرمت با Black:**

```python
def calculate_sum(a, b, c):
    result = a + b + c
    return result


def print_message(msg, times):
    for i in range(times):
        print(msg)
```

**تغییرات اصلی:**
1. فاصله بعد از کاما اضافه شد: `a, b, c`
2. فاصله دور عملگرها: `a + b + c`
3. `;` حذف و دستورات جدا شدند
4. دو خط خالی بین توابع اضافه شد
5. حلقه `for` به بلوک چندخطی با تورفتگی تبدیل شد

**نکته تأملی:** Black **منطق کد را تغییر نمی‌دهد**؛ فقط **ظاهر** آن را مرتب می‌کند.

---

### 🧠 شبیه‌سازی: تمرین «آرایشگر کد»

**سناریو:** شما یک Black هستید. کد زیر را طوری بازنویسی کنید که از سبک Black پیروی کند:

```python
import json,os

def load_data(file_path):
    with open(file_path) as f: return json.load(f)

def process(data):
    result=[]
    for item in data: result.append(item["name"])
    return result
```

**تمرین:** کد بالا را در ذهن یا روی کاغذ **فرمت کنید**. به این موارد دقت کنید:
- جدا کردن importها در خطوط مختلف
- فاصله‌گذاری در `result=[]`
- دو خط خالی بین توابع
- تورفتگی مناسب در حلقه `for`


## 🛡️ Mypy — محافظ نوع

### 💡 مفهوم
Mypy یک **بررسی‌کننده نوع استاتیک** است؛ یعنی کد شما را **بدون اجرا** بررسی می‌کند و می‌بیند آیا نوع متغیرها و توابع با هم سازگارند یا نه. Mypy از **type hints** (راهنمای نوع) استفاده می‌کند — همان چیزهایی مثل `name: str` و `-> int` که در پایتون می‌نویسید.

نصب: `pip install mypy`
اجرا: `mypy path/to/file.py`

---

### تأمل در مثال: کد واقعی

**کد بدون type hint:**

```python
def greeting(name):
    return 'Hello ' + name
```

Mypy به‌صورت پیش‌فرض این تابع را **بررسی نمی‌کند**، چون type hint ندارد. یعنی اگر کسی `greeting(123)` صدا بزند، Mypy چیزی نمی‌گوید — ولی برنامه در زمان اجرا **کرش می‌کند**.

**کد با type hint:**

```python
def greeting(name: str) -> str:
    return 'Hello ' + name
```

حالا Mypy بررسی می‌کند:

```python
greeting(3)        # error: Argument 1 has incompatible type "int"; expected "str"
greeting(b'Alice') # error: Argument 1 has incompatible type "bytes"; expected "str"
greeting("World!") # ✅ بدون خطا
```

**نکته تأملی:** Mypy خطاها را **قبل از اجرا** پیدا می‌کند. این یعنی باگ‌ها را در همان مرحله کدنویسی می‌گیرید، نه وقتی که برنامه در دست کاربر است.

---

### 🧠 شبیه‌سازی: تمرین «محافظ نوع»

**سناریو:** شما یک Mypy هستید. کد زیر را بررسی کنید و بگویید کجا **type mismatch** وجود دارد:

```python
def add(a: int, b: int) -> int:
    return a + b

def get_user(user_id: int) -> str | None:
    if user_id == 1:
        return "Alice"
    return None

result1 = add(10, "20")
result2 = get_user(1)
result3 = get_user("abc")
print(result1, result2, result3)
```

**تمرین:** حداقل **۲ خطای نوع** پیدا کنید. به این موارد دقت کنید:
- در `add(10, "20")`، آرگومان دوم باید `int` باشد ولی `str` است
- در `get_user("abc")`، آرگومان باید `int` باشد ولی `str` است
- آیا `result1` با نوع خروجی `add` همخوانی دارد؟


## 📊 جمع‌بندی: تفاوت این سه ابزار

| ویژگی | Flake8 | Black | Mypy |
|--------|--------|-------|------|
| **نقش** | لینتر (پیدا کردن خطا) | فرمتر (مرتب کردن ظاهر) | بررسی‌کننده نوع |
| **کد را تغییر می‌دهد؟** | فقط گزارش می‌دهد | خودکار بازنویسی می‌کند | فقط گزارش می‌دهد |
| **مثل چه چیزی است؟** | پلیس کد | آرایشگر کد | محافظ نوع |
| **ابزار مشابه** | Pylint, Ruff | autopep8, Ruff | Pyright |
| **تمرکز** | سبک و باگ | ظاهر و یکدستی | نوع و سازگاری |

**توصیه عملی:** بهترین ترکیب این است که **هر سه** را در پروژه پایتون خود فعال کنید. Black کد را مرتب می‌کند، Flake8 خطاها را می‌گیرد و Mypy جلوی باگ‌های نوعی را قبل از اجرا می‌گیرد. اگر می‌خواهید همه را در یک ابزار داشته باشید، **Ruff** جایگزین سریع‌تری برای Flake8 و Black است، ولی Mypy هنوز استاندارد طلایی بررسی نوع است.

---

## 🧪 شبیه‌سازی نهایی: چرخه کامل

**سناریو:** شما کدی نوشته‌اید. می‌خواهید آن را با هر سه ابزار بررسی و اصلاح کنید.

```python
import json,sys

def LoadData(file_path: str) -> dict:
    with open(file_path) as f: return json.load(f)

def Process(data: dict) -> list:
    result = []
    for item in data: result.append(item["name"])
    return result

data = LoadData(123)
names = Process(data)
print(names)
```

**تمرین سه‌مرحله‌ای:**

| مرحله | ابزار | کار شما |
|-------|-------|---------|
| ۱ | **Flake8** | چه خطاهای سبکی و منطقی در کد وجود دارد؟ (import استفاده نشده، فاصله‌گذاری، خطوط خالی) |
| ۲ | **Mypy** | چه خطاهای نوعی وجود دارد؟ (آیا `LoadData(123)` درست است؟ آیا `data` از نوع `dict` است؟) |
| ۳ | **Black** | کد را طوری بازنویسی کنید که ظاهر آن استاندارد باشد |

**هدف نهایی:** درک این موضوع که این سه ابزار **مکمل یکدیگرند**. Flake8 می‌گوید «چه چیزی اشتباه است»، Mypy می‌گوید «چه چیزی از نظر نوع ناسازگار است» و Black می‌گوید «چطور آن را مرتب نشان دهم».