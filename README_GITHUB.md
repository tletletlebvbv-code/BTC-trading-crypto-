# تشغيل البوت مجانًا عبر GitHub (بلا VPS، بلا كمبيوتر)

هاد الطريقة تخدم بالكامل من المتصفح في الموبايل. صافي.

## 1) اعمل حساب GitHub (مجاني)

روح لـ **github.com** من متصفح الموبايل → **Sign up** → عمر إيميل + باسورد + username → أكد الإيميل.

## 2) اعمل Repository جديد

- بعد ما تدخل لحسابك، دوس على زر **"+"** فوق (أو "Create repository" من الصفحة الرئيسية)
- **Repository name**: اكتب مثلاً `btc-discord-bot`
- خليه **Public** (لازم يكون Public باش الخدمة تكون مجانية بلا حدود)
- دوس **Create repository**

## 3) ارفع الملفات

في صفحة الـ repo الفارغة:
- دوس **"uploading an existing file"** (رابط أزرق يبان في النص)
- ارفع هاد الملفات (حملتهم من الشات):
  - `bot_runner.py`
  - `requirements.txt`
  - المجلد `.github/workflows/bot.yml` — **مهم:** وقت الرفع، لازم يبقى المسار بالضبط `.github/workflows/bot.yml`. إذا الرفع بالسحب ما احتفظش بالمجلدات، دوس "Add file" → "Create new file"، واكتب في خانة الاسم `.github/workflows/bot.yml` (GitHub كيصنع المجلدات تلقائيًا من الاسم)، ثم الصق المحتوى ديال الملف جوه.
- دوس **Commit changes** (زر أخضر تحت) باش يحفظ

## 4) ضيف الـ Webhooks كـ "Secrets" (سرية، محميين)

- روح لـ **Settings** (فوق في صفحة الـ repo) → **Secrets and variables** → **Actions**
- دوس **New repository secret**
- **Name**: `WEBHOOK_URL_DEFAULT`
- **Secret**: الصق رابط الـ Discord webhook ديالك
- دوس **Add secret**

(إذا بغيتي webhook مختلفة لكل نوع، زيد بنفس الطريقة: `WEBHOOK_URL_PRICE`, `WEBHOOK_URL_SESSIONS`, `WEBHOOK_URL_NEWS`)

## 5) فعّل الـ Actions وجرب

- روح لـ تبويب **Actions** فوق في صفحة الـ repo
- إذا بان زر "I understand my workflows, go ahead and enable them" دوس عليه
- تلقى workflow اسمها **"BTC Discord Bot"** — دوس عليها
- دوس **Run workflow** (زر رمادي فالجهة اليمنى) → **Run workflow** تاني باش تجربها يدويًا فالحين
- استنى دقيقة، شوف الديسكورد — خاصك تشوف رسالة البرايس وصلت

من بعد هاد التجربة، البوت غادي يخدم وحدو أوتوماتيكيًا كل 5 دقايق، من غير ما تحتاج تدخل، ومن غير أي جهاز مشعل من عندك.

## ملاحظات

- **البرايس كل 5 دقايق** (مش كل دقيقة بالضبط) — هذا حد أدنى مفروض من GitHub مجانًا، ما نقدروش نتجاوزوه بلا خدمة مدفوعة.
- **GitHub Actions مجاني تمامًا** للـ repos العامة (Public)، بلا حدود تقريبًا لهاد النوع ديال الاستخدام الخفيف.
- إذا بغيتي توقف البوت مؤقتًا: روح لـ Actions → دوس على الـ workflow → "..." → **Disable workflow**.
- إذا حبيتي تبدل رابط الـ webhook: رجع لـ Settings → Secrets → دوس على السيكريت → Update.
