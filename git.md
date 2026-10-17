## تسک ۰: آماده‌سازی محیط

**هدف:** نصب و تنظیم اولیه Git

**گام‌ها:**
```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --list --show-origin
```

**تأمل:**
- تنظیمات global و local چه تفاوتی دارند؟
- چرا email در Git مهم است؟
- اگر روی یک پروژه بخواهی نام دیگری استفاده کنی چه می‌کنی؟

**معیار پذیرش:**
- `git config --list` نام و ایمیل را نشان دهد.
- شاخه پیش‌فرض `main` باشد.

---

## تسک ۱: اولین مخزن و چرخه پایه

**هدف:** درک working directory، staging area و repository

**گام‌ها:**
```bash
mkdir git-lab && cd git-lab
git init
git status
echo "# Git Lab" > README.md
git status
git add README.md
git status
git commit -m "docs: add README"
git log --oneline
```

**تأمل:**
- چرا Git سه ناحیه جدا دارد؟
- اگر فایل را مستقیم commit کنیم چه می‌شود؟
- `git add` دقیقاً چه کاری می‌کند؟

**معیار پذیرش:**
- اولین commit با پیام مشخص ثبت شده باشد.
- `git status` تمیز باشد.

---

## تسک ۲: دیدن تغییرات با diff

**هدف:** تشخیص تغییرات unstaged، staged و کل

**گام‌ها:**
```bash
echo "line 2" >> README.md
git diff
git add README.md
git diff --staged
git diff HEAD
git commit -m "docs: update README"
```

**تأمل:**
- `git diff` و `git diff --staged` چه زمانی استفاده می‌شوند؟
- چرا قبل از commit باید diff بگیری؟

**معیار پذیرش:**
- بتوانی تفاوت سه حالت را توضیح دهی.

---

## تسک ۳: add تعاملی

**هدف:** stage کردن بخشی از تغییرات

**گام‌ها:**
```bash
echo "line 3" >> README.md
echo "line 4" >> README.md
git add -p
# گزینه‌های y/n/s/e را تمرین کن
git commit -m "docs: add lines 3 and 4"
```

**تأمل:**
- چه زمانی `git add -p` نجات‌بخش است؟
- commitهای کوچک چه مزیتی دارند؟

**معیار پذیرش:**
- حداقل یک commit با stage انتخابی ساخته باشی.

---

## تسک ۴: نادیده گرفتن فایل‌ها با gitignore

**هدف:** جلوگیری از ورود فایل‌های غیرضروری

**گام‌ها:**
```bash
echo "SECRET=123" > .env
mkdir logs && echo "error" > logs/app.log
cat > .gitignore <<'EOF'
.env
logs/
node_modules/
*.log
EOF
git status
git status --ignored
git check-ignore -v .env
git add .gitignore
git commit -m "chore: add gitignore"
```

**تأمل:**
- اگر فایل `.env` قبلاً commit شده باشد، `.gitignore` آن را حذف می‌کند؟
- الگوهای `*.log` و `logs/` چه تفاوتی دارند؟

**معیار پذیرش:**
- `.env` و `logs/` در `git status` دیده نشوند.

---

## تسک ۵: حذف و جابجایی فایل‌ها

**هدف:** مدیریت فایل‌ها در Git

**گام‌ها:**
```bash
echo "temp" > old.txt
git add old.txt && git commit -m "chore: add old.txt"
git mv old.txt new.txt
git status
git rm new.txt
git commit -m "chore: rename and remove file"
```

**تأمل:**
- تفاوت `git rm` و `rm` معمولی چیست؟
- Git چگونه rename را تشخیص می‌دهد؟

**معیار پذیرش:**
- تاریخچه تغییرات فایل قابل ردیابی باشد.

---

## تسک ۶: تاریخچه و جستجو

**هدف:** پیدا کردن commit، نویسنده و تغییرات

**گام‌ها:**
```bash
git log --oneline --graph --decorate --all
git log -p
git log --stat
git log --author="Your Name"
git log --grep="README"
git log -S"line 3"
git show <hash>
git blame README.md
```

**تأمل:**
- `git log -S` چه کاری می‌کند؟
- `git blame` در code review چه کاربردی دارد؟

**معیار پذیرش:**
- بتوانی یک commit خاص را با hash پیدا و بررسی کنی.

---

## تسک ۷: برگرداندن تغییرات قبل از commit

**هدف:** لغو تغییرات working directory و staging

**گام‌ها:**
```bash
echo "bad change" >> README.md
git restore README.md
git status

echo "staged bad" >> README.md
git add README.md
git restore --staged README.md
git restore README.md

touch junk.txt
git clean -n
git clean -f
```

**تأمل:**
- `git restore` و `git restore --staged` چه تفاوتی دارند؟
- `git clean -f` چه خطری دارد؟

**معیار پذیرش:**
- فایل‌های ناخواسته بدون آسیب به تاریخچه پاک شوند.

---

## تسک ۸: اصلاح آخرین commit

**هدف:** amend کردن commit آخر

**گام‌ها:**
```bash
echo "forgotten" > forgotten.txt
git add forgotten.txt
git commit --amend --no-edit

git commit --amend -m "docs: better message"
git log --oneline
```

**تأمل:**
- چه زمانی amend ممنوع است؟
- اگر commit را push کرده باشی چه اتفاقی می‌افتد؟

**معیار پذیرش:**
- commit آخر شامل فایل فراموش‌شده و پیام جدید باشد.

---

## تسک ۹: revert و reset

**هدف:** برگرداندن commitهای ثبت‌شده

**گام‌ها:**
```bash
echo "feature 1" > f1.txt
git add f1.txt && git commit -m "feat: f1"

git revert <hash>
git log --oneline

git reset --soft HEAD~1
git status
git reset --mixed HEAD~1
git reset --hard HEAD~1
```

**تأمل:**
- `revert` چه تفاوتی با `reset` دارد؟
- چرا `reset --hard` روی شاخه مشترک خطرناک است؟

**معیار پذیرش:**
- بتوانی تفاوت سه حالت reset را توضیح دهی.

---

## تسک ۱۰: شاخه‌ها و merge

**هدف:** کار موازی با branch

**گام‌ها:**
```bash
git switch -c feature/login
echo "login" > login.txt
git add login.txt && git commit -m "feat: login"
git switch main
git merge feature/login
git branch -d feature/login
git log --oneline --graph --all
```

**تأمل:**
- fast-forward merge چیست؟
- چه زمانی merge commit ساخته می‌شود؟

**معیار پذیرش:**
- شاخه feature در main merge شده باشد.

---

## تسک ۱۱: حل تعارض merge

**هدف:** مدیریت conflict واقعی

**گام‌ها:**
```bash
# روی main
echo "main content" > conflict.txt
git add conflict.txt && git commit -m "main: conflict"

git switch -c feature/conflict
echo "feature content" > conflict.txt
git add conflict.txt && git commit -m "feature: conflict"

git switch main
git merge feature/conflict
# conflict رخ می‌دهد
cat conflict.txt
# فایل را ویرایش کن و markerها را بردار
git add conflict.txt
git commit -m "merge: resolve conflict"
```

**تأمل:**
- markerهای `<<<<<<<`، `=======`، `>>>>>>>` چه معنایی دارند؟
- `git merge --abort` چه زمانی استفاده می‌شود؟

**معیار پذیرش:**
- conflict بدون باقی‌ماندن marker حل شده باشد.

---

## تسک ۱۲: rebase مقدماتی

**هدف:** مرتب‌سازی تاریخچه

**گام‌ها:**
```bash
git switch -c feature/rebase
echo "rebase" > rebase.txt
git add rebase.txt && git commit -m "feat: rebase"

git switch main
echo "main new" > main-new.txt
git add main-new.txt && git commit -m "feat: main new"

git switch feature/rebase
git rebase main
git log --oneline --graph --all
```

**تأمل:**
- merge و rebase چه تفاوتی در تاریخچه ایجاد می‌کنند؟
- قانون طلایی rebase چیست؟

**معیار پذیرش:**
- تاریخچه feature روی main بازپخش شده باشد.

---

## تسک ۱۳: remote و GitHub

**هدف:** ارتباط با مخزن راه دور

**گام‌ها:**
```bash
# در GitHub یک repo خالی بساز
git remote add origin git@github.com:USERNAME/git-lab.git
git push -u origin main

# جای دیگر clone کن
cd ..
git clone git@github.com:USERNAME/git-lab.git git-lab-2
cd git-lab-2
git log --oneline

# یک تغییر بده
echo "remote change" >> README.md
git add README.md && git commit -m "docs: remote change"
git push

# در repo اول
cd ../git-lab
git fetch
git pull
```

**تأمل:**
- `git fetch` و `git pull` چه تفاوتی دارند؟
- `-u` در push چه می‌کند؟

**معیار پذیرش:**
- هر دو مخزن همگام باشند.

---

## تسک ۱۴: Pull Request و Code Review

**هدف:** شبیه‌سازی کار تیمی

**گام‌ها:**
```bash
git switch -c feature/profile
echo "profile" > profile.txt
git add profile.txt && git commit -m "feat: add profile"
git push -u origin feature/profile
# در GitHub یک PR باز کن
# یک نفر دیگر را reviewer کن
# comment بگذار، change request بده
# تغییر بده و push کن
# PR را merge کن
git switch main
git pull
git branch -d feature/profile
```

**تأمل:**
- merge commit، squash و rebase merge چه تفاوتی دارند؟
- چرا protected branch و required review مهم است؟

**معیار پذیرش:**
- یک PR کامل با review و merge داشته باشی.

---

## تسک ۱۵: همگام‌سازی fork

**هدف:** کار روی پروژه‌های open source

**گام‌ها:**
```bash
# fork کن
git clone git@github.com:USERNAME/forked-repo.git
cd forked-repo
git remote add upstream git@github.com:ORIGINAL/repo.git
git fetch upstream
git switch main
git merge upstream/main
git push origin main
```

**تأمل:**
- چرا upstream را اضافه می‌کنیم؟
- چه زمانی باید force push کنی؟ چرا خطرناک است؟

**معیار پذیرش:**
- fork با مخزن اصلی همگام شود.

---

## تسک ۱۶: stash

**هدف:** ذخیره موقت تغییرات

**گام‌ها:**
```bash
echo "wip" >> README.md
git stash push -m "wip readme"
git status
git stash list
git stash show -p stash@{0}
git stash pop

echo "wip2" >> README.md
touch untracked.txt
git stash push -u -m "with untracked"
git stash apply
git stash drop
```

**تأمل:**
- `pop` و `apply` چه تفاوتی دارند؟
- stash در چه سناریوهایی بهتر از commit موقت است؟

**معیار پذیرش:**
- تغییرات بدون commit موقت ذخیره و بازیابی شوند.

---

## تسک ۱۷: cherry-pick

**هدف:** برداشتن یک commit خاص

**گام‌ها:**
```bash
git switch -c feature/cherry
echo "a" > a.txt && git add a.txt && git commit -m "feat: a"
echo "b" > b.txt && git add b.txt && git commit -m "feat: b"
git log --oneline

git switch main
git cherry-pick <hash-of-feat-a>
git log --oneline
```

**تأمل:**
- cherry-pick چه زمانی خطرناک است؟
- چرا باعث commit تکراری می‌شود؟

**معیار پذیرش:**
- فقط commit مورد نظر روی main اعمال شود.