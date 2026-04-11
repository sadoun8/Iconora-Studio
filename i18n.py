"""
Localization Module - نظام الترجمة والتعريب
Support for Arabic and English
يدعم العربية والإنجليزية
"""

# ============================================================
# 🌍 LOCALIZATION DICTIONARY - قاموس الترجمة
# ============================================================

TRANSLATIONS = {
    # ==================== MAIN WINDOW ====================
    "app_title": {
        "ar": "🎨 Iconora Studio",
        "en": "🎨 Iconora Studio"
    },
    "app_subtitle": {
        "ar": "أداة احترافية لتحويل الصور والتصميم",
        "en": "Professional Image Conversion & Design Tool"
    },

    # ==================== TABS ====================
    "tab_icon_converter": {
        "ar": "تحويل الأيقونات",
        "en": "Icon Converter"
    },
    "tab_svg_converter": {
        "ar": "تحويل SVG",
        "en": "SVG Converter"
    },
    "tab_logo_designer": {
        "ar": "تصميم الشعارات",
        "en": "Logo Designer"
    },
    "tab_signature_generator": {
        "ar": "مولد التوقيعات",
        "en": "Signature Generator"
    },
    "tab_palette_generator": {
        "ar": "مولد الألوان",
        "en": "Palette Generator"
    },
    "tab_projects": {
        "ar": "إدارة المشاريع",
        "en": "Project Manager"
    },
    "tab_settings": {
        "ar": "إعدادات البرنامج",
        "en": "Settings"
    },
    "settings_appearance_mode": {
        "ar": "وضع المظهر",
        "en": "Appearance Mode"
    },
    "settings_app_language": {
        "ar": "لغة البرنامج",
        "en": "Application Language"
    },
    "settings_export_quality": {
        "ar": "جودة التصدير العامة",
        "en": "Global Export Quality"
    },
    "settings_auto_open": {
        "ar": "فتح المجلد تلقائياً بعد التصدير",
        "en": "Auto-open folder after export"
    },
    "settings_resources": {
        "ar": "الموارد والخطوط",
        "en": "Resources"
    },
    "settings_get_fonts": {
        "ar": "الحصول على خطوط عربية احترافية",
        "en": "Get Professional Arabic Fonts"
    },
    "settings_about": {
        "ar": "حول Iconora Studio",
        "en": "About Iconora Studio"
    },
    "app_description_brief": {
        "ar": "مجموعة أدوات احترافية للمبدعين.",
        "en": "A professional suite for creators."
    },
    "settings_storage_paths": {
        "ar": "📂 التخزين والمسارات",
        "en": "📂 Storage & Paths"
    },
    "settings_open_data_dir": {
        "ar": "فتح مجلد البيانات الرئيسي",
        "en": "Open Main Data Folder"
    },
    "settings_ai_section": {
        "ar": "الذكاء الاصطناعي (Ollama/Qwen)",
        "en": "AI Assistant (Ollama/Qwen)"
    },
    "settings_ai_enable": {
        "ar": "تفعيل ميزات الذكاء الاصطناعي",
        "en": "Enable AI features"
    },
    "settings_ai_endpoint": {
        "ar": "رابط خدمة الذكاء الاصطناعي",
        "en": "AI Endpoint"
    },
    "settings_ai_model": {
        "ar": "النموذج",
        "en": "AI Model"
    },
    "settings_ai_timeout": {
        "ar": "مهلة الاتصال (ثانية)",
        "en": "Timeout (sec)"
    },
    "settings_ai_test": {
        "ar": "اختبار اتصال الذكاء الاصطناعي",
        "en": "Test AI Connection"
    },
    "msg_ai_backend_ok": {
        "ar": "خدمة الذكاء الاصطناعي متاحة وتعمل ✅",
        "en": "AI backend is reachable and ready ✅"
    },
    "msg_ai_backend_fail": {
        "ar": "تعذر الوصول إلى خدمة الذكاء الاصطناعي.\nتحقق من Ollama أو رابط الخدمة أو اسم النموذج.",
        "en": "AI backend is not reachable.\nCheck Ollama service, endpoint, or model name."
    },

    # ==================== SIGNATURE TAB ====================
    "sig_studio_title": {"ar": "✍️ ستوديو التواقيع", "en": "✍️ Signature Studio"},
    "sig_name": {"ar": "الاسم", "en": "Name"},
    "sig_name_ph": {"ar": "الاسم الكامل...", "en": "Full name..."},
    "sig_title": {"ar": "اللقب (اختياري)", "en": "Title (optional)"},
    "sig_title_ph": {"ar": "مثال: المدير، المهندس...", "en": "e.g. CEO, Designer..."},
    "sig_font": {"ar": "✒️ خط التوقيع", "en": "✒️ Signature Font"},
    "sig_title_font": {"ar": "✒️ خط اللقب", "en": "✒️ Title Font"},
    "sig_size": {"ar": "الحجم", "en": "Size"},
    "sig_ornament": {"ar": "🌿 الزخرفة/الفواصل", "en": "🌿 Ornament / Flourish"},
    "sig_main_color": {"ar": "🖌 لون الحبر الأساسي", "en": "🖌 Main Ink Color"},
    "sig_title_color": {"ar": "🖌 لون اللقب", "en": "🖌 Title Color"},
    "sig_pick_color": {"ar": "● اختر اللون", "en": "● Pick Color"},
    "sig_presets": {"ar": "ألون جاهزة:", "en": "Presets:"},
    "sig_opacity": {"ar": "💧 شفافية الحبر", "en": "💧 Opacity"},
    "sig_options": {"ar": "⚙️ خيارات", "en": "⚙️ Options"},
    "sig_transparent": {"ar": "خلفية شفافة (PNG)", "en": "Transparent Background (PNG)"},
    "sig_ink": {"ar": "تأثير الحبر الطبيعي وضغط القلم", "en": "Realistic Ink & Pressure Effect"},
    "sig_artistic_undercurve": {"ar": "منحنى سفلي فني", "en": "Artistic Undercurve"},
    "sig_artistic_swirl": {"ar": "دوامة فنية", "en": "Artistic Swirl"},
    "sig_artistic_double_strike": {"ar": "شطبة مزدوجة", "en": "Artistic Double Strike"},
    "sig_artistic_slash": {"ar": "خط مائل فني", "en": "Artistic Slash"},
    "sig_artistic_curve_up": {"ar": "منحنى علوي", "en": "Artistic Curve Up"},
    "sig_artistic_loop_under": {"ar": "حلقة سفلية", "en": "Artistic Loop Under"},
    "sig_artistic_bracket_left": {"ar": "قوس يسار", "en": "Artistic Bracket Left"},
    "sig_artistic_bracket_right": {"ar": "قوس يمين", "en": "Artistic Bracket Right"},
    "sig_save": {"ar": "✨ حفظ التوقيع (PNG)", "en": "✨ Save Signature (PNG)"},
    "sig_preview": {"ar": "المعاينة المباشرة", "en": "Live Preview"},
    "sig_style": {"ar": "📐 ستايل التوقيع", "en": "📐 Signature Style"},
    "sig_typography_settings": {"ar": "إعدادات الخطوط", "en": "Typography Settings"},
    "sig_line_spacing": {"ar": "تباعد الأسطر", "en": "Line Spacing"},
    "sig_artistic_adjust": {"ar": "تعديلات فنية", "en": "Artistic Adjustments"},
    "sig_slant": {"ar": "الميلان (مائل)", "en": "Slant (Italic)"},
    "sig_ink_thickness": {"ar": "سماكة الحبر", "en": "Ink Thickness"},
    "sig_rotation": {"ar": "التدوير", "en": "Rotation"},
    "sig_ornament_color": {"ar": "الزخرفة واللون", "en": "Ornament & Color"},
    "sig_pick_main_color": {"ar": "اختر اللون الأساسي", "en": "Pick Main Color"},
    "sig_pick_title_color": {"ar": "اختر لون اللقب", "en": "Pick Title Color"},
    "sig_overall_opacity": {"ar": "الشفافية العامة", "en": "Overall Opacity"},
    "sig_save_signature": {"ar": "✨ حفظ التوقيع", "en": "✨ Save Signature"},
    "sig_open_gallery": {"ar": "مكتبة التواقيع المحفوظة", "en": "Open Signature Library"},
    "sig_add_to_library": {"ar": "إضافة للمكتبة الشخصية", "en": "Add to Private Library"},
    "sig_added_to_library": {"ar": "تمت الإضافة للمكتبة بنجاح", "en": "Added to library successfully"},
    "sig_gallery_title": {"ar": "📚 مكتبة التواقيع الخاصة بك", "en": "📚 Your Signature Gallery"},
    "sig_pick_sig_color": {"ar": "اختر لون التوقيع", "en": "Pick Signature Color"},
    "sig_enter_name": {"ar": "يرجى إدخال الاسم.", "en": "Enter a name."},
    "opt_none": {"ar": "بدون", "en": "None"},
    "opt_normal": {"ar": "عادي", "en": "Normal"},
    "opt_upward": {"ar": "صاعد", "en": "Upward"},
    "opt_slanted": {"ar": "مائل", "en": "Slanted"},

    # ==================== LOGO TAB ====================
    "logo_designer_title": {"ar": "💎 ستوديو تصميم الشعارات", "en": "💎 Logo Design Studio"},
    "lbl_logo_text": {"ar": "اسم الشركة / النص", "en": "Company Name / Text"},
    "placeholder_company_name": {"ar": "أدخل اسم العلامة التجارية...", "en": "Enter brand name..."},
    "logo_general_settings": {"ar": "⚙️ الإعدادات العامة", "en": "⚙️ General Settings"},
    "logo_overlay": {"ar": "دمج النص مع الأيقونة في الخلفية", "en": "Overlay text on icon background"},
    "logo_typography_pos": {"ar": "✒️ الخط والموقع", "en": "✒️ Typography & Position"},
    "logo_font_size": {"ar": "حجم الخط", "en": "Font Size"},
    "logo_offset_x": {"ar": "إزاحة أفقية (نص)", "en": "Text Offset X"},
    "logo_offset_y": {"ar": "إزاحة رأسية (نص)", "en": "Text Offset Y"},
    "logo_effects": {"ar": "✨ التأثيرات البصرية", "en": "✨ Visual Effects"},
    "logo_shadow_blur": {"ar": "تشتت الظل", "en": "Shadow Blur"},
    "logo_shadow_offset": {"ar": "إزاحة الظل", "en": "Shadow Offset"},
    "logo_shadow_opacity": {"ar": "شفافية الظل", "en": "Shadow Opacity"},
    "logo_shadow_color": {"ar": "لون الظل", "en": "Shadow Color"},
    "logo_glow_color": {"ar": "لون التوهج", "en": "Glow Color"},
    "logo_glow_radius": {"ar": "نطاق التوهج", "en": "Glow Radius"},
    "logo_primary_color": {"ar": "اللون الأساسي", "en": "Primary Color"},
    "logo_secondary_color": {"ar": "اللون الثانوي", "en": "Secondary Color"},
    "logo_icon_custom": {"ar": "🎨 تخصيص الأيقونة", "en": "🎨 Icon Customization"},
    "logo_load_icon": {"ar": "تحميل أيقونة مخصصة", "en": "Load Custom Icon"},
    "logo_no_icon": {"ar": "لم يتم اختيار أيقونة", "en": "No icon selected"},
    "logo_icon_scale": {"ar": "حجم الأيقونة", "en": "Icon Scale"},
    "logo_icon_rotation": {"ar": "تدوير الأيقونة", "en": "Icon Rotation"},
    "logo_icon_opacity": {"ar": "شفافية الأيقونة", "en": "Icon Opacity"},
    "logo_icon_saturation": {"ar": "تشبع ألوان الأيقونة", "en": "Icon Saturation"},
    "logo_icon_offset_x": {"ar": "إزاحة أفقية (أيقونة)", "en": "Icon Offset X"},
    "logo_icon_offset_y": {"ar": "إزاحة رأسية (أيقونة)", "en": "Icon Offset Y"},
    "logo_generate_save": {"ar": "✨ توليد وحفظ الشعار", "en": "✨ Generate & Save Logo"},
    "logo_ai_generate": {"ar": "توليد ذكي للشعار", "en": "AI Generate Logo"},
    "logo_target_text": {"ar": "التحكم بالنص", "en": "Target: Text"},
    "logo_target_icon": {"ar": "التحكم بالأيقونة", "en": "Target: Icon"},
    "btn_apply_watermark": {"ar": "تطبيق كعلامة مائية", "en": "Apply as Watermark"},
    "msg_select_base_image": {"ar": "اختر الصورة المراد وضع العلامة عليها", "en": "Select image to watermark"},
    "msg_watermark_success": {"ar": "تم تطبيق العلامة المائية وحفظ الصورة بنجاح", "en": "Watermark applied and image saved successfully"},
    "icon_tab_title": {
        "ar": "تحويل الصور إلى أيقونات",
        "en": "Convert Images to Icons"
    },
    "btn_select_image": {
        "ar": "📁 اختر صورة",
        "en": "📁 Select Image"
    },
    "no_image_selected": {
        "ar": "لم يتم اختيار صورة",
        "en": "No image selected"
    },
    "select_sizes": {
        "ar": "اختر الأحجام المطلوبة:",
        "en": "Select desired sizes:"
    },
    "preview": {
        "ar": "معاينة",
        "en": "Preview"
    },
    "btn_save_ico": {
        "ar": "💾 حفظ ICO",
        "en": "💾 Save ICO"
    },
    "btn_save_png": {
        "ar": "📸 حفظ PNG",
        "en": "📸 Export PNG"
    },
    "btn_remove_bg": {
        "ar": "✨ إزالة الخلفية (ذكاء اصطناعي)",
        "en": "✨ Remove Background (AI)"
    },
    "msg_rembg_success": {
        "ar": "تمت إزالة الخلفية بنجاح!",
        "en": "Background removed successfully!"
    },
    "msg_rembg_error": {
        "ar": "فشلت عملية إزالة الخلفية بالذكاء الاصطناعي",
        "en": "AI background removal failed"
    },
    "btn_reset_page": {
        "ar": "🔄 إعادة ضبط الصفحة",
        "en": "🔄 Reset Page"
    },

    # Mask & Shape
    "lbl_mask_shape": {"ar": "القناع والشكل", "en": "Mask & Shape"},
    "lbl_corner_radius": {"ar": "نصف قطر الزاوية (%)", "en": "Corner Radius (%)"},
    "lbl_internal_padding": {"ar": "الهامش الداخلي (%)", "en": "Internal Padding (%)"},
    "lbl_bg_border": {"ar": "الخلفية والإطار", "en": "Background & Border"},
    "lbl_bg_color": {"ar": "لون الخلفية", "en": "Background Color"},
    "lbl_border_width": {"ar": "عرض الإطار (%)", "en": "Border Width (%)"},
    "lbl_border_color": {"ar": "لون الإطار", "en": "Border Color"},

    # Text Overlay
    "lbl_text_overlay": {"ar": "🔤 الكتابة على الأيقونة", "en": "🔤 Text Overlay"},
    "opt_enable_text": {"ar": "تفعيل الكتابة", "en": "Enable Text"},
    "lbl_text": {"ar": "النص", "en": "Text"},
    "lbl_position": {"ar": "الموقع", "en": "Position"},
    "pos_top": {"ar": "أعلى", "en": "Top"},
    "pos_center": {"ar": "وسط", "en": "Center"},
    "pos_bottom": {"ar": "أسفل", "en": "Bottom"},
    "opt_outline": {"ar": "إضافة إطار أسود (Outline)", "en": "Add black outline"},

    # ==================== SIZE LABELS ====================
    "size_16": {
        "ar": "16x16 (رمز صغير)",
        "en": "16x16 (Favicon)"
    },
    "size_24": {
        "ar": "24x24 (صغيرة)",
        "en": "24x24 (Small)"
    },
    "size_32": {
        "ar": "32x32 (افتراضي)",
        "en": "32x32 (Default)"
    },
    "size_48": {
        "ar": "48x48 (متوسطة)",
        "en": "48x48 (Medium)"
    },
    "size_64": {
        "ar": "64x64 (كبيرة)",
        "en": "64x64 (Large)"
    },
    "size_128": {
        "ar": "128x128 (كبيرة جداً)",
        "en": "128x128 (Extra Large)"
    },
    "size_256": {
        "ar": "256x256 (فائقة)",
        "en": "256x256 (Ultra Large)"
    },

    # ==================== FILE DIALOGS ====================
    "dialog_select_image": {
        "ar": "اختر صورة",
        "en": "Select Image"
    },
    "dialog_image_type": {
        "ar": "صور",
        "en": "Images"
    },
    "dialog_all_files": {
        "ar": "جميع الملفات",
        "en": "All Files"
    },
    "dialog_save_ico": {
        "ar": "احفظ ملف الأيقونة",
        "en": "Save Icon File"
    },
    "dialog_ico_type": {
        "ar": "ملفات الأيقونة",
        "en": "Icon Files"
    },
    "dialog_select_folder": {
        "ar": "اختر مجلد الحفظ",
        "en": "Select Save Folder"
    },

    # ==================== MESSAGES - INFO ====================
    "msg_success": {
        "ar": "نجاح",
        "en": "Success"
    },
    "msg_saved_ico": {
        "ar": "تم الحفظ بنجاح: ",
        "en": "Saved successfully: "
    },
    "msg_saved_svg": {
        "ar": "تم الحفظ بنجاح: ",
        "en": "Saved successfully: "
    },
    "msg_saved_logo": {
        "ar": "تم إنشاء الشعار بنجاح: ",
        "en": "Logo created successfully: "
    },
    "msg_results": {
        "ar": "النتائج",
        "en": "Results"
    },
    "msg_image_info": {
        "ar": "الحجم: {width}x{height} | الصيغة: {format}",
        "en": "Size: {width}x{height} | Format: {format}"
    },
    "msg_saved_images": {
        "ar": "تم حفظ {count} صورة بنجاح\n\nالنتائج:\n",
        "en": "Successfully saved {count} images\n\nResults:\n"
    },
    "msg_saved_file": {
        "ar": "تم حفظ: {filename}",
        "en": "Saved: {filename}"
    },
    "msg_no_preview": {
        "ar": "لا توجد معاينة حالياً",
        "en": "No preview available"
    },
    "msg_file_saved_at": {
        "ar": "الملف محفوظ في:",
        "en": "File saved at:"
    },

    # ==================== MESSAGES - WARNING ====================
    "msg_warning": {
        "ar": "تحذير",
        "en": "Warning"
    },
    "msg_confirm": {
        "ar": "تأكيد",
        "en": "Confirm"
    },
    "msg_select_image_first": {
        "ar": "الرجاء اختيار صورة أولاً",
        "en": "Please select an image first"
    },
    "msg_select_size": {
        "ar": "اختر حجماً واحداً على الأقل",
        "en": "Select at least one size"
    },
    "msg_enter_logo_text": {
        "ar": "الرجاء إدخال اسم الشعار/الشركة",
        "en": "Please enter logo/company name"
    },
    "msg_generate_logo_first": {
        "ar": "الرجاء إنشاء الشعار أولاً",
        "en": "Please generate a logo first"
    },

    # ==================== MESSAGES - ERROR ====================
    "msg_error": {
        "ar": "خطأ",
        "en": "Error"
    },
    "msg_load_error": {
        "ar": "خطأ في تحميل الصورة:\n",
        "en": "Error loading image:\n"
    },
    "msg_save_error": {
        "ar": "خطأ في الحفظ: ",
        "en": "Error saving: "
    },
    "msg_file_error": {
        "ar": "خطأ في الملف: ",
        "en": "File error: "
    },
    "msg_error_in": {
        "ar": " خطأ في: {filename} - {error}",
        "en": " Error in: {filename} - {error}"
    },
    "msg_error_occurred": {
        "ar": "حدث خطأ:\n",
        "en": "An error occurred:\n"
    },
    "msg_python_error": {
        "ar": "خطأ في Python",
        "en": "Python Error"
    },
    "msg_missing_dependencies": {
        "ar": "المكتبات المطلوبة غير مثبتة",
        "en": "Required libraries not installed"
    },

    # ==================== STATUS MESSAGES ====================
    "status_loading": {
        "ar": "جاري التحميل...",
        "en": "Loading..."
    },
    "status_converting": {
        "ar": "جاري التحويل...",
        "en": "Converting..."
    },
    "status_saving": {
        "ar": "جاري الحفظ...",
        "en": "Saving..."
    },
    "status_complete": {
        "ar": "مكتمل ✅",
        "en": "Complete ✅"
    },

    # ==================== MENU & SETTINGS ====================
    "menu_file": {
        "ar": "ملف",
        "en": "File"
    },
    "menu_edit": {
        "ar": "تحرير",
        "en": "Edit"
    },
    "menu_view": {
        "ar": "عرض",
        "en": "View"
    },
    "menu_help": {
        "ar": "مساعدة",
        "en": "Help"
    },
    "menu_language": {
        "ar": "اللغة",
        "en": "Language"
    },
    "language_arabic": {
        "ar": "العربية",
        "en": "Arabic"
    },
    "language_english": {
        "ar": "الإنجليزية",
        "en": "English"
    },
    "menu_settings": {
        "ar": "الإعدادات",
        "en": "Settings"
    },
    "menu_about": {
        "ar": "عن البرنامج",
        "en": "About"
    },
    "menu_exit": {
        "ar": "خروج",
        "en": "Exit"
    },

    # ==================== HELP & DOCUMENTATION ====================
    "help_title": {
        "ar": "تعليمات الاستخدام",
        "en": "Help & Instructions"
    },
    "help_step1": {
        "ar": "1️⃣ اختر صورة من جهازك",
        "en": "1️⃣ Select an image from your computer"
    },
    "help_step2": {
        "ar": "2️⃣ اختر الأحجام المطلوبة",
        "en": "2️⃣ Select the desired sizes"
    },
    "help_step3": {
        "ar": "3️⃣ انقر على حفظ ICO أو حفظ PNG",
        "en": "3️⃣ Click Save ICO or Export PNG"
    },
    "help_step4": {
        "ar": "4️⃣ اختر مكان الحفظ وانتظر",
        "en": "4️⃣ Choose save location and wait"
    },
    "about_version": {
        "ar": "الإصدار: 1.2.0",
        "en": "Version: 1.2.0"
    },
    "about_description": {
        "ar": "تطبيق احترافي لتحويل الصور والتصميم",
        "en": "Professional image conversion and design tool"
    },

    # ==================== TOOLTIPS ====================
    "tooltip_select_image": {
        "ar": "اختر صورة من جهازك (PNG, JPG, BMP, إلخ)",
        "en": "Select an image from your computer (PNG, JPG, BMP, etc)"
    },
    "tooltip_sizes": {
        "ar": "حدد الأحجام التي تريد تصديرها",
        "en": "Select the sizes you want to export"
    },
    "tooltip_ico": {
        "ar": "حفظ جميع الأحجام في ملف ICO واحد",
        "en": "Save all sizes in a single ICO file"
    },
    "tooltip_png": {
        "ar": "حفظ كل حجم كصورة PNG منفصلة",
        "en": "Save each size as a separate PNG image"
    },

    # ==================== QUALITY SETTINGS ====================
    "quality_title": {
        "ar": "جودة التحويل",
        "en": "Conversion Quality"
    },
    "quality_high": {
        "ar": "عالية جداً",
        "en": "Very High"
    },
    # Image Adjustments
    "lbl_brightness": {"ar": "السطوع", "en": "Brightness"},
    "lbl_contrast": {"ar": "التباين", "en": "Contrast"},
    "lbl_saturation": {"ar": "تشبع الألوان", "en": "Saturation"},
    "lbl_flip_h": {"ar": "قلب أفقي", "en": "Flip Horizontal"},
    "lbl_flip_v": {"ar": "قلب رأسي", "en": "Flip Vertical"},
    "lbl_image_adjust": {"ar": "🖼️ تعديلات الصورة", "en": "🖼️ Image Adjustments"},
    "opt_circle": {"ar": "قص دائري", "en": "Circle Mask"},
    "opt_squircle": {"ar": "قص سكويركل (iOS)", "en": "Squircle Mask (iOS)"},
    "opt_rounded": {"ar": "حواف مستديرة", "en": "Rounded Corners"},
    "msg_select_icon_first": {"ar": "الرجاء اختيار أيقونة أولاً", "en": "Please select an icon first"},
    "dlg_select_icon": {"ar": "اختر أيقونة للشعار", "en": "Select Logo Icon"},
    "lbl_image_files": {"ar": "ملفات الصور", "en": "Image Files"},
    "lbl_all_files": {"ar": "جميع الملفات", "en": "All Files"},
    "lbl_logo_text": {"ar": "نص الشعار", "en": "Logo Text"},
    "placeholder_company_name": {"ar": "اسم الشركة...", "en": "Company name..."},
    "quality_normal": {
        "ar": "عادية",
        "en": "Normal"
    },
    "quality_fast": {
        "ar": "سريعة",
        "en": "Fast"
    },

    # ==================== SVG TAB ====================
    "btn_convert_svg": {
        "ar": "🔄 بدء تحويل SVG الآن",
        "en": "🔄 Start SVG Conversion Now"
    },
    "lbl_image_preview": {
        "ar": "معاينة الصورة",
        "en": "Image Preview"
    },
    "lbl_image_files": {
        "ar": "صور",
        "en": "Images"
    },
    "lbl_all_files": {
        "ar": "جميع الملفات",
        "en": "All Files"
    },
    "dlg_select_image": {
        "ar": "اختر صورة",
        "en": "Select Image"
    },
    "dlg_select_icon": {
        "ar": "اختر أيقونة/رمز",
        "en": "Select Icon/Symbol"
    },
    "msg_select_icon_first": {
        "ar": "الرجاء اختيار أيقونة أولاً",
        "en": "Please select an icon first"
    },
    "lbl_error": {
        "ar": "خطأ",
        "en": "Error"
    },
    "lbl_filename": {
        "ar": "اسم الملف",
        "en": "Filename"
    },
    "lbl_dimensions": {
        "ar": "الأبعاد",
        "en": "Dimensions"
    },
    "lbl_size": {
        "ar": "الحجم",
        "en": "Size"
    },
    "lbl_ico_files": {
        "ar": "ملفات الأيقونة",
        "en": "Icon Files"
    },
    "dlg_save_ico": {
        "ar": "احفظ ملف الأيقونة",
        "en": "Save Icon File"
    },
    "msg_exported_files": {
        "ar": "تم تصدير الملفات",
        "en": "Files exported"
    },

    # ==================== LOGO TAB ====================
    "logo_designer_title": {"ar": "🎯 مصمم الشعارات", "en": "🎯 Logo Designer"},
    "logo_general_settings": {"ar": "الإعدادات العامة", "en": "General Settings"},
    "logo_style": {"ar": "النمط", "en": "Style"},
    "logo_layout": {"ar": "التخطيط", "en": "Layout"},
    "logo_template": {"ar": "القالب", "en": "Template"},
    "logo_canvas_size": {"ar": "حجم مساحة العمل", "en": "Canvas Size"},
    "logo_overlay": {"ar": "نص فوق الأيقونة (تداخل)", "en": "Text Over Icon (Overlay)"},
    "logo_typography_pos": {"ar": "الخط والموقع", "en": "Typography & Position"},
    "logo_font_size": {"ar": "حجم الخط", "en": "Font Size"},
    "logo_offset_x": {"ar": "إزاحة النص X", "en": "Text Offset X"},
    "logo_offset_y": {"ar": "إزاحة النص Y", "en": "Text Offset Y"},
    "logo_effects": {"ar": "✨ التأثيرات (ظل وتوهج)", "en": "✨ Effects (Shadow & Glow)"},
    "logo_shadow_blur": {"ar": "نعومة الظل", "en": "Shadow Blur"},
    "logo_shadow_offset": {"ar": "إزاحة الظل", "en": "Shadow Offset"},
    "logo_shadow_opacity": {"ar": "شفافية الظل", "en": "Shadow Opacity"},
    "logo_shadow_color": {"ar": "لون الظل", "en": "Shadow Color"},
    "logo_glow_radius": {"ar": "نصف قطر التوهج", "en": "Glow Radius"},
    "logo_glow_color": {"ar": "لون التوهج", "en": "Glow Color"},
    "logo_primary_color": {"ar": "اللون الأساسي", "en": "Primary Color"},
    "logo_secondary_color": {"ar": "اللون الثانوي/3D", "en": "Secondary/3D Color"},
    "logo_icon_custom": {"ar": "تخصيص الأيقونة", "en": "Icon Customization"},
    "logo_load_icon": {"ar": "📦 تحميل أيقونة/رمز", "en": "📦 Load Icon/Symbol"},
    "logo_icon_scale": {"ar": "حجم الأيقونة (%)", "en": "Icon Scale (%)"},
    "logo_icon_rotation": {"ar": "تدوير الأيقونة", "en": "Icon Rotation"},
    "logo_icon_opacity": {"ar": "شفافية الأيقونة", "en": "Icon Opacity"},
    "logo_icon_saturation": {"ar": "تشبع الأيقونة", "en": "Icon Saturation"},
    "logo_icon_offset_x": {"ar": "إزاحة الأيقونة X", "en": "Icon Offset X"},
    "logo_icon_offset_y": {"ar": "إزاحة الأيقونة Y", "en": "Icon Offset Y"},
    "logo_move_target": {"ar": "عنصر التحريك", "en": "Drag Target"},
    "logo_target_text": {"ar": "النص", "en": "Text"},
    "logo_target_icon": {"ar": "الأيقونة", "en": "Icon"},
    "logo_generate_save": {"ar": "✨ إنشاء وحفظ الشعار", "en": "✨ Generate & Save Logo"},
    "logo_no_icon": {"ar": "لم يتم اختيار أيقونة", "en": "No icon selected"},
    "lbl_logo_settings": {"ar": "إعدادات الشعار", "en": "Logo Settings"},
    "lbl_logo_text": {"ar": "نص الشعار", "en": "Logo Text"},
    "placeholder_company_name": {"ar": "أدخل اسم الشركة/الشعار", "en": "Enter company/logo name"},
    "lbl_font": {"ar": "الخط", "en": "Font"},
    "lbl_font_size": {"ar": "حجم الخط", "en": "Font Size"},
    "lbl_text_color": {"ar": "لون النص", "en": "Text Color"},
    "lbl_bg_color": {"ar": "لون الخلفية", "en": "Background Color"},
    "lbl_effects": {"ar": "التأثيرات", "en": "Effects"},
    "opt_use_gradient": {"ar": "استخدام تدرج لوني", "en": "Use color gradient"},
    "opt_add_shadow": {"ar": "إضافة ظل", "en": "Add shadow"},
    "opt_blur_effect": {"ar": "تأثير ضبابي", "en": "Blur effect"},
    "lbl_preview": {"ar": "المعاينة", "en": "Preview"},
    "btn_generate_logo": {"ar": "✨ إنشاء وحفظ الشعار", "en": "✨ Generate & Save Logo"},
    "btn_apply_conversion": {"ar": "🚀 تنفيذ التحويل النهائي", "en": "🚀 Execute Final Conversion"},
    "btn_save_logo": {"ar": "حفظ الشعار", "en": "Save Logo"},
    "lbl_png_files": {"ar": "صور PNG", "en": "PNG Images"},
    "dlg_select_icon": {"ar": "اختر أيقونة/رمز", "en": "Select Icon/Symbol"},
    "lbl_image_files": {"ar": "ملفات الصور", "en": "Image Files"},
    "lbl_all_files": {"ar": "جميع الملفات", "en": "All Files"},

    # ==================== PALETTE TAB ====================
    "tab_palette_generator": {
        "ar": "🎨 مولد الألوان",
        "en": "🎨 Color Palettes"
    },
    "palette_tab_title": {
        "ar": "مولد لوحات الألوان",
        "en": "Palette Generator"
    },
    "palette_desc": {
        "ar": "قم بإنشاء لوحات ألوان احترافية لتصاميمك",
        "en": "Generate professional color palettes for your designs"
    },
    "palette_style": {
        "ar": "نمط اللوحة:",
        "en": "Palette Style:"
    },
    "palette_select": {
        "ar": "اختر اللوحة:",
        "en": "Select Palette:"
    },
    "palette_preview": {
        "ar": "معاينة اللوحة:",
        "en": "Palette Preview:"
    },
    "palette_info_placeholder": {
        "ar": "اختر لوحة ألوان لعرض تفاصيل الألوان",
        "en": "Select a palette to see color information"
    },
    "palette_generate_btn": {
        "ar": "إنشاء وحفظ لوحة الألوان",
        "en": "Generate & Save Palette"
    },
    "palette_modern": {
        "ar": "عصري",
        "en": "Modern"
    },
    "palette_luxury": {
        "ar": "فخم",
        "en": "Luxury"
    },
    "palette_save_success": {
        "ar": "تم حفظ لوحة الألوان في:\n{path}",
        "en": "Palette saved to:\n{path}"
    },
    "palette_select_warn": {
        "ar": "يرجى اختيار لوحة ألوان أولاً",
        "en": "Please select a palette first"
    },
    "palette_output_warn": {
        "ar": "يرجى تحديد مجلد الإخراج",
        "en": "Please specify output folder"
    },
    "palette_generating": {
        "ar": "جاري الإنشاء...",
        "en": "Generating..."
    },
    "palette_ready": {
        "ar": "جاهز",
        "en": "Ready"
    },
    "palette_error": {
        "ar": "فشل الإنشاء: {error}",
        "en": "Generation failed: {error}"
    },
    "palette_load_error": {
        "ar": "فشل تحميل اللوحة: {error}",
        "en": "Failed to load palette: {error}"
    },
    "lbl_output_folder": {
        "ar": "مجلد المخرجات:",
        "en": "Output Folder:"
    },
    "btn_browse": {
        "ar": "استعراض",
        "en": "Browse"
    },

    # ==================== PROJECTS TAB ====================
    "projects_tab_title": {
        "ar": "إدارة المشاريع",
        "en": "Project Manager"
    },
    "projects_desc": {
        "ar": "إدارة وحفظ مشاريعك للعودة إليها لاحقاً",
        "en": "Manage and save your projects to return to them later"
    },
    "btn_save_project": {
        "ar": "💾 حفظ المشروع",
        "en": "💾 Save Project"
    },
    "btn_load_project": {
        "ar": "📂 تحميل مشروع",
        "en": "📂 Load Project"
    },
    "project_name": {
        "ar": "اسم المشروع",
        "en": "Project Name"
    },
    "project_type": {
        "ar": "نوع المشروع",
        "en": "Project Type"
    },
    "project_date": {
        "ar": "التاريخ",
        "en": "Date"
    },
    "msg_project_saved": {
        "ar": "تم حفظ المشروع بنجاح",
        "en": "Project saved successfully"
    },
    "msg_project_loaded": {
        "ar": "تم تحميل المشروع بنجاح",
        "en": "Project loaded successfully"
    },
}


class Localization:
    """نظام إدارة الترجمة والتعريب"""

    def __init__(self, language: str = "ar"):
        """
        Initialize localization

        Args:
            language: "ar" for Arabic, "en" for English
        """
        self.current_language = language if language in ["ar", "en"] else "ar"

    def get(self, key: str, **kwargs) -> str:
        """
        الحصول على نص مترجم
        Get translated text

        Args:
            key: مفتاح الترجمة / Translation key
            **kwargs: متغيرات للاستبدال / Variables for substitution

        Returns:
            النص المترجم / Translated text
        """
        if key not in TRANSLATIONS:
            return f"[{key}]"  # Return key if not found

        translation = TRANSLATIONS[key].get(self.current_language,
                                          TRANSLATIONS[key].get("en", f"[{key}]"))

        # استبدال المتغيرات / Replace variables
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                print(f"Missing translation variable: {e}")

        return translation

    def set_language(self, language: str):
        """
        تغيير اللغة
        Change language

        Args:
            language: "ar" for Arabic, "en" for English
        """
        if language in ["ar", "en"]:
            self.current_language = language

    def get_language(self) -> str:
        """الحصول على اللغة الحالية / Get current language"""
        return self.current_language

    def is_arabic(self) -> bool:
        """التحقق من كون اللغة عربية / Check if language is Arabic"""
        return self.current_language == "ar"

    def is_english(self) -> bool:
        """التحقق من كون اللغة إنجليزية / Check if language is English"""
        return self.current_language == "en"


# إنشاء كائن ترجمة عام / Create global localization object
i18n = Localization("ar")  # الافتراضي: العربية / Default: Arabic


def tr(key: str, **kwargs) -> str:
    """
    دالة مختصرة للترجمة
    Shortcut function for translation

    Example:
        text = tr("app_title")
        message = tr("msg_image_info", width=100, height=100)
    """
    return i18n.get(key, **kwargs)


def set_language(language: str):
    """تعيين اللغة / Set language"""
    i18n.set_language(language)


def get_language() -> str:
    """الحصول على اللغة الحالية / Get current language"""
    return i18n.get_language()


# للاستخدام مباشرة / For direct usage
__all__ = ["i18n", "tr", "set_language", "get_language", "Localization", "TRANSLATIONS"]
