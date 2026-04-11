// Section configurations — all three designers share the same engine
// but with different canvas sizes, templates, and tool sets.

// ============================================================
// ICON DESIGNER SECTION CONFIG
// ============================================================
export const ICON_SIZES = [
  { label: 'App Icon 512×512', w: 512, h: 512 },
  { label: 'Favicon 32×32',    w: 32,  h: 32  },
  { label: 'Icon 128×128',     w: 128, h: 128 },
  { label: 'Icon 256×256',     w: 256, h: 256 },
];

export const ICON_TEMPLATES = [
  {
    id: 'app-icon',
    label: 'تطبيق',
    emoji: '📱',
    bg: '#6366f1',
    objects: [
      { type: 'rect', fill: 'rgba(255,255,255,0.15)', rx: 80, ry: 80, width: 340, height: 340, left: 85, top: 85 },
      { type: 'text', text: 'A', fontSize: 220, fontFamily: 'Outfit', fill: '#ffffff', left: 155, top: 120, fontWeight: '800' },
    ]
  },
  {
    id: 'shield',
    label: 'أمان',
    emoji: '🛡️',
    bg: '#0f172a',
    objects: [
      { type: 'circle', fill: '#3b82f6', radius: 160, left: 96, top: 96 },
      { type: 'text', text: '✓', fontSize: 200, fontFamily: 'Outfit', fill: '#ffffff', left: 145, top: 110, fontWeight: '700' },
    ]
  },
  {
    id: 'spark',
    label: 'طاقة',
    emoji: '⚡',
    bg: '#422006',
    objects: [
      { type: 'text', text: '⚡', fontSize: 300, fontFamily: 'Outfit', fill: '#f59e0b', left: 80, top: 70 },
    ]
  },
  {
    id: 'lock',
    label: 'قفل',
    emoji: '🔒',
    bg: '#1e1b4b',
    objects: [
      { type: 'rect', fill: '#6366f1', rx: 60, ry: 60, width: 280, height: 180, left: 115, top: 245 },
      { type: 'circle', fill: 'transparent', stroke: '#6366f1', strokeWidth: 40, radius: 100, left: 156, top: 70 },
      { type: 'circle', fill: '#ffffff', radius: 30, left: 222, top: 310 },
    ]
  },
  {
    id: 'leaf-icon',
    label: 'طبيعة',
    emoji: '🌿',
    bg: '#052e16',
    objects: [
      { type: 'circle', fill: '#16a34a', radius: 180, left: 80, top: 80 },
      { type: 'text', text: '🌿', fontSize: 220, fontFamily: 'Outfit', fill: '#ffffff', left: 90, top: 100 },
    ]
  },
  {
    id: 'camera',
    label: 'كاميرا',
    emoji: '📷',
    bg: '#1a1a1a',
    objects: [
      { type: 'rect', fill: '#374151', rx: 40, ry: 40, width: 360, height: 280, left: 76, top: 155 },
      { type: 'circle', fill: '#6b7280', radius: 90, left: 166, top: 200 },
      { type: 'circle', fill: '#111827', radius: 60, left: 196, top: 230 },
      { type: 'circle', fill: '#1d4ed8', radius: 25, left: 231, top: 265 },
    ]
  },
];

export const ICON_SVG_ICONS = [
  { label: 'نجمة', emoji: '⭐', svg: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' },
  { label: 'قلب',  emoji: '❤',  svg: 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z' },
  { label: 'برق',  emoji: '⚡', svg: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z' },
  { label: 'هلال', emoji: '🌙', svg: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' },
  { label: 'عين',  emoji: '👁', svg: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zm11 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6z' },
  { label: 'علامة', emoji: '✓', svg: 'M20 6L9 17l-5-5' },
  { label: 'موجة', emoji: '〰',  svg: 'M2 12C4 8 6 6 8 8s4 6 6 4 4-6 6-4' },
  { label: 'X',    emoji: '✖',  svg: 'M18 6L6 18M6 6l12 12' },
];

// ============================================================
// SIGNATURE DESIGNER SECTION CONFIG
// ============================================================
export const SIG_SIZES = [
  { label: 'توقيع 800×300',  w: 800, h: 300 },
  { label: 'توقيع 600×200',  w: 600, h: 200 },
  { label: 'مربع 400×400',   w: 400, h: 400 },
  { label: 'بانر 1200×400',  w: 1200, h: 400 },
];

export const SIG_CALLIGRAPHY_FONTS = [
  { label: 'Amiri (خط عربي كلاسيكي)',       value: 'Amiri' },
  { label: 'Scheherazade (خط قرآني)',        value: 'Scheherazade New' },
  { label: 'Noto Naskh (نسخ)',            value: 'Noto Naskh Arabic' },
  { label: 'Cairo (عصري)',                value: 'Cairo' },
  { label: 'Georgia (لاتيني كلاسيكي)',     value: 'Georgia' },
  { label: 'Courier New (مونوسبيس)',       value: 'Courier New' },
];

export const SIG_TEMPLATES = [
  {
    id: 'sig-classic',
    label: 'كلاسيكي',
    emoji: '✍️',
    bg: '#fffef7',
    objects: [
      { type: 'text', text: 'اسمك هنا', fontSize: 90, fontFamily: 'Amiri', fill: '#0f1115', left: 120, top: 80, fontWeight: 'bold', fontStyle: 'italic' },
      { type: 'rect', fill: '#0f1115', rx: 0, ry: 0, width: 560, height: 3, left: 120, top: 195 },
    ]
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
    ]
  },
  {
    id: 'sig-gold',
    label: 'ذهبي',
    emoji: '✨',
    bg: '#0a0804',
    objects: [
      { type: 'text', text: 'الاسم بالعربية', fontSize: 80, fontFamily: 'Amiri', fill: '#c9a227', left: 80, top: 70, fontWeight: 'bold' },
      { type: 'rect', fill: 'transparent', stroke: '#c9a227', strokeWidth: 2, rx: 0, ry: 0, width: 640, height: 240, left: 80, top: 30 },
    ]
  },
  {
    id: 'sig-minimal',
    label: 'بسيط',
    emoji: '⬜',
    bg: '#f8fafc',
    objects: [
      { type: 'text', text: 'Name', fontSize: 100, fontFamily: 'Georgia', fill: '#0f1115', left: 180, top: 70, fontStyle: 'italic' },
    ]
  },
  {
    id: 'sig-stamp',
    label: 'ختم',
    emoji: '🔵',
    bg: '#f8fafc',
    objects: [
      { type: 'circle', fill: 'transparent', stroke: '#1e40af', strokeWidth: 5, radius: 140, left: 310, top: 10 },
      { type: 'circle', fill: 'transparent', stroke: '#1e40af', strokeWidth: 2, radius: 120, left: 330, top: 30 },
      { type: 'text', text: 'شركتك', fontSize: 52, fontFamily: 'Cairo', fill: '#1e40af', left: 360, top: 95, fontWeight: 'bold' },
      { type: 'text', text: 'COMPANY NAME', fontSize: 18, fontFamily: 'Outfit', fill: '#1e40af', left: 342, top: 178, charSpacing: 80 },
    ]
  },
  {
    id: 'sig-arabic',
    label: 'خطاط',
    emoji: '🕌',
    bg: '#faf5eb',
    objects: [
      { type: 'text', text: 'بِسْمِ اللَّهِ', fontSize: 90, fontFamily: 'Scheherazade New', fill: '#7c2d12', left: 140, top: 60, fontWeight: 'bold' },
      { type: 'text', text: 'الرَّحْمَٰنِ الرَّحِيمِ', fontSize: 58, fontFamily: 'Scheherazade New', fill: '#7c2d12', left: 110, top: 175 },
    ]
  },
];

export const SIG_SVG_ICONS = [
  { label: 'قلم',    emoji: '✏️', svg: 'M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7' },
  { label: 'بريد',  emoji: '✉️', svg: 'M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zm0 2l8 5 8-5' },
  { label: 'هاتف', emoji: '📞', svg: 'M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13 19.79 19.79 0 0 1 1.61 4.4 2 2 0 0 1 3.59 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.16 6.16l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z' },
  { label: 'موقع', emoji: '🌐', svg: 'M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zm0 0c-2.76 4-2.76 16 0 16m0 0c2.76-4 2.76-16 0-16M2 12h20' },
  { label: 'لينكد', emoji: '💼', svg: 'M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z' },
  { label: 'نجمة',  emoji: '⭐', svg: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' },
];

// ============================================================
// SVG ORNAMENTS & BADGES LIBRARY (SHARED)
// ============================================================
export const ORNAMENTS = [
  { label: 'تاج',     emoji: '👑', svg: 'M2 20h20v2H2v-2zM4 18l2-10 3 4 3-8 3 8 3-4 2 10H4z' },
  { label: 'درع',     emoji: '🛡️', svg: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z' },
  { label: 'زخرفة 1', emoji: '〰️', svg: 'M12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z M2 12c0 5.52 4.48 10 10 10s10-4.48 10-10H22c0 5.52-4.48 10-10 10S2 17.52 2 12H0z' },
  { label: 'غار',     emoji: '🌿', svg: 'M21.58 12c0-5.3-4.3-9.58-9.58-9.58C6.7 2.42 2.42 6.7 2.42 12S6.7 21.58 12 21.58c5.3 0 9.58-4.3 9.58-9.58zM12 20.42c-4.64 0-8.42-3.78-8.42-8.42 0-4.64 3.78-8.42 8.42-8.42s8.42 3.78 8.42 8.42c0 4.64-3.78 8.42-8.42 8.42z' },
  { label: 'شريط',    emoji: '🎀', svg: 'M16 8l-4 4-4-4v14l4-2 4 2V8z M4 4h16c1.1 0 2 .9 2 2v6c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z' },
  { label: 'معين',    emoji: '♦️', svg: 'M12 2l8 10-8 10L4 12z' },
  { label: 'نقطة',    emoji: '•', svg: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z' },
  { label: 'وردة',    emoji: '🌸', svg: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z' },
];
