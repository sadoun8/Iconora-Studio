import {
  ICON_SIZES, ICON_TEMPLATES, ICON_SVG_ICONS,
  SIG_SIZES, SIG_TEMPLATES, SIG_SVG_ICONS, SIG_CALLIGRAPHY_FONTS,
  ORNAMENTS
} from '../sectionConfigs.js';

// ============================================================
// CONSTANTS (Fallback Bootstrap Data)
// ============================================================
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

const CANVAS_SIZES = [
  { label: 'مربع 800×800', w: 800, h: 800 },
  { label: 'أفقي 1200×600', w: 1200, h: 600 },
  { label: 'عمودي 600×900', w: 600, h: 900 },
  { label: 'شعار 512×512', w: 512, h: 512 },
];

const TEMPLATES = [
  {
    id: 'coffee', label: 'مقهى', emoji: '☕', bg: '#2d1b0e',
    objects: [
      { type: 'rect', fill: '#c8860a', rx: 70, ry: 70, width: 320, height: 320, left: 240, top: 240 },
      { type: 'text', text: 'مَقهى', fontSize: 80, fontFamily: 'Amiri', fill: '#fff', left: 270, top: 288, fontWeight: 'bold' },
      { type: 'text', text: 'C A F É', fontSize: 20, fontFamily: 'Outfit', fill: '#c8860a', left: 318, top: 420, charSpacing: 250 },
    ]
  },
  {
    id: 'tech', label: 'تقنية', emoji: '⚡', bg: '#0d0d1f',
    objects: [
      { type: 'rect', fill: 'transparent', stroke: '#6366f1', strokeWidth: 3, rx: 16, ry: 16, width: 340, height: 120, left: 230, top: 310 },
      { type: 'text', text: 'TECH', fontSize: 68, fontFamily: 'Outfit', fill: '#818cf8', left: 265, top: 316, fontWeight: '800' },
      { type: 'text', text: 'نصنع المستقبل', fontSize: 22, fontFamily: 'Cairo', fill: '#64748b', left: 280, top: 450 },
    ]
  },
  {
    id: 'elegant', label: 'أناقة', emoji: '✨', bg: '#080808',
    objects: [
      { type: 'text', text: 'LUXE', fontSize: 96, fontFamily: 'Georgia', fill: '#c9a227', left: 230, top: 310, fontWeight: 'bold' },
      { type: 'text', text: '— النخبـة —', fontSize: 26, fontFamily: 'Amiri', fill: '#64748b', left: 290, top: 435 },
    ]
  },
  {
    id: 'minimal', label: 'مينيمال', emoji: '◻️', bg: '#f8fafc',
    objects: [
      { type: 'rect', fill: '#0f1115', rx: 10, ry: 10, width: 340, height: 100, left: 230, top: 350 },
      { type: 'text', text: 'BRAND', fontSize: 50, fontFamily: 'Outfit', fill: '#ffffff', left: 265, top: 368, fontWeight: '700', charSpacing: 200 },
    ]
  },
  {
    id: 'sports', label: 'رياضة', emoji: '🏆', bg: '#0a1628',
    objects: [
      { type: 'rect', fill: '#f59e0b', rx: 0, ry: 0, width: 400, height: 12, left: 200, top: 390 },
      { type: 'text', text: 'CHAMPIONS', fontSize: 54, fontFamily: 'Outfit', fill: '#ffffff', left: 200, top: 310, fontWeight: '800', charSpacing: 80 },
      { type: 'text', text: 'أبطال', fontSize: 40, fontFamily: 'Cairo', fill: '#f59e0b', left: 320, top: 415, fontWeight: 'bold' },
    ]
  },
  {
    id: 'restaurant', label: 'مطعم', emoji: '🍽️', bg: '#1a0a04',
    objects: [
      { type: 'circle', fill: 'transparent', stroke: '#b45309', strokeWidth: 4, radius: 160, left: 240, top: 240 },
      { type: 'text', text: 'مطعــم', fontSize: 62, fontFamily: 'Amiri', fill: '#fbbf24', left: 280, top: 318, fontWeight: 'bold' },
      { type: 'text', text: 'RESTAURANT', fontSize: 16, fontFamily: 'Outfit', fill: '#b45309', left: 263, top: 407, charSpacing: 180 },
    ]
  },
  {
    id: 'studio', label: 'استوديو', emoji: '🎨', bg: '#0f0520',
    objects: [
      { type: 'rect', fill: '#7c3aed', rx: 50, ry: 50, width: 120, height: 120, left: 340, top: 240 },
      { type: 'text', text: 'STUDIO', fontSize: 56, fontFamily: 'Outfit', fill: '#ffffff', left: 248, top: 385, fontWeight: '800', charSpacing: 120 },
      { type: 'text', text: 'تصميم إبداعي', fontSize: 20, fontFamily: 'Cairo', fill: '#a78bfa', left: 295, top: 455 },
    ]
  },
  {
    id: 'medical', label: 'طب', emoji: '⚕️', bg: '#f0fdf4',
    objects: [
      { type: 'circle', fill: '#16a34a', radius: 100, left: 300, top: 200 },
      { type: 'rect', fill: '#ffffff', rx: 4, ry: 4, width: 30, height: 100, left: 370, top: 250 },
      { type: 'rect', fill: '#ffffff', rx: 4, ry: 4, width: 100, height: 30, left: 335, top: 285 },
      { type: 'text', text: 'عيادة الشفاء', fontSize: 38, fontFamily: 'Cairo', fill: '#15803d', left: 275, top: 440, fontWeight: 'bold' },
    ]
  },
];

const SVG_ICONS = [
  { label: 'نجمة', emoji: '⭐', svg: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' },
  { label: 'قلب', emoji: '❤', svg: 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z' },
  { label: 'برق', emoji: '⚡', svg: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z' },
  { label: 'خاتم', emoji: '💎', svg: 'M6 2l-4 6 10 14L22 8l-4-6H6zM3.43 8L6.37 4h11.26l2.94 4H3.43zm8.57 11.8L4.56 10h14.88L12 19.8z' },
  { label: 'شعلة', emoji: '🔥', svg: 'M13.5 0.67s.74 2.65.74 4.8c0 2.06-1.35 3.73-3.41 3.73-2.07 0-3.63-1.67-3.63-3.73l.03-.36C5.21 7.51 4 10.62 4 14c0 4.42 3.58 8 8 8s8-3.58 8-8C20 8.61 17.41 3.8 13.5.67z' },
  { label: 'ورقة', emoji: '🍃', svg: 'M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1-2.3A4.49 4.49 0 0 0 8 20C19 20 22 3 22 3c-1 2-8 2-8 2z' },
  { label: 'هلال', emoji: '🌙', svg: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' },
  { label: 'عين', emoji: '👁', svg: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zm11 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6z' },
  { label: 'جبل', emoji: '⛰️', svg: 'M3 17l6-12 4 7 2.5-4L21 17H3z' },
  { label: 'اللانهاية', emoji: '∞', svg: 'M18.6 6.62c-1.44 0-2.8.56-3.77 1.53L12 10.66 10.48 12h.01L7.8 14.39c-.64.64-1.49.99-2.4.99-1.87 0-3.39-1.51-3.39-3.38S3.53 8.62 5.4 8.62c.91 0 1.76.35 2.44 1.03l1.13 1 1.51-1.34L9.22 8.2C8.2 7.18 6.84 6.62 5.4 6.62 2.42 6.62 0 9.04 0 12s2.42 5.38 5.4 5.38c1.44 0 2.8-.56 3.77-1.53l2.83-2.51.01.01L13.52 12h-.01l2.69-2.39c.64-.64 1.49-.99 2.4-.99 1.87 0 3.39 1.51 3.39 3.38s-1.52 3.38-3.39 3.38c-.9 0-1.76-.35-2.44-1.03l-1.14-1.01-1.51 1.34 1.27 1.12c1.02 1.01 2.37 1.57 3.82 1.57 2.98 0 5.4-2.41 5.4-5.38s-2.42-5.38-5.4-5.38z' },
  { label: 'موجة', emoji: '🌊', svg: 'M2 8c1.5-2 3-2 4.5 0s3 2 4.5 0 3-2 4.5 0 3 2 4.5 0M2 14c1.5-2 3-2 4.5 0s3 2 4.5 0 3-2 4.5 0 3 2 4.5 0' },
  { label: 'صاروخ', emoji: '🚀', svg: 'M12 2.5s4 2 5.5 8-2 10.5-5.5 11-5.5-1-7-5.5S5 7.5 12 2.5z M9 11h6M10 14h4' },
];

export const FALLBACK_BOOTSTRAP = {
  fonts: {
    general: ALL_FONTS,
    signature: [...SIG_CALLIGRAPHY_FONTS, ...ALL_FONTS.filter(f => !SIG_CALLIGRAPHY_FONTS.find(s => s.value === f.value))],
  },
  templates: {
    logo: TEMPLATES,
    icon: ICON_TEMPLATES,
    signature: SIG_TEMPLATES,
  },
  icons: {
    logo: SVG_ICONS,
    icon: ICON_SVG_ICONS,
    signature: SIG_SVG_ICONS,
  },
  ornaments: ORNAMENTS,
  sizes: {
    logo: CANVAS_SIZES,
    icon: ICON_SIZES,
    signature: SIG_SIZES,
  },
  settings: {
    ai_enabled: true,
    language: 'en',
    theme: 'dark',
  },
};
