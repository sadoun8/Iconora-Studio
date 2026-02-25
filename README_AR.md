# Iconora Studio - Development Guide

## المرحلة الأولى ✅ (النواة الأساسية)

### المميزات المنجزة:
- [x] واجهة رئيسية احترافية
- [x] نظام التبويبات
- [x] تحويل الصور إلى ICO
- [x] اختيار أحجام متعددة
- [x] حفظ تلقائي في مجلد exports
- [x] دعم معايير Windows الأيقونات

### الملفات الرئيسية:
```
core/icon_converter.py     - محرك تحويل الأيقونات
ui/icon_tab.py             - واجهة تبويب الأيقونات
ui/main_window.py          - النافذة الرئيسية
main.py                    - نقطة الدخول
```

---

## 📥 التثبيت والتشغيل

### 1️⃣ تثبيت المكتبات:
```bash
pip install -r requirements.txt
```

### 2️⃣ تشغيل البرنامج:
```bash
python main.py
```

### 3️⃣ صنع ملف exe (اختياري):
```bash
pyinstaller --onefile --windowed --icon=assets/icons/app.ico main.py
```

---

## 🔮 المراحل القادمة

### المرحلة 2️⃣ – SVG Converter
- تحويل PNG إلى SVG
- معاينة مباشرة
- دعم الشفافية
- تغيير الألوان

### المرحلة 3️⃣ – Logo Designer
- محرر شعارات متقدم
- قوالب جاهزة
- أنماط (Minimal, Luxury, 3D)
- تأثيرات إضاءة

### المرحلة 4️⃣ – Signature Generator
- توقيعات عربية/إنجليزية
- تأثيرات حبر
- مقاسات مخصصة

### المرحلة 5️⃣ – أدوات إضافية
- إزالة الخلفية
- تأثيرات 3D
- ضغط الصور

---

## 🏗️ الهيكل المعماري

```
IconoraStudio/
├── main.py                 # نقطة الدخول
├── requirements.txt        # المكتبات المطلوبة
│
├── core/                   # محركات المعالجة
│   ├── __init__.py
│   ├── icon_converter.py   # تحويل الأيقونات ✅
│   ├── svg_converter.py    # قريباً
│   ├── logo_engine.py      # قريباً
│   ├── signature_engine.py # قريباً
│   └── background_remover.py # قريباً
│
├── ui/                     # واجهات المستخدم
│   ├── __init__.py
│   ├── main_window.py      # النافذة الرئيسية ✅
│   ├── icon_tab.py         # تبويب الأيقونات ✅
│   ├── logo_tab.py         # قريباً
│   ├── signature_tab.py    # قريباً
│   └── settings_tab.py     # قريباً
│
├── assets/
│   ├── fonts/              # خطوط مخصصة
│   ├── templates/          # قوالب جاهزة
│   └── icons/              # أيقونات التطبيق
│
└── exports/                # مجلد الملفات المُصدّرة
```

---

## 💡 نصائح التطوير

### إضافة ميزة جديدة:

1. أنشئ محرك في `core/`
2. أنشئ تبويب في `ui/`
3. أضفه إلى `main_window.py`
4. اختبره محلياً

### مثال - إضافة SVG Converter:

```python
# 1. في core/svg_converter.py
class SVGConverter:
    def convert_to_svg(self, image_path):
        # الكود هنا
        pass

# 2. في ui/svg_tab.py
class SVGTab(ctk.CTkFrame):
    def __init__(self, parent):
        # الكود هنا
        pass

# 3. في ui/main_window.py
svg_tab = tab_view.add("تحويل SVG")
svg_content = SVGTab(svg_tab)
svg_content.pack(fill="both", expand=True)
```

---

## 🎨 نظام الألوان

- **الخلفية الأساسية**: `#1a1a1a`
- **المظهر**: Dark theme
- **اللون الرئيسي**: Blue
- **حرف الخط الرئيسي**: Arial

---

## 📊 الإحصائيات

| المعيار | القيمة |
|--------|--------|
| لغة البرمجة | Python 3.12 |
| حجم الملف المتوقع (exe) | ~150 MB |
| استهلاك الذاكرة | ~100-150 MB |
| متوافق مع | Windows 7+ |

---

## 🐛 معالجة الأخطاء

جميع العمليات محمية من الأخطاء وتعرض رسائل خطأ واضحة.

---

## 📝 الملاحظات

- البرنامج يعمل بنمط **Modular** لسهولة الصيانة
- كل ميزة في ملف منفصل
- يمكن إضافة ميزات جديدة بسهولة
- الواجهة تدعم العربية بالكامل

---

**تم الإنشاء بواسطة Copilot | آخر تحديث: 25/02/2026**
