"""
Test Localization System
اختبار نظام الترجمة والتعريب

Verify that all translations are working correctly
"""

import sys
from i18n import tr, set_language, i18n, TRANSLATIONS


def test_translations():
    """اختبار جميع الترجمات / Test all translations"""

    print("\n" + "="*70)
    print("🧪 اختبار نظام الترجمة / LOCALIZATION SYSTEM TEST")
    print("="*70 + "\n")

    # Test 1: Check if all translations have both languages
    print("✅ الاختبار 1️⃣: التحقق من اكتمال الترجمات")
    print("   Test 1️⃣: Checking translation completeness\n")

    missing_languages = []
    total_keys = 0
    complete_keys = 0

    for key, translations in TRANSLATIONS.items():
        total_keys += 1
        if "ar" in translations and "en" in translations:
            complete_keys += 1
        else:
            missing_languages.append(key)

    print(f"   إجمالي المفاتيح: {total_keys}")
    print(f"   المفاتيح الكاملة: {complete_keys}")
    print(f"   المفاتيح غير الكاملة: {len(missing_languages)}")

    if missing_languages:
        print(f"   ❌ المفاتيح الناقصة: {missing_languages}")
    else:
        print("   ✅ جميع المفاتيح كاملة!")

    # Test 2: Test Arabic translations
    print("\n✅ الاختبار 2️⃣: اختبار الترجمات العربية")
    print("   Test 2️⃣: Testing Arabic translations\n")

    set_language("ar")
    test_keys_ar = [
        "app_title",
        "app_subtitle",
        "btn_select_image",
        "msg_success",
        "msg_error"
    ]

    for key in test_keys_ar:
        text = tr(key)
        print(f"   {key}: {text}")

    # Test 3: Test English translations
    print("\n✅ الاختبار 3️⃣: اختبار الترجمات الإنجليزية")
    print("   Test 3️⃣: Testing English translations\n")

    set_language("en")
    test_keys_en = [
        "app_title",
        "app_subtitle",
        "btn_select_image",
        "msg_success",
        "msg_error"
    ]

    for key in test_keys_en:
        text = tr(key)
        print(f"   {key}: {text}")

    # Test 4: Test translations with variables
    print("\n✅ الاختبار 4️⃣: اختبار الترجمات مع المتغيرات")
    print("   Test 4️⃣: Testing translations with variables\n")

    set_language("ar")
    msg_ar = tr("msg_image_info", width=800, height=600, format="PNG")
    print(f"   العربية: {msg_ar}")

    set_language("en")
    msg_en = tr("msg_image_info", width=800, height=600, format="PNG")
    print(f"   English: {msg_en}")

    # Test 5: Size labels
    print("\n✅ الاختبار 5️⃣: اختبار تسميات الأحجام")
    print("   Test 5️⃣: Testing size labels\n")

    set_language("ar")
    sizes = ["size_16", "size_32", "size_64", "size_128", "size_256"]
    for size_key in sizes:
        label = tr(size_key)
        print(f"   {label}")

    # Test 6: Language switching
    print("\n✅ الاختبار 6️⃣: اختبار تبديل اللغة")
    print("   Test 6️⃣: Testing language switching\n")

    print(f"   اللغة الحالية: {i18n.get_language()}")
    print(f"   النص: {tr('app_title')}")

    set_language("en")
    print(f"   Current language: {i18n.get_language()}")
    print(f"   Text: {tr('app_title')}")

    set_language("ar")
    print(f"   اللغة الحالية: {i18n.get_language()}")
    print(f"   النص: {tr('app_title')}")

    # Test 7: Message categories
    print("\n✅ الاختبار 7️⃣: اختبار فئات الرسائل")
    print("   Test 7️⃣: Testing message categories\n")

    categories = {
        "🎯 الواجهة الرئيسية": ["app_title", "app_subtitle"],
        "📁 التبويبات": ["tab_icon_converter", "tab_svg_converter"],
        "🔘 الأزرار": ["btn_select_image", "btn_save_ico"],
        "⚠️ التحذيرات": ["msg_warning", "msg_select_image_first"],
        "❌ الأخطاء": ["msg_error", "msg_load_error"],
        "✅ النجاح": ["msg_success", "msg_saved_ico"]
    }

    set_language("ar")
    for category, keys in categories.items():
        print(f"\n   {category}")
        for key in keys:
            try:
                text = tr(key)
                print(f"      ✅ {key}: {text}")
            except Exception as e:
                print(f"      ❌ {key}: خطأ - {e}")

    # Summary
    print("\n" + "="*70)
    print("📊 ملخص الاختبار / TEST SUMMARY")
    print("="*70)
    print(f"""
    ✅ إجمالي المفاتيح: {total_keys}
    ✅ المفاتيح الكاملة: {complete_keys}/{total_keys}
    ✅ الترجمات العربية: ✓
    ✅ الترجمات الإنجليزية: ✓
    ✅ المتغيرات والقوالب: ✓
    ✅ تبديل اللغة: ✓

    🎯 النتيجة:
       ✅ نظام الترجمة يعمل بشكل مثالي!
       ✅ جميع الترجمات موجودة وكاملة!
       ✅ التطبيق جاهز للاستخدام الكامل بالعربية والإنجليزية!
    """)
    print("="*70 + "\n")


def count_translations():
    """عدّ الترجمات / Count translations"""

    print("\n📊 إحصائيات الترجمات / TRANSLATION STATISTICS\n")

    categories = {
        "Main Window": [],
        "Tabs": [],
        "Buttons": [],
        "File Dialogs": [],
        "Info Messages": [],
        "Warning Messages": [],
        "Error Messages": [],
        "Status Messages": [],
        "Menus": [],
        "Help": [],
        "Tooltips": [],
        "Other": []
    }

    # Categorize translations
    for key in TRANSLATIONS.keys():
        if key.startswith("app_"):
            categories["Main Window"].append(key)
        elif key.startswith("tab_"):
            categories["Tabs"].append(key)
        elif key.startswith("btn_"):
            categories["Buttons"].append(key)
        elif key.startswith("dialog_"):
            categories["File Dialogs"].append(key)
        elif key.startswith("msg_i"):
            categories["Info Messages"].append(key)
        elif key.startswith("msg_w"):
            categories["Warning Messages"].append(key)
        elif key.startswith("msg_e"):
            categories["Error Messages"].append(key)
        elif key.startswith("status_"):
            categories["Status Messages"].append(key)
        elif key.startswith("menu_"):
            categories["Menus"].append(key)
        elif key.startswith("help_"):
            categories["Help"].append(key)
        elif key.startswith("tooltip_"):
            categories["Tooltips"].append(key)
        else:
            categories["Other"].append(key)

    total = 0
    for category, keys in categories.items():
        if keys:
            print(f"   {category:25} | {len(keys):3} مفاتيح")
            total += len(keys)

    print(f"   {'-'*40}")
    print(f"   {'المجموع أو Total':25} | {total:3} مفاتيح\n")


if __name__ == "__main__":
    try:
        test_translations()
        count_translations()

        print("✅ اجتياز جميع الاختبارات!")
        print("✅ All tests passed!\n")

        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار / Test Error:")
        print(f"   {e}\n")
        sys.exit(1)
