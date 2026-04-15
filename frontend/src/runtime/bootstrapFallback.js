const ARABIC_FONTS = [
  { label: 'Cairo (عصري)', value: 'Cairo' },
  { label: 'Tajawal (رشيق)', value: 'Tajawal' },
  { label: 'Amiri (كلاسيكي)', value: 'Amiri' },
  { label: 'IBM Plex Arabic', value: 'IBM Plex Sans Arabic' },
  { label: 'Scheherazade', value: 'Scheherazade New' },
  { label: 'Noto Naskh', value: 'Noto Naskh Arabic' },
];

const LATIN_FONTS = [
  { label: 'Outfit (Modern)', value: 'Outfit' },
  { label: 'Arial', value: 'Arial' },
  { label: 'Georgia', value: 'Georgia' },
  { label: 'Courier New', value: 'Courier New' },
];

const ALL_FONTS = [...ARABIC_FONTS, ...LATIN_FONTS];

const SIGNATURE_FONTS = [
  { label: 'Amiri (خط عربي كلاسيكي)', value: 'Amiri' },
  { label: 'Scheherazade (تقليدي)', value: 'Scheherazade New' },
  { label: 'Noto Naskh (نسخ)', value: 'Noto Naskh Arabic' },
  { label: 'Cairo (عصري)', value: 'Cairo' },
  { label: 'Georgia (لاتيني كلاسيكي)', value: 'Georgia' },
  { label: 'Courier New (Mono)', value: 'Courier New' },
];

const LOGO_SIZES = [
  { label: 'مربع 800×800', w: 800, h: 800 },
  { label: 'أفقي 1200×600', w: 1200, h: 600 },
  { label: 'عمودي 600×900', w: 600, h: 900 },
  { label: 'شعار 512×512', w: 512, h: 512 },
];

const ICON_SIZES = [
  { label: 'App Icon 512×512', w: 512, h: 512 },
  { label: 'Favicon 32×32', w: 32, h: 32 },
  { label: 'Icon 128×128', w: 128, h: 128 },
  { label: 'Icon 256×256', w: 256, h: 256 },
];

const SIGNATURE_SIZES = [
  { label: 'توقيع 800×300', w: 800, h: 300 },
  { label: 'توقيع 600×200', w: 600, h: 200 },
  { label: 'مربع 400×400', w: 400, h: 400 },
  { label: 'بانر 1200×400', w: 1200, h: 400 },
];

const LOGO_TEMPLATES = [
  {
    id: 'coffee',
    label: 'مقهى',
    emoji: '☕',
    bg: '#2d1b0e',
    objects: [
      { type: 'rect', fill: '#c8860a', rx: 70, ry: 70, width: 320, height: 320, left: 240, top: 240 },
      { type: 'text', text: 'مَقهى', fontSize: 80, fontFamily: 'Amiri', fill: '#fff', left: 270, top: 288, fontWeight: 'bold' },
      { type: 'text', text: 'C A F E', fontSize: 20, fontFamily: 'Outfit', fill: '#c8860a', left: 320, top: 420, charSpacing: 250 },
    ],
  },
  {
    id: 'tech',
    label: 'تقنية',
    emoji: '⚡',
    bg: '#0d0d1f',
    objects: [
      { type: 'rect', fill: 'transparent', stroke: '#6366f1', strokeWidth: 3, rx: 16, ry: 16, width: 340, height: 120, left: 230, top: 310 },
      { type: 'text', text: 'TECH', fontSize: 68, fontFamily: 'Outfit', fill: '#818cf8', left: 265, top: 316, fontWeight: '800' },
      { type: 'text', text: 'نصنع المستقبل', fontSize: 22, fontFamily: 'Cairo', fill: '#64748b', left: 280, top: 450 },
    ],
  },
  {
    id: 'studio',
    label: 'استوديو',
    emoji: '🎨',
    bg: '#0f0520',
    objects: [
      { type: 'rect', fill: '#7c3aed', rx: 50, ry: 50, width: 120, height: 120, left: 340, top: 240 },
      { type: 'text', text: 'STUDIO', fontSize: 56, fontFamily: 'Outfit', fill: '#ffffff', left: 248, top: 385, fontWeight: '800', charSpacing: 120 },
      { type: 'text', text: 'تصميم إبداعي', fontSize: 20, fontFamily: 'Cairo', fill: '#a78bfa', left: 295, top: 455 },
    ],
  },
];

const ICON_TEMPLATES = [
  {
    id: 'app-icon',
    label: 'تطبيق',
    emoji: '📱',
    bg: '#6366f1',
    objects: [
      { type: 'rect', fill: 'rgba(255,255,255,0.15)', rx: 80, ry: 80, width: 340, height: 340, left: 85, top: 85 },
      { type: 'text', text: 'A', fontSize: 220, fontFamily: 'Outfit', fill: '#ffffff', left: 155, top: 120, fontWeight: '800' },
    ],
  },
  {
    id: 'shield',
    label: 'أمان',
    emoji: '🛡️',
    bg: '#0f172a',
    objects: [
      { type: 'circle', fill: '#3b82f6', radius: 160, left: 96, top: 96 },
      { type: 'text', text: '✓', fontSize: 200, fontFamily: 'Outfit', fill: '#ffffff', left: 145, top: 110, fontWeight: '700' },
    ],
  },
  {
    id: 'leaf-icon',
    label: 'طبيعة',
    emoji: '🌿',
    bg: '#052e16',
    objects: [
      { type: 'circle', fill: '#16a34a', radius: 180, left: 80, top: 80 },
      { type: 'text', text: '🌿', fontSize: 220, fontFamily: 'Outfit', fill: '#ffffff', left: 90, top: 100 },
    ],
  },
];

const SIGNATURE_TEMPLATES = [
  {
    id: 'sig-classic',
    label: 'كلاسيكي',
    emoji: '✍️',
    bg: '#fffef7',
    objects: [
      { type: 'text', text: 'اسمك هنا', fontSize: 90, fontFamily: 'Amiri', fill: '#0f1115', left: 120, top: 80, fontWeight: 'bold', fontStyle: 'italic' },
      { type: 'rect', fill: '#0f1115', rx: 0, ry: 0, width: 560, height: 3, left: 120, top: 195 },
    ],
  },
  {
    id: 'sig-modern',
    label: 'عصري',
    emoji: '🖊️',
    bg: '#0f1115',
    objects: [
      { type: 'text', text: 'YOUR NAME', fontSize: 70, fontFamily: 'Outfit', fill: '#ffffff', left: 150, top: 80, fontWeight: '800', charSpacing: 120 },
      { type: 'rect', fill: '#6366f1', rx: 6, ry: 6, width: 80, height: 6, left: 150, top: 180 },
      { type: 'text', text: 'Designer & Creator', fontSize: 24, fontFamily: 'Outfit', fill: '#64748b', left: 150, top: 210 },
    ],
  },
  {
    id: 'sig-gold',
    label: 'ذهبي',
    emoji: '✨',
    bg: '#0a0804',
    objects: [
      { type: 'text', text: 'الاسم بالعربية', fontSize: 80, fontFamily: 'Amiri', fill: '#c9a227', left: 80, top: 70, fontWeight: 'bold' },
      { type: 'rect', fill: 'transparent', stroke: '#c9a227', strokeWidth: 2, rx: 0, ry: 0, width: 640, height: 240, left: 80, top: 30 },
    ],
  },
];

const LOGO_ICONS = [
  { label: 'نجمة', emoji: '⭐', svg: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' },
  { label: 'قلب', emoji: '❤', svg: 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z' },
  { label: 'برق', emoji: '⚡', svg: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z' },
  { label: 'هلال', emoji: '🌙', svg: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' },
  { label: 'عين', emoji: '👁', svg: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zm11 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6z' },
];

const ICON_LIBRARY = [
  { label: 'نجمة', emoji: '⭐', svg: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' },
  { label: 'قلب', emoji: '❤', svg: 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z' },
  { label: 'برق', emoji: '⚡', svg: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z' },
  { label: 'علامة', emoji: '✓', svg: 'M20 6L9 17l-5-5' },
  { label: 'موجة', emoji: '〰', svg: 'M2 12C4 8 6 6 8 8s4 6 6 4 4-6 6-4' },
];

const SIGNATURE_ICONS = [
  { label: 'قلم', emoji: '✏️', svg: 'M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7' },
  { label: 'بريد', emoji: '✉️', svg: 'M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zm0 2l8 5 8-5' },
  { label: 'هاتف', emoji: '📞', svg: 'M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13 19.79 19.79 0 0 1 1.61 4.4 2 2 0 0 1 3.59 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.16 6.16l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z' },
  { label: 'موقع', emoji: '🌐', svg: 'M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zm0 0c-2.76 4-2.76 16 0 16m0 0c2.76-4 2.76-16 0-16M2 12h20' },
];

const ORNAMENTS = [
  { label: 'تاج', emoji: '👑', svg: 'M2 20h20v2H2v-2zM4 18l2-10 3 4 3-8 3 8 3-4 2 10H4z' },
  { label: 'درع', emoji: '🛡️', svg: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z' },
  { label: 'معين', emoji: '♦', svg: 'M12 2l8 10-8 10L4 12z' },
  { label: 'وردة', emoji: '🌸', svg: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z' },
];

export const FALLBACK_BOOTSTRAP = {
  fonts: {
    general: ALL_FONTS,
    signature: [
      ...SIGNATURE_FONTS,
      ...ALL_FONTS.filter((font) => !SIGNATURE_FONTS.some((signatureFont) => signatureFont.value === font.value)),
    ],
  },
  templates: {
    logo: LOGO_TEMPLATES,
    icon: ICON_TEMPLATES,
    signature: SIGNATURE_TEMPLATES,
  },
  icons: {
    logo: LOGO_ICONS,
    icon: ICON_LIBRARY,
    signature: SIGNATURE_ICONS,
  },
  ornaments: ORNAMENTS,
  sizes: {
    logo: LOGO_SIZES,
    icon: ICON_SIZES,
    signature: SIGNATURE_SIZES,
  },
  settings: {
    ai_enabled: true,
    language: 'en',
    theme: 'dark',
  },
  ai_hints: {
    icon: 'مثال: أيقونة تطبيق بتصميم مسطح، رمز البرق الأزرق على خلفية داكنة',
    signature: 'مثال: توقيع إلكتروني أنيق باسم "محمد" بخط عربي ذهبي على خلفية داكنة',
    logo: 'مثال: أسد هادئ بأسلوب فيكتور مسطح لشركة تقنية، لا نص',
  },
};
