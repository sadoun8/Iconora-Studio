# 🚀 Iconora Studio - دليل التشغيل السريع

## الخطوة 1: التحقق من المتطلبات المثبتة

تأكد من تثبيت جميع المكتبات:

```bash
pip install customtkinter pillow cairosvg svgwrite tkinterdnd2
```

## الخطوة 2: تشغيل التطبيق

### الخيار 1: ملف التشغيل الرئيسي
```bash
python main.py
```

### الخيار 2: من خلال الكود مباشرة
```bash
python -c "from ui.main_window import MainWindow; import customtkinter as ctk; app = ctk.CTk(); MainWindow(app); app.mainloop()"
```

## الخطوة 3: اختبار كل مرحلة

### اختبار المرحلة الأولى (Icon Converter)
1. افتح التبويب "تحويل الأيقونات"
2. اختر صورة PNG
3. اختر الأحجام المطلوبة (16، 32، 48، 64 بكسل، إلخ)
4. انقر "تحويل إلى ICO" أو "تصدير PNG"

### اختبار المرحلة الثانية (SVG Converter)
1. افتح التبويب "تحويل SVG"
2. اختر صورة
3. انقر "تحويل إلى SVG"
4. ستجد الملف في `exports/` مع معاينة فورية

### اختبار المرحلة الثالثة (Logo Designer) ⭐ جديد
1. افتح التبويب "تصميم الشعارات"
2. أدخل نص الشعار (مثلاً: "My Brand")
3. اختر:**
   - الخط من القائمة المنسدلة
   - حجم الخط باستخدام المشغل
   - لون النص بالنقر على الزر الملون
   - لون الخلفية
4. فعّل التأثيرات إذا أردت (ظلال، ضبابي، تدرج)
5. انقر "✨ إنشاء الشعار"
6. انقر "💾 حفظ الشعار"

## الخطوة 4: تغيير اللغة

- انقر على 🇸🇦 **العربية** أو 🇬🇧 **English** في الرأس
- ستتغير اللغة فوراً بدون إغلاق التطبيق

## الخطوة 5: اختبار الكود (اختياري)

```bash
python test_logo_engine.py
```

ستظهر رسائل النجاح والشعارات في مجلد `exports/`

## الهيكل الأساسي للمشروع:

```
Iconora Studio/
├── main.py                  # التطبيق الرئيسي
├── core/
│   ├── icon_converter.py    # محرك تحويل الأيقونات
│   ├── svg_converter.py     # محرك تحويل SVG
│   └── logo_engine.py       # محرك تصميم الشعارات (جديد)
├── ui/
│   ├── main_window.py       # الكل الرئيسية
│   ├── icon_tab.py          # واجهة الأيقونات
│   ├── svg_tab.py           # واجهة SVG
│   └── logo_tab.py          # واجهة الشعارات (جديد)
├── config.py                # إعدادات عامة
├── i18n.py                  # نظام الترجمة (200+ ترجمة)
├── language_config.py       # حفظ اللغة
├── exports/                 # مجلد الملفات المُنتجة
├── requirements.txt         # المتطلبات
├── PHASE_3_SUMMARY.md       # ملخص الجديد
├── PHASE_3_COMPLETE.md      # التقرير الكامل
└── test_logo_engine.py      # اختبارات محرك الشعارات
```

## 💡 نصائح مفيدة:

### للحصول على أفضل النتائج مع Logo Designer:
1. **اختر خطاً واضحاً:** Arial أو Segoe UI أفضل للبدء
2. **حجم الخط:** 80-150 بكسل عادة يعطي أفضل النتائج
3. **الألوان:** استخدم تباين قوي بين النص والخلفية
4. **التدرجات:** رائعة للخلفيات الحديثة والاحترافية

### لتسريع العملية:
- استخدم نفس الخط واللون للشعارات المختلفة
- جرب التدرجات المختلفة
- جاور قبل الحفظ

### اختبار متقدم:
```python
from core.logo_engine import LogoEngine

engine = LogoEngine()

# شعار بسيط
engine.generate_logo(
    text="Test",
    font_size=100,
    text_color="#FFFFFF",
    bg_color="#0066FF"
)

# شعار بتدرج وتأثيرات
engine.generate_logo(
    text="Premium",
    font_size=120,
    use_gradient=True,
    gradient_color2="#FF0000",
    effects={"shadow": True}
)
```

---

**استمتع بـ Iconora Studio! 🎨✨**
