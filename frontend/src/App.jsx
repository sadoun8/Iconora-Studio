import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as fabric from 'fabric';
import {
  Sparkles, Type, Download, Layers, MousePointer2, Wand2,
  Loader2, Undo2, Redo2, Trash2, Square, Circle,
  AlignCenter, Bold, Italic, Move, Image as ImageIcon,
  Save, FolderOpen, ChevronDown, X, TriangleAlert, Star,
  Settings2, Palette, Pentagon, PenLine, Hexagon, LayoutTemplate,
  Eye, EyeOff, Lock, Unlock, Copy, RefreshCw, Sliders,
  Pen, Eraser, Wind, ArrowUpDown, ZoomIn, ZoomOut, Maximize2,
  AlignLeft, AlignRight, AlignJustify, RotateCcw, Crop,
  FlipHorizontal, FlipVertical, ChevronUp, ChevronRight,
} from 'lucide-react';
import {
  ICON_SIZES, ICON_TEMPLATES, ICON_SVG_ICONS,
  SIG_SIZES, SIG_TEMPLATES, SIG_SVG_ICONS, SIG_CALLIGRAPHY_FONTS,
  ORNAMENTS
} from './sectionConfigs.js';
import './index.css';
import {
  createProject,
  exportProject,
  exportCanvas as exportCanvasApi,
  exportIconPack,
  fetchBootstrap,
  generateLogo,
  getHealth,
  getProject,
  getSettings,
  importProject as importProjectApi,
  listProjects,
  saveSettings,
  updateProject,
} from './lib/api.js';
import {
  NoticeModal,
  OpenProjectModal,
  SaveProjectModal,
  SettingsModal,
} from './components/AppModals.jsx';

// ============================================================
// CONSTANTS
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

const FALLBACK_BOOTSTRAP = {
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

const DEFAULT_SETTINGS_DRAFT = {
  theme: 'dark',
  language: 'en',
  default_quality: 95,
  auto_open_folder: false,
  ai_enabled: true,
  ai_endpoint: 'http://127.0.0.1:11434',
  ai_model: 'qwen2.5:7b-instruct',
  ai_timeout: 30,
};

// ============================================================
// HELPERS
// ============================================================
function getLayerLabel(obj) {
  if (!obj) return 'عنصر';
  if (obj.type === 'i-text' || obj.type === 'text') return `Ⓣ "${(obj.text || '').slice(0, 14)}"`;
  if (obj.type === 'image') return '🖼 صورة';
  if (obj.type === 'rect') return '▭ مستطيل';
  if (obj.type === 'circle') return '○ دائرة';
  if (obj.type === 'polygon') return '⬡ مضلع';
  if (obj.type === 'path') return '✏ مسار';
  if (obj.type === 'group') return '⊞ مجموعة';
  return obj.type || 'عنصر';
}

// Catmull-Rom to Bezier for smooth signature paths
function catmullRomToBezier(points) {
  if (points.length < 2) return '';
  let d = `M ${points[0].x} ${points[0].y}`;
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[Math.max(0, i - 1)];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = points[Math.min(points.length - 1, i + 2)];
    const cp1x = p1.x + (p2.x - p0.x) / 6;
    const cp1y = p1.y + (p2.y - p0.y) / 6;
    const cp2x = p2.x - (p3.x - p1.x) / 6;
    const cp2y = p2.y - (p3.y - p1.y) / 6;
    d += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${p2.x} ${p2.y}`;
  }
  return d;
}

// ============================================================
// MAIN APP
// ============================================================
export default function App() {
  const canvasRef = useRef(null);
  const [fabricCanvas, setFabricCanvas] = useState(null);
  const [activeObject, setActiveObject] = useState(null);
  const [layers, setLayers] = useState([]);
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const historyRef = useRef({ stack: [], idx: -1, paused: false });
  const [canvasSize, setCanvasSize] = useState({ w: 800, h: 800 });
  const [zoom, setZoom] = useState(100);
  const [activePropTab, setActivePropTab] = useState('style');
  const [section, setSection] = useState('logo');

  // ── Active tool ──
  const [activeTool, setActiveTool] = useState('select'); // select | pen | draw | eraser

  // ── Drawing state for freehand signature ──
  const isDrawingRef = useRef(false);
  const drawPointsRef = useRef([]);
  const drawTimesRef = useRef([]);
  const drawOverlayRef = useRef(null); // overlay canvas for live preview
  const drawColorRef = useRef('#0f1115');
  const drawSizeRef = useRef(4);

  // ── Snapping guides state ──
  const [snapEnabled, setSnapEnabled] = useState(true);
  const snapLinesRef = useRef({ h: [], v: [] });

  // ── Curved text modal ──
  const [showCurvedTextModal, setShowCurvedTextModal] = useState(false);
  // editingCurvedId: if non-null we're editing an existing curved-text group
  const [editingCurvedId, setEditingCurvedId] = useState(null);
  const [curvedTextValue, setCurvedTextValue] = useState('نص مقوس على القوس');
  const [curvedTextRadius, setCurvedTextRadius] = useState(200);
  const [curvedTextFont, setCurvedTextFont] = useState('Cairo');
  const [curvedTextSize, setCurvedTextSize] = useState(36);
  const [curvedTextColor, setCurvedTextColor] = useState('#6366f1');
  const [curvedTextStartAngle, setCurvedTextStartAngle] = useState(180);

  // ── SVG Filter modal ──
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [blurAmount, setBlurAmount] = useState(0);

  // ── Export transparent PNG modal ──
  const [bootstrap, setBootstrap] = useState(FALLBACK_BOOTSTRAP);
  const [bootstrapError, setBootstrapError] = useState('');
  const [healthInfo, setHealthInfo] = useState(null);
  const [healthError, setHealthError] = useState('');
  const [currentProjectId, setCurrentProjectId] = useState('');
  const [currentProjectName, setCurrentProjectName] = useState('');
  const [showSaveProjectModal, setShowSaveProjectModal] = useState(false);
  const [saveProjectDraft, setSaveProjectDraft] = useState('');
  const [showProjectsModal, setShowProjectsModal] = useState(false);
  const [availableProjects, setAvailableProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [noticeModal, setNoticeModal] = useState({ open: false, title: '', message: '' });
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [settingsDraft, setSettingsDraft] = useState(DEFAULT_SETTINGS_DRAFT);
  const [settingsError, setSettingsError] = useState('');
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const isApplyingProjectRef = useRef(false);

  // Derived section config
  const sectionConfig = (() => {
    const runtimeTemplates = bootstrap.templates || FALLBACK_BOOTSTRAP.templates;
    const runtimeSizes = bootstrap.sizes || FALLBACK_BOOTSTRAP.sizes;
    const runtimeIcons = bootstrap.icons || FALLBACK_BOOTSTRAP.icons;
    const runtimeFonts = bootstrap.fonts || FALLBACK_BOOTSTRAP.fonts;
    if (section === 'icon') return {
      templates: runtimeTemplates.icon || FALLBACK_BOOTSTRAP.templates.icon, sizes: runtimeSizes.icon || FALLBACK_BOOTSTRAP.sizes.icon, icons: runtimeIcons.icon || FALLBACK_BOOTSTRAP.icons.icon,
      defaultSize: (runtimeSizes.icon || FALLBACK_BOOTSTRAP.sizes.icon)?.[0] || { w: 512, h: 512 }, fonts: runtimeFonts.general || FALLBACK_BOOTSTRAP.fonts.general,
      aiHint: 'مثال: أيقونة تطبيق بتصميم مسطح، رمز البرق الأزرق على خلفية داكنة',
    };
    if (section === 'signature') return {
      templates: runtimeTemplates.signature || FALLBACK_BOOTSTRAP.templates.signature, sizes: runtimeSizes.signature || FALLBACK_BOOTSTRAP.sizes.signature, icons: runtimeIcons.signature || FALLBACK_BOOTSTRAP.icons.signature,
      defaultSize: (runtimeSizes.signature || FALLBACK_BOOTSTRAP.sizes.signature)?.[0] || { w: 800, h: 300 }, fonts: runtimeFonts.signature || FALLBACK_BOOTSTRAP.fonts.signature,
      aiHint: 'مثال: توقيع إلكتروني أنيق باسم "محمد" بخط عربي ذهبي على خلفية داكنة',
    };
    return {
      templates: runtimeTemplates.logo || FALLBACK_BOOTSTRAP.templates.logo, sizes: runtimeSizes.logo || FALLBACK_BOOTSTRAP.sizes.logo, icons: runtimeIcons.logo || FALLBACK_BOOTSTRAP.icons.logo,
      defaultSize: (runtimeSizes.logo || FALLBACK_BOOTSTRAP.sizes.logo)?.[0] || { w: 800, h: 800 }, fonts: runtimeFonts.general || FALLBACK_BOOTSTRAP.fonts.general,
      aiHint: 'مثال: أسد هادئ بأسلوب فيكتور مسطح لشركة تقنية، لا نص',
    };
  })();
  const selectedCanvasLabel = sectionConfig.sizes.find(size => size.w === canvasSize.w && size.h === canvasSize.h)?.label
    || sectionConfig.sizes[0]?.label
    || '';
  const runtimeSettings = { ...DEFAULT_SETTINGS_DRAFT, ...(bootstrap.settings || {}) };
  const isAiEnabled = runtimeSettings.ai_enabled !== false;

  const showNotice = useCallback((title, message) => {
    setNoticeModal({ open: true, title, message });
  }, []);

  // AI State
  const [aiPrompt, setAiPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [aiError, setAiError] = useState('');

  // Object Properties
  const [fillColor, setFillColor] = useState('#6366f1');
  const [strokeColor, setStrokeColor] = useState('#6366f1');
  const [strokeWidth, setStrokeWidth] = useState(0);
  const [opacity, setOpacity] = useState(100);
  const [fontSize, setFontSize] = useState(48);
  const [fontFamily, setFontFamily] = useState('Cairo');
  const [isBold, setIsBold] = useState(false);
  const [isItalic, setIsItalic] = useState(false);
  const [shadowBlur, setShadowBlur] = useState(0);
  const [cornerRadius, setCornerRadius] = useState(0);
  const [posX, setPosX] = useState(0);
  const [posY, setPosY] = useState(0);
  const [angle, setAngle] = useState(0);
  const [skewX, setSkewX] = useState(0);
  const [charSpacing, setCharSpacing] = useState(0);
  const [lineHeight, setLineHeight] = useState(1.16);
  const [textAlign, setTextAlign] = useState('left');

  // ── Draw color/size for signature tool ──
  const [drawColor, setDrawColor] = useState('#0f1115');
  const [drawSize, setDrawSize] = useState(4);

  // ── Layer visibility/lock ──
  const [layerStates, setLayerStates] = useState({}); // { objId: { visible, locked } }

  // ── Sidebar collapse ──
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [panelCollapsed, setPanelCollapsed] = useState(false);

  // ── Active sidebar tab ──
  const [sidebarTab, setSidebarTab] = useState('tools'); // tools | templates | icons | ai | layers

  useEffect(() => {
    let mounted = true;

    const loadBootstrapData = async () => {
      try {
        const payload = await fetchBootstrap();
        if (!mounted) return;
        setBootstrap({
          ...FALLBACK_BOOTSTRAP,
          ...payload,
          fonts: { ...FALLBACK_BOOTSTRAP.fonts, ...(payload.fonts || {}) },
          templates: { ...FALLBACK_BOOTSTRAP.templates, ...(payload.templates || {}) },
          icons: { ...FALLBACK_BOOTSTRAP.icons, ...(payload.icons || {}) },
          sizes: { ...FALLBACK_BOOTSTRAP.sizes, ...(payload.sizes || {}) },
          ornaments: payload.ornaments || FALLBACK_BOOTSTRAP.ornaments,
          settings: { ...FALLBACK_BOOTSTRAP.settings, ...(payload.settings || {}) },
        });
        setBootstrapError('');
      } catch (error) {
        if (mounted) {
          setBootstrapError(error.message || 'Failed to load runtime assets');
        }
      }
    };

    const loadHealthData = async () => {
      try {
        const payload = await getHealth();
        if (!mounted) return;
        setHealthInfo(payload);
        setHealthError('');
      } catch (error) {
        if (mounted) {
          setHealthError(error.message || 'Failed to load backend health');
        }
      }
    };

    const loadSettingsData = async () => {
      try {
        const payload = await getSettings();
        if (!mounted) return;
        setBootstrap(prev => ({
          ...prev,
          settings: { ...DEFAULT_SETTINGS_DRAFT, ...(prev.settings || {}), ...payload },
        }));
        setSettingsDraft(prev => ({ ...prev, ...payload }));
      } catch (error) {
        if (mounted) {
          setSettingsError(error.message || 'Failed to load runtime settings');
        }
      }
    };

    loadBootstrapData();
    loadHealthData();
    loadSettingsData();
    return () => {
      mounted = false;
    };
  }, []);

  // --------------------------------------------------------
  // CANVAS INIT
  // --------------------------------------------------------
  useEffect(() => {
    const canvas = new fabric.Canvas(canvasRef.current, {
      width: 800, height: 800,
      backgroundColor: '#ffffff',
      preserveObjectStacking: true,
      selectionBorderColor: '#6366f1',
      selectionColor: 'rgba(99,102,241,0.08)',
      selectionLineWidth: 1.5,
    });
    setFabricCanvas(canvas);

    const onSelect = (e) => {
      const obj = e.selected?.[0];
      setActiveObject(obj || null);
      syncPropsFromObject(obj);
    };
    const onDeselect = () => setActiveObject(null);

    canvas.on('selection:created', onSelect);
    canvas.on('selection:updated', onSelect);
    canvas.on('selection:cleared', onDeselect);

    canvas.on('object:modified', () => {
      saveSnapshot(canvas);
      refreshLayers(canvas);
      const obj = canvas.getActiveObject();
      if (obj) syncPropsFromObject(obj);
    });
    canvas.on('object:added', () => { saveSnapshot(canvas); refreshLayers(canvas); });
    canvas.on('object:removed', () => { saveSnapshot(canvas); refreshLayers(canvas); });

    saveSnapshot(canvas);
    return () => canvas.dispose();
  }, []); // eslint-disable-line

  // ── Section change ──
  useEffect(() => {
    if (!fabricCanvas) return;
    if (isApplyingProjectRef.current) return;
    const { w, h } = sectionConfig.defaultSize;
    historyRef.current.paused = true;
    fabricCanvas.clear();
    fabricCanvas.backgroundColor = '#ffffff';
    fabricCanvas.setDimensions({ width: w, height: h });
    fabricCanvas.requestRenderAll();
    setCanvasSize({ w, h });
    setLayers([]);
    setLayerStates({});
    setActiveObject(null);
    historyRef.current = { stack: [], idx: -1, paused: false };
    setHistory([]);
    setHistoryIndex(-1);
    setActiveTool('select');
    setCurrentProjectId('');
    setCurrentProjectName('');
  }, [section]); // eslint-disable-line

  // ── Tool change → update canvas interaction mode ──
  useEffect(() => {
    if (!fabricCanvas) return;
    if (activeTool === 'select') {
      fabricCanvas.isDrawingMode = false;
      fabricCanvas.selection = true;
      fabricCanvas.defaultCursor = 'default';
    } else if (activeTool === 'draw') {
      fabricCanvas.isDrawingMode = true;
      fabricCanvas.freeDrawingBrush.color = drawColor;
      fabricCanvas.freeDrawingBrush.width = drawSize;
      fabricCanvas.freeDrawingBrush.decimate = 4;
      fabricCanvas.defaultCursor = 'crosshair';
    } else if (activeTool === 'pen') {
      fabricCanvas.isDrawingMode = false;
      fabricCanvas.selection = false;
      fabricCanvas.defaultCursor = 'crosshair';
    }
  }, [activeTool, fabricCanvas, drawColor, drawSize]);

  // ── Snapping ──
  useEffect(() => {
    if (!fabricCanvas || !snapEnabled) return;
    const SNAP_DIST = 8;

    const onMoving = (e) => {
      const obj = e.target;
      if (!obj) return;
      const cw = fabricCanvas.width, ch = fabricCanvas.height;
      const ow = obj.getScaledWidth(), oh = obj.getScaledHeight();
      let { left, top } = obj;

      const snapH = [];
      const snapV = [];

      // Canvas center snaps
      const cx = cw / 2, cy = ch / 2;
      // Object center
      const ocx = left + ow / 2, ocy = top + oh / 2;

      if (Math.abs(ocx - cx) < SNAP_DIST) { obj.set('left', cx - ow / 2); snapV.push(cx); }
      if (Math.abs(ocy - cy) < SNAP_DIST) { obj.set('top', cy - oh / 2); snapH.push(cy); }
      if (Math.abs(left) < SNAP_DIST) { obj.set('left', 0); snapV.push(0); }
      if (Math.abs(top) < SNAP_DIST) { obj.set('top', 0); snapH.push(0); }
      if (Math.abs(left + ow - cw) < SNAP_DIST) { obj.set('left', cw - ow); snapV.push(cw); }
      if (Math.abs(top + oh - ch) < SNAP_DIST) { obj.set('top', ch - oh); snapH.push(ch); }

      snapLinesRef.current = { h: snapH, v: snapV };
    };

    const onMoved = () => { snapLinesRef.current = { h: [], v: [] }; };

    fabricCanvas.on('object:moving', onMoving);
    fabricCanvas.on('object:moved', onMoved);
    return () => {
      fabricCanvas.off('object:moving', onMoving);
      fabricCanvas.off('object:moved', onMoved);
    };
  }, [fabricCanvas, snapEnabled]);

  // ── Sync draw color to brush ──
  useEffect(() => {
    drawColorRef.current = drawColor;
    drawSizeRef.current = drawSize;
    if (fabricCanvas && fabricCanvas.freeDrawingBrush) {
      fabricCanvas.freeDrawingBrush.color = drawColor;
      fabricCanvas.freeDrawingBrush.width = drawSize;
    }
  }, [drawColor, drawSize, fabricCanvas]);

  // --------------------------------------------------------
  // SYNC object properties → state
  // --------------------------------------------------------
  const syncPropsFromObject = useCallback((obj) => {
    if (!obj) return;
    setFillColor(obj.fill && typeof obj.fill === 'string' ? obj.fill : '#6366f1');
    setStrokeColor(obj.stroke || '#6366f1');
    setStrokeWidth(obj.strokeWidth || 0);
    setOpacity(Math.round((obj.opacity ?? 1) * 100));
    setShadowBlur(obj.shadow?.blur || 0);
    setCornerRadius(obj.rx || 0);
    setPosX(Math.round(obj.left || 0));
    setPosY(Math.round(obj.top || 0));
    setAngle(Math.round(obj.angle || 0));
    setSkewX(Math.round(obj.skewX || 0));
    if (obj.type === 'i-text' || obj.type === 'text') {
      setFontSize(obj.fontSize || 48);
      setFontFamily(obj.fontFamily || 'Cairo');
      setIsBold(obj.fontWeight === 'bold' || obj.fontWeight >= 700);
      setIsItalic(obj.fontStyle === 'italic');
      setCharSpacing(Math.round(obj.charSpacing || 0));
      setLineHeight(obj.lineHeight || 1.16);
      setTextAlign(obj.textAlign || 'left');
    }
  }, []);

  // --------------------------------------------------------
  // LAYERS
  // --------------------------------------------------------
  const refreshLayers = useCallback((canvas) => {
    if (!canvas) return;
    const objs = canvas.getObjects().slice().reverse();
    setLayers(objs.map((o, i) => ({ id: i, obj: o, label: getLayerLabel(o) })));
  }, []);

  const updateLayers = useCallback(() => {
    if (fabricCanvas) refreshLayers(fabricCanvas);
  }, [fabricCanvas, refreshLayers]);

  // ── Layer visibility ──
  const toggleLayerVisibility = (obj) => {
    const id = obj.__uid || (obj.__uid = Math.random().toString(36).slice(2));
    setLayerStates(prev => {
      const cur = prev[id] || { visible: true, locked: false };
      const visible = !cur.visible;
      obj.set('visible', visible);
      obj.set('selectable', !(!visible || cur.locked));
      fabricCanvas?.requestRenderAll();
      return { ...prev, [id]: { ...cur, visible } };
    });
  };

  const toggleLayerLock = (obj) => {
    const id = obj.__uid || (obj.__uid = Math.random().toString(36).slice(2));
    setLayerStates(prev => {
      const cur = prev[id] || { visible: true, locked: false };
      const locked = !cur.locked;
      obj.set('selectable', !(locked || !cur.visible));
      obj.set('evented', !locked);
      fabricCanvas?.requestRenderAll();
      return { ...prev, [id]: { ...cur, locked } };
    });
  };

  // --------------------------------------------------------
  // HISTORY
  // --------------------------------------------------------
  const saveSnapshot = useCallback((canvas) => {
    if (!canvas || historyRef.current.paused) return;
    const json = JSON.stringify({ ...canvas.toJSON(['id', '__uid']), backgroundColor: canvas.backgroundColor });
    const h = historyRef.current;
    const newStack = h.stack.slice(0, h.idx + 1);
    newStack.push(json);
    if (newStack.length > 40) newStack.shift();
    h.stack = newStack;
    h.idx = newStack.length - 1;
    setHistory([...newStack]);
    setHistoryIndex(h.idx);
  }, []);

  const restoreSnapshot = useCallback(async (canvas, jsonStr) => {
    const data = JSON.parse(jsonStr);
    await canvas.loadFromJSON(data);
    if (data.backgroundColor) canvas.backgroundColor = data.backgroundColor;
    canvas.requestRenderAll();
  }, []);

  const undo = useCallback(async () => {
    if (!fabricCanvas) return;
    const h = historyRef.current;
    if (h.idx <= 0) return;
    h.idx -= 1;
    h.paused = true;
    await restoreSnapshot(fabricCanvas, h.stack[h.idx]);
    h.paused = false;
    setHistoryIndex(h.idx);
    refreshLayers(fabricCanvas);
  }, [fabricCanvas, refreshLayers, restoreSnapshot]);

  const redo = useCallback(async () => {
    if (!fabricCanvas) return;
    const h = historyRef.current;
    if (h.idx >= h.stack.length - 1) return;
    h.idx += 1;
    h.paused = true;
    await restoreSnapshot(fabricCanvas, h.stack[h.idx]);
    h.paused = false;
    setHistoryIndex(h.idx);
    refreshLayers(fabricCanvas);
  }, [fabricCanvas, refreshLayers, restoreSnapshot]);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e) => {
      const isInput = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName);
      if (isInput) return;
      if ((e.ctrlKey || e.metaKey) && e.key === 'z') { e.preventDefault(); undo(); }
      if ((e.ctrlKey || e.metaKey) && e.key === 'y') { e.preventDefault(); redo(); }
      if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); deleteSelected(); }
      if (e.key === 'Escape') { setActiveTool('select'); }
      if (e.key === 'v') setActiveTool('select');
      if (e.key === 'p') setActiveTool('draw');
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [undo, redo]); // eslint-disable-line

  // --------------------------------------------------------
  // OBJECT ACTIONS
  // --------------------------------------------------------
  const addText = () => {
    if (!fabricCanvas) return;
    const text = new fabric.IText('نص جديد', {
      left: fabricCanvas.width / 2 - 50,
      top: fabricCanvas.height / 2 - 25,
      fontFamily: 'Cairo', fill: '#0f1115', fontSize: 56, fontWeight: 'bold',
    });
    fabricCanvas.add(text);
    fabricCanvas.setActiveObject(text);
    fabricCanvas.renderAll();
    text.enterEditing();
  };

  const addRect = () => {
    if (!fabricCanvas) return;
    const r = new fabric.Rect({
      left: fabricCanvas.width / 2 - 100, top: fabricCanvas.height / 2 - 60,
      fill: '#6366f1', width: 200, height: 120, rx: 12, ry: 12,
    });
    fabricCanvas.add(r);
    fabricCanvas.setActiveObject(r);
    fabricCanvas.renderAll();
  };

  const addCircle = () => {
    if (!fabricCanvas) return;
    const c = new fabric.Circle({
      left: fabricCanvas.width / 2 - 80, top: fabricCanvas.height / 2 - 80,
      fill: '#a855f7', radius: 80,
    });
    fabricCanvas.add(c);
    fabricCanvas.setActiveObject(c);
    fabricCanvas.renderAll();
  };

  const addPolygon = () => {
    if (!fabricCanvas) return;
    const pts = [];
    for (let i = 0; i < 6; i++) {
      pts.push({ x: 80 * Math.cos((i * 2 * Math.PI) / 6), y: 80 * Math.sin((i * 2 * Math.PI) / 6) });
    }
    const p = new fabric.Polygon(pts, {
      left: fabricCanvas.width / 2 - 80, top: fabricCanvas.height / 2 - 80, fill: '#ec4899',
    });
    fabricCanvas.add(p);
    fabricCanvas.setActiveObject(p);
    fabricCanvas.renderAll();
  };

  // Add a star shape
  const addStar = () => {
    if (!fabricCanvas) return;
    const pts = [];
    for (let i = 0; i < 10; i++) {
      const r = i % 2 === 0 ? 90 : 40;
      pts.push({ x: r * Math.cos((i * 2 * Math.PI) / 10 - Math.PI / 2), y: r * Math.sin((i * 2 * Math.PI) / 10 - Math.PI / 2) });
    }
    const star = new fabric.Polygon(pts, {
      left: fabricCanvas.width / 2 - 90, top: fabricCanvas.height / 2 - 90, fill: '#f59e0b',
    });
    fabricCanvas.add(star);
    fabricCanvas.setActiveObject(star);
    fabricCanvas.renderAll();
  };

  const addSvgIcon = (icon) => {
    if (!fabricCanvas) return;
    const svgStr = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="${icon.svg}"/></svg>`;
    fabric.loadSVGFromString(svgStr).then(({ objects }) => {
      const group = fabric.util.groupSVGElements(objects);
      group.set({
        left: fabricCanvas.width / 2 - 50,
        top: fabricCanvas.height / 2 - 50,
        fill: '#6366f1',
        scaleX: section === 'signature' ? 3 : 10,
        scaleY: section === 'signature' ? 3 : 10,
      });
      fabricCanvas.add(group);
      fabricCanvas.setActiveObject(group);
      fabricCanvas.requestRenderAll();
    });
  };

  // ── CURVED TEXT (SVG textPath) — with unique ID & edit-in-place ──
  const buildCurvedSvgStr = (cw, ch, r, startAngleDeg, font, size, color, text) => {
    const cx = cw / 2, cy = ch / 2;
    const startAngleRad = (startAngleDeg * Math.PI) / 180;
    const endAngleRad = startAngleRad + Math.PI;
    const x1 = cx + r * Math.cos(startAngleRad);
    const y1 = cy + r * Math.sin(startAngleRad);
    const x2 = cx + r * Math.cos(endAngleRad);
    const y2 = cy + r * Math.sin(endAngleRad);
    // Use a stable (non-timestamp) path id so two renders don't produce duplicate IDs
    const pathId = 'curved-path-preview';
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${cw}" height="${ch}" overflow="visible">
  <defs><path id="${pathId}" d="M ${x1} ${y1} A ${r} ${r} 0 0 1 ${x2} ${y2}"/></defs>
  <text font-family="${font}" font-size="${size}" fill="${color}" overflow="visible">
    <textPath href="#${pathId}">${text}</textPath>
  </text>
</svg>`;
  };

    // Curved Text COMMIT (Converting perfect SVG to Fabric Image)
    const commitCurvedText = (overrideParam = null) => {
      if (!fabricCanvas) return;
      
      // Protect against React passing Synthetic Events instead of ID strings
      const isEvent = overrideParam && typeof overrideParam === 'object' && overrideParam.nativeEvent;
      const safeOverrideId = isEvent ? null : overrideParam;
      
      const resolvedId = safeOverrideId || editingCurvedId;
      const uniqueId = resolvedId || ('ct-' + Date.now());
      const r = curvedTextRadius;
      
      const startAngleRad = (curvedTextStartAngle * Math.PI) / 180;
      const isBottom = curvedTextStartAngle > 0 && curvedTextStartAngle < 180;
      const sweep = isBottom ? 0 : 1; 
      const arcSweep = 179; 
      const endAngleRad = startAngleRad + (arcSweep * Math.PI / 180);
      
      // We generate the exact SVG that works in the preview
      // using a large enough viewBox (800x800)
      const svgStr = `
        <svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800" overflow="visible">
          <defs>
            <path id="p-${uniqueId}" d="M ${400 + r * Math.cos(startAngleRad)} ${400 + r * Math.sin(startAngleRad)} A ${r} ${r} 0 0 ${sweep} ${400 + r * Math.cos(endAngleRad)} ${400 + r * Math.sin(endAngleRad)}" />
          </defs>
          <text font-family="${curvedTextFont}" font-size="${curvedTextSize}" fill="${curvedTextColor}" text-anchor="middle" direction="rtl">
            <textPath href="#p-${uniqueId}" startOffset="50%">${curvedTextValue}</textPath>
          </text>
        </svg>
      `;

      // Convert SVG to data URL to preserve Arabic textPath connections natively
      const svgDataUrl = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgStr);
      
      const imgEl = new Image();
      imgEl.onload = () => {
        const fImg = new fabric.Image(imgEl);
        
        fImg.__curvedTextId = uniqueId;
        fImg.__curvedMeta = {
          text: curvedTextValue, radius: curvedTextRadius, font: curvedTextFont,
          size: curvedTextSize, color: curvedTextColor, startAngle: curvedTextStartAngle,
        };

        // AGGRESSIVE DELETE OLD
        let foundExisting = false;
        const currentObjects = fabricCanvas.getObjects();
        for (let i = currentObjects.length - 1; i >= 0; i--) {
          const obj = currentObjects[i];
          if (obj.__curvedTextId === uniqueId) {
            fImg.set({
              left: obj.left, top: obj.top, angle: obj.angle,
              scaleX: obj.scaleX, scaleY: obj.scaleY,
              originX: obj.originX, originY: obj.originY
            });
            
            // Critical for Fabric JS: discard if it's active before removing it
            if (fabricCanvas.getActiveObject() === obj) {
              fabricCanvas.discardActiveObject();
            }
            fabricCanvas.remove(obj);
            foundExisting = true;
          }
        }

        if (!foundExisting) {
          const vCenter = fabricCanvas.getVpCenter();
          fImg.set({ left: vCenter.x, top: vCenter.y, originX: 'center', originY: 'center' });
        }

        fabricCanvas.add(fImg);
        fabricCanvas.setActiveObject(fImg);
        fabricCanvas.renderAll();
        
        // Only close modal if we didn't explicitly pass an override directly
        // (If safeOverrideId is passed, we're likely in the side panel, not modal)
        if (!safeOverrideId && typeof setShowCurvedTextModal === 'function') {
          setShowCurvedTextModal(false);
          setEditingCurvedId(null);
        }
      };
      
      imgEl.onerror = (e) => console.error("Failed to load SVG Image for curved text", e);
      imgEl.src = svgDataUrl;
    };

  // Open curved text modal in NEW or EDIT mode
  const openCurvedTextModal = (editGroup = null) => {
    if (editGroup && editGroup.__curvedMeta) {
      const m = editGroup.__curvedMeta;
      setCurvedTextValue(m.text);
      setCurvedTextRadius(m.radius);
      setCurvedTextFont(m.font);
      setCurvedTextSize(m.size);
      setCurvedTextColor(m.color);
      setCurvedTextStartAngle(m.startAngle);
      setEditingCurvedId(editGroup.__curvedTextId);
    } else {
      setEditingCurvedId(null);
    }
    setShowCurvedTextModal(true);
  };

  const deleteSelected = useCallback(() => {
    if (!fabricCanvas) return;
    const obj = fabricCanvas.getActiveObject();
    if (!obj) return;
    fabricCanvas.remove(obj);
    fabricCanvas.discardActiveObject();
    fabricCanvas.renderAll();
    setActiveObject(null);
  }, [fabricCanvas]);

  const duplicateSelected = async () => {
    if (!fabricCanvas) return;
    const obj = fabricCanvas.getActiveObject();
    if (!obj) return;
    const cloned = await obj.clone();
    cloned.set({ left: (obj.left || 0) + 24, top: (obj.top || 0) + 24 });
    fabricCanvas.add(cloned);
    fabricCanvas.setActiveObject(cloned);
    fabricCanvas.requestRenderAll();
  };

  // --------------------------------------------------------
  // PROPERTY SETTERS
  // --------------------------------------------------------
  const applyProp = (key, value) => {
    if (!fabricCanvas || !activeObject) return;
    activeObject.set(key, value);
    fabricCanvas.renderAll();
  };

  const handleFillChange = (val) => { setFillColor(val); applyProp('fill', val); };
  const handleStrokeChange = (val) => { setStrokeColor(val); applyProp('stroke', val); };
  const handleStrokeWidthChange = (val) => { const n = Number(val); setStrokeWidth(n); applyProp('strokeWidth', n); };
  const handleOpacityChange = (val) => { const n = Number(val); setOpacity(n); applyProp('opacity', n / 100); };

  // ── Font size with getBBox auto-fit (fixes overflow) ──
  const handleFontSizeChange = (val) => {
    const n = Number(val);
    setFontSize(n);
    if (!fabricCanvas || !activeObject) return;
    activeObject.set('fontSize', n);
    // Re-measure bounding box so the object's dimensions stay accurate
    if (activeObject.type === 'i-text' || activeObject.type === 'text') {
      activeObject.initDimensions?.();
    }
    fabricCanvas.renderAll();
  };

  // ── Font family with getBBox recalculation ──
  const handleFontFamilyChange = (val) => {
    setFontFamily(val);
    if (!fabricCanvas || !activeObject) return;
    activeObject.set('fontFamily', val);
    // After font change dimensions may differ — let Fabric recalc them
    if (activeObject.type === 'i-text' || activeObject.type === 'text') {
      activeObject.initDimensions?.();
      // nudge: setCoords re-syncs selection handles to new bounding box
      activeObject.setCoords();
    }
    fabricCanvas.renderAll();
  };

  const handleBoldToggle = () => { const next = !isBold; setIsBold(next); applyProp('fontWeight', next ? 'bold' : 'normal'); };
  const handleItalicToggle = () => { const next = !isItalic; setIsItalic(next); applyProp('fontStyle', next ? 'italic' : 'normal'); };
  const handleLineHeightChange = (val) => { const n = Number(val); setLineHeight(n); applyProp('lineHeight', n); };
  const handleTextAlignChange = (val) => { setTextAlign(val); applyProp('textAlign', val); };
  const handleCharSpacingChange = (val) => { const n = Number(val); setCharSpacing(n); applyProp('charSpacing', n); };

  const handleShadowChange = (val) => {
    const n = Number(val);
    setShadowBlur(n);
    if (!fabricCanvas || !activeObject) return;
    activeObject.set('shadow', n === 0 ? null : new fabric.Shadow({ color: 'rgba(0,0,0,0.4)', blur: n, offsetX: 4, offsetY: 4 }));
    fabricCanvas.renderAll();
  };

  const handleCornerRadiusChange = (val) => { const n = Number(val); setCornerRadius(n); applyProp('rx', n); applyProp('ry', n); };
  const handlePosXChange = (val) => { const n = Number(val); setPosX(n); applyProp('left', n); };
  const handlePosYChange = (val) => { const n = Number(val); setPosY(n); applyProp('top', n); };
  const handleAngleChange = (val) => { const n = Number(val); setAngle(n); applyProp('angle', n); };
  const handleSkewXChange = (val) => { const n = Number(val); setSkewX(n); applyProp('skewX', n); };
  const handleCanvasBg = (val) => { if (!fabricCanvas) return; fabricCanvas.backgroundColor = val; fabricCanvas.requestRenderAll(); };

  const applyGoldGradient = () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (!active) return;
    const grad = new fabric.Gradient({
      type: 'linear',
      coords: { x1: 0, y1: 0, x2: active.width, y2: active.height },
      colorStops: [
        { offset: 0, color: '#bf953f' }, { offset: 0.25, color: '#fcf6ba' },
        { offset: 0.5, color: '#b38728' }, { offset: 0.75, color: '#fbf5b7' },
        { offset: 1, color: '#aa771c' },
      ],
      gradientUnits: 'pixels'
    });
    active.set('fill', grad);
    fabricCanvas.renderAll();
    updateLayers();
  };

  const applySilverGradient = () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (!active) return;
    const grad = new fabric.Gradient({
      type: 'linear',
      coords: { x1: 0, y1: 0, x2: active.width, y2: active.height },
      colorStops: [
        { offset: 0, color: '#bdc3c7' }, { offset: 0.3, color: '#f8f8f8' },
        { offset: 0.6, color: '#95a5a6' }, { offset: 1, color: '#7f8c8d' },
      ],
      gradientUnits: 'pixels'
    });
    active.set('fill', grad);
    fabricCanvas.renderAll();
    updateLayers();
  };

  const applyPurpleGradient = () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (!active) return;
    const grad = new fabric.Gradient({
      type: 'linear',
      coords: { x1: 0, y1: 0, x2: active.width || 200, y2: active.height || 60 },
      colorStops: [
        { offset: 0, color: '#6366f1' }, { offset: 0.5, color: '#a855f7' }, { offset: 1, color: '#ec4899' },
      ],
      gradientUnits: 'pixels'
    });
    active.set('fill', grad);
    fabricCanvas.renderAll();
    updateLayers();
  };

  const toggleFlipX = () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (active) { active.set('flipX', !active.flipX); fabricCanvas.requestRenderAll(); }
  };

  const toggleFlipY = () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (active) { active.set('flipY', !active.flipY); fabricCanvas.requestRenderAll(); }
  };

  // ── Zoom ──
  const changeZoom = (delta) => {
    if (!fabricCanvas) return;
    const newZoom = Math.max(10, Math.min(400, zoom + delta));
    fabricCanvas.setZoom(newZoom / 100);
    setZoom(newZoom);
  };

  const resetZoom = () => {
    if (!fabricCanvas) return;
    fabricCanvas.setZoom(1);
    fabricCanvas.setViewportTransform([1, 0, 0, 1, 0, 0]);
    setZoom(100);
  };

  // --------------------------------------------------------
  // SAVE / LOAD / EXPORT
  // --------------------------------------------------------
  const buildProjectPayload = useCallback((nameOverride = '') => {
    if (!fabricCanvas) return null;
    return {
      id: currentProjectId || undefined,
      name: nameOverride || currentProjectName || `Iconora ${section}`,
      kind: section,
      canvas: fabricCanvas.toJSON(),
      assets: {
        fonts: [fontFamily],
      },
      editor: {
        section,
        canvas_size: canvasSize,
        background: fabricCanvas.backgroundColor || '#ffffff',
        zoom,
      },
      export_defaults: {
        format: section === 'icon' ? 'ico' : 'png',
        width: canvasSize.w,
        height: canvasSize.h,
        transparent: false,
      },
    };
  }, [canvasSize, currentProjectId, currentProjectName, fabricCanvas, fontFamily, section, zoom]);

  const applyLoadedProject = useCallback(async (project) => {
    if (!fabricCanvas) return;
    isApplyingProjectRef.current = true;
    try {
      const nextSection = ['logo', 'icon', 'signature'].includes(project.kind) ? project.kind : section;
      setSection(nextSection);

      const canvasData = project.canvas || {};
      const nextSize = project.editor?.canvas_size;
      if (nextSize?.w && nextSize?.h) {
        fabricCanvas.setDimensions({ width: nextSize.w, height: nextSize.h });
        setCanvasSize({ w: nextSize.w, h: nextSize.h });
      }

      await fabricCanvas.loadFromJSON(canvasData);
      fabricCanvas.backgroundColor = project.editor?.background || canvasData.backgroundColor || '#ffffff';

      const nextZoom = Math.max(10, Math.min(400, Number(project.editor?.zoom || 100)));
      fabricCanvas.setViewportTransform([1, 0, 0, 1, 0, 0]);
      fabricCanvas.setZoom(nextZoom / 100);
      setZoom(nextZoom);

      const loadedFont = project.assets?.fonts?.[0];
      if (loadedFont) {
        setFontFamily(loadedFont);
      }

      setActiveTool('select');
      setActiveObject(null);
      setLayerStates({});
      fabricCanvas.requestRenderAll();
      refreshLayers(fabricCanvas);
      saveSnapshot(fabricCanvas);
      setCurrentProjectId(project.id || '');
      setCurrentProjectName(project.name || '');
    } finally {
      isApplyingProjectRef.current = false;
    }
  }, [fabricCanvas, refreshLayers, saveSnapshot, section]);

  const saveProject = async (nameOverride = '') => {
    if (!fabricCanvas) return false;
    const proposedName = (nameOverride || currentProjectName || `Iconora ${section}`).trim();
    if (!proposedName) {
      showNotice('اسم المشروع', 'يرجى إدخال اسم صالح للمشروع.');
      return false;
    }
    try {
      const payload = buildProjectPayload(proposedName);
      const project = currentProjectId
        ? await updateProject(currentProjectId, payload)
        : await createProject(payload);
      setCurrentProjectId(project.id || '');
      setCurrentProjectName(project.name || proposedName);
      setShowSaveProjectModal(false);
      showNotice('تم الحفظ', `تم حفظ المشروع: ${project.name}`);
      return true;
    } catch (error) {
      showNotice('تعذر الحفظ', error.message);
      return false;
    }
  };

  const openSaveProjectModal = () => {
    setSaveProjectDraft(currentProjectName || `Iconora ${section}`);
    setShowSaveProjectModal(true);
  };

  const openSettingsModal = () => {
    setSettingsDraft({ ...DEFAULT_SETTINGS_DRAFT, ...(bootstrap.settings || {}) });
    setSettingsError('');
    setShowSettingsModal(true);
  };

  const persistSettings = async () => {
    setIsSavingSettings(true);
    setSettingsError('');
    try {
      const payload = await saveSettings(settingsDraft);
      setBootstrap(prev => ({
        ...prev,
        settings: { ...DEFAULT_SETTINGS_DRAFT, ...(prev.settings || {}), ...payload },
      }));
      setHealthInfo(prev => (
        prev
          ? { ...prev, ai_enabled: payload.ai_enabled !== false }
          : prev
      ));
      setShowSettingsModal(false);
      showNotice('تم حفظ الإعدادات', 'تم تحديث إعدادات التطبيق المحلية بنجاح.');
      return true;
    } catch (error) {
      const message = error.message || 'تعذر حفظ الإعدادات.';
      setSettingsError(message);
      return false;
    } finally {
      setIsSavingSettings(false);
    }
  };

  const loadProjectFromApi = async () => {
    if (!fabricCanvas) return;
    try {
      const result = await listProjects();
      const projects = result.projects || [];
      if (!projects.length) {
        showNotice('فتح مشروع', 'لا توجد مشاريع محفوظة حالياً.');
        return;
      }
      setAvailableProjects(projects);
      setSelectedProjectId(projects[0]?.id || '');
      setShowProjectsModal(true);
    } catch (error) {
      showNotice('تعذر الفتح', error.message);
    }
  };

  const confirmLoadProject = async () => {
    if (!selectedProjectId) {
      showNotice('فتح مشروع', 'يرجى اختيار مشروع أولاً.');
      return;
    }
    try {
      const project = await getProject(selectedProjectId);
      await applyLoadedProject(project);
      setShowProjectsModal(false);
      showNotice('تم الفتح', `تم فتح المشروع: ${project.name}`);
    } catch (error) {
      showNotice('تعذر الفتح', error.message);
    }
  };

  const exportProjectFile = async () => {
    if (!currentProjectId) {
      showNotice('تصدير المشروع', 'احفظ المشروع أولاً قبل تصديره كملف.');
      return;
    }
    try {
      const result = await exportProject(currentProjectId);
      const payload = result.document || result;
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${(currentProjectName || payload.name || 'iconora_project').replace(/[<>:\"/\\\\|?*]+/g, '_')}.iconora`;
      link.click();
      URL.revokeObjectURL(url);
      showNotice('تم التصدير', 'تم تصدير ملف المشروع بنجاح.');
    } catch (error) {
      showNotice('تعذر التصدير', error.message);
    }
  };

  const importProjectFile = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.iconora,.json,application/json';
    input.onchange = async (event) => {
      const file = event.target.files?.[0];
      if (!file) return;
      try {
        const text = await file.text();
        const documentData = JSON.parse(text);
        const imported = await importProjectApi(documentData, file.name.replace(/\.(iconora|json)$/i, ''));
        await applyLoadedProject(imported);
        showNotice('تم الاستيراد', `تم استيراد المشروع: ${imported.name}`);
      } catch (error) {
        showNotice('تعذر الاستيراد', error.message || 'فشل في قراءة ملف المشروع.');
      }
    };
    input.click();
  };

  const loadImage = () => {
    const input = document.createElement('input');
    input.type = 'file'; input.accept = 'image/*';
    input.onchange = (e) => {
      const file = e.target.files?.[0];
      if (!file || !fabricCanvas) return;
      const url = URL.createObjectURL(file);
      const imgEl = new window.Image();
      imgEl.src = url;
      imgEl.onload = () => {
        const fImg = new fabric.FabricImage(imgEl);
        if (fImg.width > fabricCanvas.width * 0.8) fImg.scaleToWidth(fabricCanvas.width * 0.8);
        fImg.set({ left: 40, top: 40 });
        fabricCanvas.add(fImg);
        fabricCanvas.setActiveObject(fImg);
        fabricCanvas.renderAll();
      };
    };
    input.click();
  };

  // ── Export PNG ──
  const exportSvg = async () => {
    if (!fabricCanvas) return;
    try {
      const result = await exportCanvasApi({
        format: 'svg',
        section,
        width: canvasSize.w,
        height: canvasSize.h,
        transparent: false,
        svg_text: fabricCanvas.toSVG(),
        filename: `iconora_${Date.now()}`,
      });
      showNotice('تم التصدير', result.output_path);
    } catch (error) {
      showNotice('تعذر التصدير', error.message);
    }
  };

  const capturePngDataUrl = async (multiplier = 2, transparent = false) => {
    if (!fabricCanvas) return null;
    const active = fabricCanvas.getActiveObject();
    if (active) {
      fabricCanvas.discardActiveObject();
      fabricCanvas.requestRenderAll();
    }

    const originalBg = fabricCanvas.backgroundColor;
    if (transparent) {
      fabricCanvas.backgroundColor = 'rgba(0,0,0,0)';
    }

    return new Promise((resolve) => {
      setTimeout(() => {
        const dataUrl = fabricCanvas.toDataURL({ format: 'png', multiplier });
        fabricCanvas.backgroundColor = originalBg;
        fabricCanvas.requestRenderAll();
        if (active) {
          fabricCanvas.setActiveObject(active);
          fabricCanvas.requestRenderAll();
        }
        resolve(dataUrl);
      }, 80);
    });
  };

  const exportPngViaApi = async (multiplier = 2, transparent = false) => {
    try {
      const dataUrl = await capturePngDataUrl(multiplier, transparent);
      if (!dataUrl) return;
      const qualityLabel = multiplier === 1 ? '1x' : multiplier === 2 ? '2x' : '4x';
      const result = await exportCanvasApi({
        format: 'png',
        section,
        width: canvasSize.w * multiplier,
        height: canvasSize.h * multiplier,
        transparent,
        data_url: dataUrl,
        filename: `iconora_${transparent ? 'transparent_' : ''}${qualityLabel}`,
      });
      showNotice('تم التصدير', result.output_path);
    } catch (error) {
      showNotice('تعذر التصدير', error.message);
    }
  };

  const exportIcoViaApi = async () => {
    if (!fabricCanvas) return;
    try {
      const multiplier = 256 / fabricCanvas.width;
      const dataUrl = await capturePngDataUrl(multiplier, true);
      if (!dataUrl) return;
      const result = await exportIconPack({
        width: 256,
        height: 256,
        data_url: dataUrl,
        filename: `iconora_favicon_${Date.now()}`,
      });
      showNotice('تم إنشاء حزمة الأيقونات', result.output_path);
    } catch (error) {
      showNotice('تعذر إنشاء ICO', error.message);
    }
  };

  // --------------------------------------------------------
  // TEMPLATES
  // --------------------------------------------------------
  const applyTemplate = (tpl) => {
    if (!fabricCanvas) return;
    historyRef.current.paused = true;
    fabricCanvas.clear();
    const solidBg = tpl.bg.startsWith('linear-gradient') || tpl.bg.startsWith('radial-gradient')
      ? '#0a0a0a' : tpl.bg;
    fabricCanvas.backgroundColor = solidBg;
    const defW = sectionConfig.defaultSize.w, defH = sectionConfig.defaultSize.h;
    const scaleX = fabricCanvas.width / defW, scaleY = fabricCanvas.height / defH;
    const scaleFont = Math.min(scaleX, scaleY);
    tpl.objects.forEach(o => {
      const base = { ...o };
      delete base.type;
      if (o.text !== undefined) delete base.text;
      const scaledProps = {
        ...base, left: (o.left || 100) * scaleX, top: (o.top || 100) * scaleY,
        ...(o.fontSize && { fontSize: o.fontSize * scaleFont }),
        ...(o.width && { width: o.width * scaleX }),
        ...(o.height && { height: o.height * scaleY }),
        ...(o.radius && { radius: o.radius * scaleFont }),
        ...(o.rx && { rx: o.rx * scaleFont, ry: o.rx * scaleFont }),
      };
      let obj;
      if (o.type === 'text') obj = new fabric.IText(o.text, scaledProps);
      else if (o.type === 'rect') obj = new fabric.Rect(scaledProps);
      else if (o.type === 'circle') obj = new fabric.Circle(scaledProps);
      if (obj) fabricCanvas.add(obj);
    });
    historyRef.current.paused = false;
    fabricCanvas.requestRenderAll();
    refreshLayers(fabricCanvas);
    saveSnapshot(fabricCanvas);
  };

  // --------------------------------------------------------
  // AI GENERATION
  // --------------------------------------------------------
  /* Phase 2A cleanup: retired legacy AI path.
    if (!aiPrompt.trim() || !fabricCanvas) return;
    setIsGenerating(true); setAiError('');
    try {
      const data = await generateLogo({ prompt: aiPrompt, remove_background: true });
      placeGeneratedImage(data.image_data);
    } catch {
      setAiError('تعذر توليد الشعار! ربما حدث خطأ في الخادم.');
    } finally { setIsGenerating(false); }
  };

  */
  const placeGeneratedImage = useCallback((imageDataUrl) => {
    if (!fabricCanvas || !imageDataUrl) return;
    const imgEl = new window.Image();
    imgEl.src = imageDataUrl;
    imgEl.onload = () => {
      const fImg = new fabric.FabricImage(imgEl);
      if (fImg.width > fabricCanvas.width * 0.5) fImg.scaleToWidth(fabricCanvas.width * 0.5);
      fImg.set({ left: (fabricCanvas.width - fImg.getScaledWidth()) / 2, top: (fabricCanvas.height - fImg.getScaledHeight()) / 2 });
      fabricCanvas.add(fImg);
      fabricCanvas.setActiveObject(fImg);
      fabricCanvas.renderAll();
      setAiPrompt('');
    };
  }, [fabricCanvas]);

  const handleGenerateLogoViaApi = async () => {
    if (!isAiEnabled || !aiPrompt.trim() || !fabricCanvas) return;
    setIsGenerating(true); setAiError('');
    try {
      const data = await generateLogo({ prompt: aiPrompt, remove_background: true });
      placeGeneratedImage(data.image_data);
    } catch {
      setAiError('طھط¹ط°ط± طھظˆظ„ظٹط¯ ط§ظ„ط´ط¹ط§ط±! ط±ط¨ظ…ط§ ط­ط¯ط« ط®ط·ط£ ظپظٹ ط§ظ„ط®ط§ط¯ظ….');
    } finally { setIsGenerating(false); }
  };

  // --------------------------------------------------------
  // LAYER ACTIONS
  // --------------------------------------------------------
  const selectLayer = (obj) => {
    if (!fabricCanvas || !obj) return;
    fabricCanvas.setActiveObject(obj);
    fabricCanvas.renderAll();
    setActiveObject(obj);
    syncPropsFromObject(obj);
  };

  const deleteLayer = (obj) => {
    if (!fabricCanvas || !obj) return;
    fabricCanvas.remove(obj);
    fabricCanvas.discardActiveObject();
    fabricCanvas.renderAll();
    setActiveObject(null);
  };

  const canUndo = historyRef.current.idx > 0;
  const canRedo = historyRef.current.idx < historyRef.current.stack.length - 1;
  const isText = activeObject?.type === 'i-text' || activeObject?.type === 'text';
  const isShape = activeObject?.type === 'rect';
  // A curved text group has the special metadata marker
  const isCurvedText = !!(activeObject?.__curvedTextId);

  // ============================================================
  // RENDER
  // ============================================================
  return (
    <div className="app-container" dir="rtl">

      {/* ====== TOPBAR ====== */}
      <header className="topbar">
        <div className="topbar-brand">
          <div className="logo-icon"><Sparkles size={16} color="white" /></div>
          <span className="brand-name">Iconora <span className="brand-accent">Studio</span></span>
          <span className="badge">v3.0</span>
        </div>

        {/* Section Nav */}
        <nav style={{ display: 'flex', gap: '4px', background: 'var(--bg-active)', borderRadius: '10px', padding: '3px' }}>
          {[
            { id: 'logo', icon: <LayoutTemplate size={14} />, label: 'لوجو' },
            { id: 'icon', icon: <Hexagon size={14} />, label: 'أيقونات' },
            { id: 'signature', icon: <PenLine size={14} />, label: 'توقيع' },
          ].map(tab => (
            <button key={tab.id} onClick={() => setSection(tab.id)} className={`section-tab ${section === tab.id ? 'active' : ''}`}>
              {tab.icon} {tab.label}
            </button>
          ))}
        </nav>

        {/* Center controls */}
        <div className="topbar-center" style={{ gap: '6px' }}>
          <button className="history-btn" onClick={undo} disabled={!canUndo} title="تراجع Ctrl+Z"><Undo2 size={15} /></button>
          <button className="history-btn" onClick={redo} disabled={!canRedo} title="إعادة Ctrl+Y"><Redo2 size={15} /></button>
          <div className="sep-v" />
          <button className="history-btn" onClick={() => changeZoom(-10)} title="تصغير"><ZoomOut size={15} /></button>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', minWidth: '36px', textAlign: 'center' }}>{zoom}%</span>
          <button className="history-btn" onClick={() => changeZoom(10)} title="تكبير"><ZoomIn size={15} /></button>
          <button className="history-btn" onClick={resetZoom} title="إعادة التعيين"><Maximize2 size={14} /></button>
          <div className="sep-v" />
          <select className="styled-select" style={{ width: 'auto', padding: '5px 8px', fontSize: '0.78rem' }}
            value={selectedCanvasLabel}
            onChange={(e) => {
              const s = sectionConfig.sizes.find(x => x.label === e.target.value);
              if (s && fabricCanvas) { fabricCanvas.setDimensions({ width: s.w, height: s.h }); fabricCanvas.requestRenderAll(); setCanvasSize({ w: s.w, h: s.h }); }
            }}>
            {sectionConfig.sizes.map(s => <option key={s.label}>{s.label}</option>)}
          </select>
          <label className="snap-toggle" title="المحاذاة التلقائية">
            <input type="checkbox" checked={snapEnabled} onChange={e => setSnapEnabled(e.target.checked)} />
            <span>مغناطيس</span>
          </label>
        </div>

        {/* Actions */}
        <div className="topbar-actions">
          <button className="btn btn-ghost btn-sm" onClick={openSettingsModal}><Settings2 size={14} /> إعدادات</button>
          <div className="sep-v" />
          <button className="btn btn-ghost btn-sm" onClick={openSaveProjectModal}><Save size={14} /> حفظ</button>
          <button className="btn btn-ghost btn-sm" onClick={loadProjectFromApi}><FolderOpen size={14} /> فتح</button>
          <button className="btn btn-ghost btn-sm" onClick={importProjectFile}><FolderOpen size={14} /> استيراد</button>
          <button className="btn btn-ghost btn-sm" onClick={exportProjectFile}><Download size={14} /> مشروع</button>
          <div className="sep-v" />
          {section === 'icon' && (
            <button className="btn btn-ghost btn-sm" style={{ color: '#fcd34d' }} onClick={exportIcoViaApi}><Download size={14} /> ICO</button>
          )}
          <button className="btn btn-ghost btn-sm" onClick={exportSvg}><Download size={14} /> SVG</button>
          <button className="btn btn-ghost btn-sm" onClick={() => exportPngViaApi(2, true)} title="تصدير بخلفية شفافة">
            <Download size={14} /> PNG شفاف
          </button>
          <div style={{ display: 'flex', borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--primary-dark)' }}>
            <button className="btn btn-primary btn-sm" style={{ borderRadius: 0, borderRight: '1px solid rgba(255,255,255,0.15)' }} onClick={() => exportPngViaApi(2)}><Download size={13} /> PNG</button>
            <button className="btn btn-primary btn-sm" style={{ borderRadius: 0, padding: '6px 7px', fontSize: '0.7rem' }} onClick={() => exportPngViaApi(1)}>1×</button>
            <button className="btn btn-primary btn-sm" style={{ borderRadius: 0, padding: '6px 7px', fontSize: '0.7rem' }} onClick={() => exportPngViaApi(4)}>4×</button>
          </div>
        </div>
      </header>

      {/* ====== WORKSPACE ====== */}
      <main className="workspace">

        {/* ====== LEFT SIDEBAR ====== */}
        <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
          {/* Sidebar tab bar */}
          <div className="sidebar-tabbar">
            {[
              { id: 'tools', icon: <Settings2 size={15} />, label: 'أدوات' },
              { id: 'templates', icon: <Star size={15} />, label: 'قوالب' },
              { id: 'icons', icon: <Sparkles size={15} />, label: 'مكتبة' },
              { id: 'ai', icon: <Wand2 size={15} />, label: 'ذكاء' },
              { id: 'layers', icon: <Layers size={15} />, label: 'طبقات' },
            ].map(t => (
              <button key={t.id} className={`sidebar-tab-btn ${sidebarTab === t.id ? 'active' : ''}`}
                onClick={() => setSidebarTab(t.id)} title={t.label}>
                {t.icon}
              </button>
            ))}
          </div>

          <div className="sidebar-content">
            {/* TOOLS TAB */}
            {sidebarTab === 'tools' && (
              <>
                <div className="sidebar-section">
                  <div className="section-label">🖱 وضع التحرير</div>
                  <div className="tool-grid">
                    <button className={`tool-btn ${activeTool === 'select' ? 'active' : ''}`} onClick={() => setActiveTool('select')}>
                      <MousePointer2 size={17} /> تحديد
                    </button>
                    {section === 'signature' && (
                      <button className={`tool-btn ${activeTool === 'draw' ? 'active' : ''}`} onClick={() => setActiveTool('draw')}>
                        <Pen size={17} /> فرشاة
                      </button>
                    )}
                  </div>
                </div>

                {/* Draw settings (signature mode only) */}
                {section === 'signature' && activeTool === 'draw' && (
                  <div className="sidebar-section">
                    <div className="section-label">🖊 إعدادات الريشة</div>
                    <div className="control-row">
                      <span className="control-label">اللون</span>
                      <div className="color-input-wrapper" style={{ width: 28, height: 28 }}>
                        <input type="color" value={drawColor} onChange={e => setDrawColor(e.target.value)} />
                      </div>
                    </div>
                    <div className="control-row">
                      <span className="control-label">السُمك</span>
                      <div className="range-row" style={{ flex: 1 }}>
                        <input type="range" className="range-slider" min="1" max="30" value={drawSize} onChange={e => setDrawSize(Number(e.target.value))} />
                        <span className="control-value">{drawSize}px</span>
                      </div>
                    </div>
                    {/* Quick color palette for drawing */}
                    <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap', marginTop: '6px' }}>
                      {['#0f1115', '#ffffff', '#6366f1', '#f59e0b', '#ec4899', '#22c55e', '#c9a227', '#ef4444'].map(c => (
                        <div key={c} onClick={() => setDrawColor(c)} style={{
                          width: 22, height: 22, borderRadius: 4, background: c, cursor: 'pointer',
                          border: drawColor === c ? '2px solid var(--primary)' : '1px solid var(--border-2)',
                          flexShrink: 0,
                        }} />
                      ))}
                    </div>
                    <button className="btn btn-ghost btn-sm" style={{ width: '100%', marginTop: '8px' }}
                      onClick={() => { if (fabricCanvas) { fabricCanvas.isDrawingMode = false; setTimeout(() => { if (fabricCanvas) fabricCanvas.isDrawingMode = activeTool === 'draw'; }, 10); } }}>
                      <RefreshCw size={13} /> مسح الريشة
                    </button>
                  </div>
                )}

                <div className="sidebar-section">
                  <div className="section-label">✦ إضافة عناصر</div>
                  <div className="tool-grid">
                    <button className="tool-btn" onClick={addText}><Type size={17} /> نص</button>
                    <button className="tool-btn" onClick={addRect}><Square size={17} /> مستطيل</button>
                    <button className="tool-btn" onClick={addCircle}><Circle size={17} /> دائرة</button>
                    <button className="tool-btn" onClick={addPolygon}><Hexagon size={17} /> مضلع</button>
                    <button className="tool-btn" onClick={addStar}><Star size={17} /> نجمة</button>
                    <button className="tool-btn" onClick={loadImage}><ImageIcon size={17} /> صورة</button>
                  </div>
                </div>

                {/* Curved Text */}
                <div className="sidebar-section">
                  <div className="section-label">🔄 نص مقوس</div>
                  <button className="btn btn-ghost btn-sm" style={{ width: '100%' }} onClick={() => openCurvedTextModal()}>
                    <AlignCenter size={14} /> إضافة نص على قوس
                  </button>
                  {isCurvedText && (
                    <button className="btn btn-primary btn-sm" style={{ width: '100%', marginTop: '6px' }} onClick={() => openCurvedTextModal(activeObject)}>
                      ✏ تعديل النص المقوس المحدد
                    </button>
                  )}
                </div>

                {/* Gradients */}
                <div className="sidebar-section">
                  <div className="section-label">🎨 تدرجات احترافية</div>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    <button className="gradient-btn" style={{ background: 'linear-gradient(135deg,#bf953f,#fcf6ba,#b38728)' }} onClick={applyGoldGradient} title="ذهبي">ذهبي</button>
                    <button className="gradient-btn" style={{ background: 'linear-gradient(135deg,#bdc3c7,#f8f8f8,#7f8c8d)' }} onClick={applySilverGradient} title="فضي">فضي</button>
                    <button className="gradient-btn" style={{ background: 'linear-gradient(135deg,#6366f1,#a855f7,#ec4899)' }} onClick={applyPurpleGradient} title="بنفسجي">إبداعي</button>
                  </div>
                </div>

                {/* Flip */}
                <div className="sidebar-section">
                  <div className="section-label">↔ انعكاس</div>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={toggleFlipX}><FlipHorizontal size={14} /> أفقي</button>
                    <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={toggleFlipY}><FlipVertical size={14} /> رأسي</button>
                  </div>
                </div>

                {/* SVG Filters */}
                <div className="sidebar-section">
                  <div className="section-label">✨ فلاتر SVG</div>
                  <button className="btn btn-ghost btn-sm" style={{ width: '100%' }} onClick={() => setShowFilterModal(true)}>
                    <Sliders size={14} /> إعدادات الفلاتر
                  </button>
                </div>
              </>
            )}

            {/* TEMPLATES TAB */}
            {sidebarTab === 'templates' && (
              <div className="sidebar-section">
                <div className="section-label"><Star size={12} /> قوالب جاهزة</div>
                <div className="templates-grid">
                  {sectionConfig.templates.map(tpl => (
                    <div key={tpl.id} className="template-card" onClick={() => applyTemplate(tpl)}>
                      <div className="template-preview">{tpl.emoji}</div>
                      {tpl.label}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* ICONS TAB */}
            {sidebarTab === 'icons' && (
              <>
                <div className="sidebar-section">
                  <div className="section-label"><Sparkles size={12} /> مكتبة أيقونات</div>
                  <div className="icons-grid">
                    {sectionConfig.icons.map(icon => (
                      <button key={icon.label} title={icon.label} onClick={() => addSvgIcon(icon)} className="icon-grid-btn">
                        {icon.emoji}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="sidebar-section">
                  <div className="section-label" style={{ color: '#fbbf24' }}>👑 زخارف فاخرة</div>
                  <div className="icons-grid">
                    {(bootstrap.ornaments || FALLBACK_BOOTSTRAP.ornaments).map(orn => (
                      <button key={orn.label} title={orn.label} onClick={() => addSvgIcon(orn)} className="icon-grid-btn ornament">
                        {orn.emoji}
                      </button>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* AI TAB */}
            {sidebarTab === 'ai' && (
              <div className="sidebar-section" style={{ flex: 1 }}>
                <div className="section-label"><Wand2 size={12} /> مولد الذكاء الاصطناعي</div>
                <div className="ai-panel">
                  <div className="ai-panel-header"><Sparkles size={15} /> توليد بالذكاء الاصطناعي</div>
                  <textarea className="ai-textarea" placeholder={sectionConfig.aiHint}
                    value={aiPrompt} onChange={e => setAiPrompt(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && e.ctrlKey && isAiEnabled) handleGenerateLogoViaApi(); }}
                    disabled={!isAiEnabled}
                  />
                  {!isAiEnabled && (
                    <div className="ai-error"><TriangleAlert size={13} /> الذكاء الاصطناعي معطل حالياً من الإعدادات.</div>
                  )}
                  {aiError && (
                    <div className="ai-error"><TriangleAlert size={13} /> {aiError}</div>
                  )}
                  <button className={`btn btn-primary btn-full ${isGenerating ? 'generating-indicator' : ''}`}
                    onClick={handleGenerateLogoViaApi} disabled={!isAiEnabled || isGenerating || !aiPrompt.trim()}>
                    {isGenerating ? <><Loader2 size={15} className="animate-spin" /> جاري التوليد...</> : <><Wand2 size={15} /> توليد ودمج</>}
                  </button>
                    <p className="ai-note">
                      Ctrl+Enter للتوليد السريع
                      <br />
                      <span style={{ color: 'var(--text-faint)' }}>
                        {bootstrapError
                          ? 'وضع fallback للأصول مفعل'
                          : healthError
                            ? 'تعذر التحقق من صحة backend'
                            : healthInfo?.status === 'ok'
                              ? `متصل بواجهة API المحلية${healthInfo.version ? ` • v${healthInfo.version}` : ''}`
                              : 'متصل بواجهة API المحلية'}
                      </span>
                    </p>
                </div>
              </div>
            )}

            {/* LAYERS TAB */}
            {sidebarTab === 'layers' && (
              <div className="sidebar-section">
                <div className="section-label" style={{ justifyContent: 'space-between' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Layers size={12} /> الطبقات ({layers.length})</span>
                </div>
                {layers.length === 0 ? (
                  <div className="empty-layers">لا توجد عناصر بعد</div>
                ) : (
                  <div className="layers-list">
                    {layers.map((l, i) => {
                      const id = l.obj.__uid;
                      const ls = layerStates[id] || { visible: true, locked: false };
                      return (
                        <div key={i} className={`layer-item ${activeObject === l.obj ? 'active' : ''}`} onClick={() => !ls.locked && selectLayer(l.obj)}>
                          <button className="layer-action-btn" onClick={e => { e.stopPropagation(); toggleLayerVisibility(l.obj); }} title={ls.visible ? 'إخفاء' : 'إظهار'}>
                            {ls.visible ? <Eye size={12} /> : <EyeOff size={12} />}
                          </button>
                          <button className="layer-action-btn" onClick={e => { e.stopPropagation(); toggleLayerLock(l.obj); }} title={ls.locked ? 'فتح' : 'قفل'}>
                            {ls.locked ? <Lock size={12} /> : <Unlock size={12} />}
                          </button>
                          <span className="layer-name">{l.label}</span>
                          <button className="layer-delete" onClick={e => { e.stopPropagation(); deleteLayer(l.obj); }}><X size={12} /></button>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        </aside>

        {/* ====== CANVAS ====== */}
        <div className="canvas-container-outer">
          <div className="canvas-wrapper fade-in" style={{ position: 'relative' }}>
            <canvas ref={canvasRef} id="main-canvas" />
            {/* Snap lines overlay */}
            <svg className="snap-lines-overlay" style={{
              position: 'absolute', inset: 0, pointerEvents: 'none',
              width: canvasSize.w, height: canvasSize.h,
            }}>
              {snapLinesRef.current.h.map((y, i) => (
                <line key={`h-${i}`} x1="0" y1={y} x2={canvasSize.w} y2={y} stroke="#6366f1" strokeWidth="1" strokeDasharray="4 4" opacity="0.7" />
              ))}
              {snapLinesRef.current.v.map((x, i) => (
                <line key={`v-${i}`} x1={x} y1="0" x2={x} y2={canvasSize.h} stroke="#6366f1" strokeWidth="1" strokeDasharray="4 4" opacity="0.7" />
              ))}
            </svg>
          </div>

          {/* Zoom info */}
          <div className="canvas-zoom-info">
            <span>{canvasSize.w} × {canvasSize.h} px</span>
            <span>•</span>
            <span>{zoom}%</span>
            {activeTool !== 'select' && <span style={{ color: 'var(--warning)' }}>• {activeTool === 'draw' ? '✏ رسم حر' : activeTool}</span>}
            {activeObject && <><span>•</span><span style={{ color: 'var(--primary-light)' }}>{getLayerLabel(activeObject)}</span></>}
          </div>
        </div>

        {/* ====== RIGHT PANEL ====== */}
        <aside className="control-panel">
          {activeObject ? (
            <div className="fade-in">
              {/* Tabs — Global Inspector */}
              <div className="prop-tabs">
                <button className={`prop-tab ${activePropTab === 'style' ? 'active' : ''}`} onClick={() => setActivePropTab('style')}>
                  <Palette size={12} style={{ display: 'inline', marginLeft: '3px' }} /> المظهر
                </button>
                {isText && (
                  <button className={`prop-tab ${activePropTab === 'text' ? 'active' : ''}`} onClick={() => setActivePropTab('text')}>
                    <Type size={12} style={{ display: 'inline', marginLeft: '3px' }} /> النص
                  </button>
                )}
                {isCurvedText && (
                  <button className={`prop-tab ${activePropTab === 'curved' ? 'active' : ''}`} onClick={() => setActivePropTab('curved')}>
                    🔄 القوس
                  </button>
                )}
                <button className={`prop-tab ${activePropTab === 'position' ? 'active' : ''}`} onClick={() => setActivePropTab('position')}>
                  <Move size={12} style={{ display: 'inline', marginLeft: '3px' }} /> موضع
                </button>
              </div>

              {/* === STYLE TAB === */}
              {activePropTab === 'style' && (
                <div className="panel-section">
                  {activeObject.type !== 'image' && (
                    <>
                      <div className="panel-title">اللون الداخلي</div>
                      <div className="control-row">
                        <div className="color-swatch-row" style={{ width: '100%' }}>
                          <div className="color-input-wrapper"><input type="color" value={fillColor} onChange={e => handleFillChange(e.target.value)} /></div>
                          <input className="color-hex" value={fillColor} onChange={e => handleFillChange(e.target.value)} maxLength={7} />
                        </div>
                      </div>
                      {/* Quick colors */}
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '8px' }}>
                        {['#ffffff','#0f1115','#f8fafc','#1e293b','#334155','#6366f1','#818cf8','#a855f7','#ec4899','#ef4444','#f59e0b','#22c55e','#14b8a6','#0ea5e9','#c9a227','#2d1b0e','#0d0d1f','#080808','#0a1628','#f0fdf4'].map(c => (
                          <div key={c} onClick={() => handleFillChange(c)} title={c} className="color-swatch" style={{ background: c, border: fillColor === c ? '2px solid var(--primary)' : '1px solid var(--border-2)' }} />
                        ))}
                      </div>

                      <div className="sep" />

                      <div className="panel-title">الحدود (Stroke)</div>
                      <div className="color-swatch-row" style={{ marginBottom: '8px' }}>
                        <div className="color-input-wrapper"><input type="color" value={strokeColor} onChange={e => handleStrokeChange(e.target.value)} /></div>
                        <input className="color-hex" value={strokeColor} onChange={e => handleStrokeChange(e.target.value)} maxLength={7} />
                      </div>
                      <div className="control-row">
                        <span className="control-label">سُمك الحد</span>
                        <div className="range-row" style={{ flex: 1 }}>
                          <input type="range" className="range-slider" min="0" max="20" value={strokeWidth} onChange={e => handleStrokeWidthChange(e.target.value)} />
                          <span className="control-value">{strokeWidth}px</span>
                        </div>
                      </div>
                      <div className="sep" />
                    </>
                  )}

                  <div className="panel-title">الشفافية</div>
                  <div className="control-row">
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="0" max="100" value={opacity} onChange={e => handleOpacityChange(e.target.value)} />
                      <span className="control-value">{opacity}%</span>
                    </div>
                  </div>
                  <div className="sep" />

                  <div className="panel-title">الظل</div>
                  <div className="control-row">
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="0" max="40" value={shadowBlur} onChange={e => handleShadowChange(e.target.value)} />
                      <span className="control-value">{shadowBlur}px</span>
                    </div>
                  </div>

                  {isShape && (
                    <>
                      <div className="sep" />
                      <div className="panel-title">انحناء الزوايا</div>
                      <div className="control-row">
                        <div className="range-row" style={{ flex: 1 }}>
                          <input type="range" className="range-slider" min="0" max="100" value={cornerRadius} onChange={e => handleCornerRadiusChange(e.target.value)} />
                          <span className="control-value">{cornerRadius}px</span>
                        </div>
                      </div>
                    </>
                  )}
                  <div className="sep" />
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={duplicateSelected}><Copy size={13} /> تكرار</button>
                    <button className="btn btn-danger btn-sm" onClick={deleteSelected}><Trash2 size={13} /></button>
                  </div>
                </div>
              )}

              {/* === TEXT TAB === */}
              {activePropTab === 'text' && isText && (
                <div className="panel-section">
                  <div className="panel-title">الخط</div>
                  <select className="styled-select" value={fontFamily} onChange={e => handleFontFamilyChange(e.target.value)} style={{ marginBottom: '10px' }}>
                    {sectionConfig.fonts.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
                  </select>

                  <div className="panel-title">حجم الخط</div>
                  <div className="control-row" style={{ marginBottom: '10px' }}>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="8" max="300" value={fontSize} onChange={e => handleFontSizeChange(e.target.value)} />
                      <span className="control-value">{fontSize}px</span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '6px', marginBottom: '10px' }}>
                    <button className={`btn btn-ghost btn-sm ${isBold ? 'prop-active' : ''}`} onClick={handleBoldToggle}><Bold size={13} /></button>
                    <button className={`btn btn-ghost btn-sm ${isItalic ? 'prop-active' : ''}`} onClick={handleItalicToggle}><Italic size={13} /></button>
                    {['left','center','right'].map(a => (
                      <button key={a} className={`btn btn-ghost btn-sm ${textAlign === a ? 'prop-active' : ''}`} onClick={() => handleTextAlignChange(a)}>
                        {a === 'left' ? <AlignLeft size={13} /> : a === 'center' ? <AlignCenter size={13} /> : <AlignRight size={13} />}
                      </button>
                    ))}
                  </div>

                  <div className="sep" />
                  <div className="panel-title">تباعد الأحرف</div>
                  <div className="control-row">
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="-200" max="600" value={charSpacing} onChange={e => handleCharSpacingChange(e.target.value)} />
                      <span className="control-value">{charSpacing}</span>
                    </div>
                  </div>

                  <div className="sep" />
                  <div className="panel-title">ارتفاع السطر</div>
                  <div className="control-row">
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="0.8" max="3" step="0.05" value={lineHeight} onChange={e => handleLineHeightChange(e.target.value)} />
                      <span className="control-value">{lineHeight.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* === CURVED TEXT INSPECTOR TAB === */}
              {activePropTab === 'curved' && isCurvedText && (
                <div className="panel-section">
                  <div className="panel-title">🔄 خصائص النص المقوس</div>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '12px', lineHeight: 1.5 }}>
                    عدّل الإعدادات ثم اضغط «تطبيق» لتحديث العنصر في مكانه دون إضافة نسخة جديدة.
                  </p>
                  <div className="modal-field" style={{ marginBottom: '10px' }}>
                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>النص</label>
                    <input className="modal-input" value={curvedTextValue}
                      onChange={e => setCurvedTextValue(e.target.value)} />
                  </div>
                  <div className="modal-field" style={{ marginBottom: '10px' }}>
                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>الخط</label>
                    <select className="styled-select" value={curvedTextFont} onChange={e => setCurvedTextFont(e.target.value)}>
                      {sectionConfig.fonts.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
                    </select>
                  </div>
                  <div className="modal-field" style={{ marginBottom: '10px' }}>
                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>حجم الحرف: {curvedTextSize}px</label>
                    <input type="range" className="range-slider" min="10" max="120" value={curvedTextSize}
                      onChange={e => setCurvedTextSize(Number(e.target.value))} />
                  </div>
                  <div className="modal-field" style={{ marginBottom: '10px' }}>
                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>نصف القطر: {curvedTextRadius}px</label>
                    <input type="range" className="range-slider" min="60" max="400" value={curvedTextRadius}
                      onChange={e => setCurvedTextRadius(Number(e.target.value))} />
                  </div>
                  <div className="modal-field" style={{ marginBottom: '10px' }}>
                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>زاوية البدء: {curvedTextStartAngle}°</label>
                    <input type="range" className="range-slider" min="0" max="360" value={curvedTextStartAngle}
                      onChange={e => setCurvedTextStartAngle(Number(e.target.value))} />
                  </div>
                  <div className="modal-field" style={{ marginBottom: '14px' }}>
                    <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>اللون</label>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                      <div className="color-input-wrapper"><input type="color" value={curvedTextColor} onChange={e => setCurvedTextColor(e.target.value)} /></div>
                      <input className="color-hex" value={curvedTextColor} onChange={e => setCurvedTextColor(e.target.value)} maxLength={7} />
                    </div>
                  </div>
                  {/* inline live preview */}
                  <div style={{ background: 'var(--bg-active)', borderRadius: '8px', padding: '8px', textAlign: 'center', marginBottom: '12px', minHeight: '120px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {curvedTextValue ? (
                      <svg width="100%" height="110" viewBox="0 0 400 400" overflow="visible">
                        <defs>
                          <path id="panel-prev-arc" d={(() => {
                            const r = curvedTextRadius;
                            const a1 = (curvedTextStartAngle * Math.PI) / 180;
                            const isBottom = curvedTextStartAngle > 0 && curvedTextStartAngle < 180;
                            const sweep = isBottom ? 0 : 1;
                            const a2 = a1 + (179 * Math.PI / 180);
                            return `M ${200 + r * Math.cos(a1)} ${200 + r * Math.sin(a1)} A ${r} ${r} 0 0 ${sweep} ${200 + r * Math.cos(a2)} ${200 + r * Math.sin(a2)}`;
                          })()} />
                        </defs>
                        <text fontFamily={curvedTextFont} fontSize={curvedTextSize} fill={curvedTextColor} textAnchor="middle" direction="rtl">
                          <textPath href="#panel-prev-arc" startOffset="50%">{curvedTextValue}</textPath>
                        </text>
                      </svg>
                    ) : (
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>أدخل النص</span>
                    )}
                  </div>
                  <button
                    className="btn btn-primary"
                    style={{ width: '100%' }}
                    onClick={() => commitCurvedText(activeObject.__curvedTextId)}
                  >
                    ✦ تطبيق التعديلات
                  </button>
                </div>
              )}

              {/* === POSITION TAB === */}
              {activePropTab === 'position' && (
                <div className="panel-section">
                  <div className="panel-title">الموضع</div>
                  <div className="control-row">
                    <span className="control-label">المحور X</span>
                    <input type="number" className="num-input" value={posX} onChange={e => handlePosXChange(e.target.value)} />
                  </div>
                  <div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">المحور Y</span>
                    <input type="number" className="num-input" value={posY} onChange={e => handlePosYChange(e.target.value)} />
                  </div>

                  <div className="sep" />
                  <div className="panel-title">الزوايا والميول</div>
                  <div className="control-row">
                    <span className="control-label">دوران</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="-180" max="180" value={angle} onChange={e => handleAngleChange(e.target.value)} />
                      <span className="control-value" style={{ minWidth: '35px' }}>{angle}°</span>
                    </div>
                  </div>
                  <div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">ميلان</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="-89" max="89" value={skewX} onChange={e => handleSkewXChange(e.target.value)} />
                      <span className="control-value" style={{ minWidth: '35px' }}>{skewX}°</span>
                    </div>
                  </div>

                  <div className="sep" />
                  <div className="panel-title">محاذاة</div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                    {[
                      { label: 'توسيط أفقي', action: () => { if (!fabricCanvas || !activeObject) return; activeObject.set('left', (fabricCanvas.width - activeObject.getScaledWidth()) / 2); fabricCanvas.renderAll(); } },
                      { label: 'توسيط رأسي', action: () => { if (!fabricCanvas || !activeObject) return; activeObject.set('top', (fabricCanvas.height - activeObject.getScaledHeight()) / 2); fabricCanvas.renderAll(); } },
                      { label: 'محاذاة يسار', action: () => { if (!fabricCanvas || !activeObject) return; activeObject.set('left', 0); fabricCanvas.renderAll(); } },
                      { label: 'محاذاة أعلى', action: () => { if (!fabricCanvas || !activeObject) return; activeObject.set('top', 0); fabricCanvas.renderAll(); } },
                    ].map(a => (
                      <button key={a.label} className="btn btn-ghost btn-sm" onClick={a.action} style={{ fontSize: '0.72rem' }}>{a.label}</button>
                    ))}
                  </div>

                  <div className="sep" />
                  <div className="panel-title">ترتيب الطبقات</div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                    {[
                      { label: '⬆ للأمام', action: () => { fabricCanvas?.bringObjectForward(activeObject); refreshLayers(fabricCanvas); } },
                      { label: '⬇ للخلف', action: () => { fabricCanvas?.sendObjectBackwards(activeObject); refreshLayers(fabricCanvas); } },
                      { label: '⤒ للأعلى', action: () => { fabricCanvas?.bringObjectToFront(activeObject); refreshLayers(fabricCanvas); } },
                      { label: '⤓ للأسفل', action: () => { fabricCanvas?.sendObjectToBack(activeObject); refreshLayers(fabricCanvas); } },
                    ].map(a => (
                      <button key={a.label} className="btn btn-ghost btn-sm" onClick={a.action} style={{ fontSize: '0.72rem' }}>{a.label}</button>
                    ))}
                  </div>
                </div>
              )}

              {/* Canvas background */}
              <div className="panel-section">
                <div className="panel-title">خلفية اللوحة</div>
                <div className="color-swatch-row">
                  <div className="color-input-wrapper"><input type="color" defaultValue="#ffffff" onChange={e => handleCanvasBg(e.target.value)} /></div>
                  <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                    {['#ffffff', '#0f1115', '#f8fafc', '#1e1b4b', '#0c4a6e', '#1a0a04', '#0a0804', 'transparent'].map(c => (
                      <div key={c} onClick={() => handleCanvasBg(c === 'transparent' ? 'rgba(0,0,0,0)' : c)}
                        style={{ width: 22, height: 22, borderRadius: 4, background: c === 'transparent' ? 'repeating-conic-gradient(#aaa 0% 25%, #fff 0% 50%) 0 0 / 8px 8px' : c, cursor: 'pointer', border: '1px solid var(--border-2)', flexShrink: 0 }}
                        title={c === 'transparent' ? 'شفاف' : c}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <>
              <div className="empty-panel">
                <MousePointer2 size={32} />
                <div>
                  <div style={{ fontWeight: 600, marginBottom: '4px', color: 'var(--text-secondary)' }}>لا يوجد عنصر محدد</div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>اضغط على أي عنصر في اللوحة لعرض خصائصه</div>
                </div>
              </div>
              <div className="panel-section">
                <div className="panel-title">خلفية اللوحة</div>
                <div className="color-swatch-row">
                  <div className="color-input-wrapper"><input type="color" defaultValue="#ffffff" onChange={e => handleCanvasBg(e.target.value)} /></div>
                  <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                    {['#ffffff', '#0f1115', '#f8fafc', '#1e1b4b', '#0c4a6e', '#1a0a04', '#0a0804'].map(c => (
                      <div key={c} onClick={() => handleCanvasBg(c)} style={{ width: 22, height: 22, borderRadius: 4, background: c, cursor: 'pointer', border: '1px solid var(--border-2)', flexShrink: 0 }} />
                    ))}
                  </div>
                </div>
              </div>
            </>
          )}
        </aside>
      </main>

      <SettingsModal
        open={showSettingsModal}
        onClose={() => setShowSettingsModal(false)}
        settingsDraft={settingsDraft}
        setSettingsDraft={setSettingsDraft}
        healthInfo={healthInfo}
        settingsError={settingsError}
        isSavingSettings={isSavingSettings}
        onSave={persistSettings}
      />

      <SaveProjectModal
        open={showSaveProjectModal}
        onClose={() => setShowSaveProjectModal(false)}
        value={saveProjectDraft}
        onChange={setSaveProjectDraft}
        onSave={() => saveProject(saveProjectDraft)}
      />

      <OpenProjectModal
        open={showProjectsModal}
        onClose={() => setShowProjectsModal(false)}
        projects={availableProjects}
        selectedProjectId={selectedProjectId}
        onSelect={setSelectedProjectId}
        onOpen={confirmLoadProject}
      />

      <NoticeModal
        open={noticeModal.open}
        title={noticeModal.title}
        message={noticeModal.message}
        onClose={() => setNoticeModal({ open: false, title: '', message: '' })}
      />

      {false && showSettingsModal && (
        <div className="modal-overlay" onClick={() => setShowSettingsModal(false)}>
          <div className="modal-box" onClick={e => e.stopPropagation()} style={{ maxWidth: '560px' }}>
            <div className="modal-header">
              <span>إعدادات التطبيق</span>
              <button className="modal-close" onClick={() => setShowSettingsModal(false)}><X size={16} /></button>
            </div>
            <div className="modal-body">
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="modal-field">
                  <label>Theme</label>
                  <select
                    className="styled-select"
                    value={settingsDraft.theme}
                    onChange={e => setSettingsDraft(prev => ({ ...prev, theme: e.target.value }))}
                  >
                    <option value="dark">Dark</option>
                    <option value="light">Light</option>
                  </select>
                </div>
                <div className="modal-field">
                  <label>Language</label>
                  <select
                    className="styled-select"
                    value={settingsDraft.language}
                    onChange={e => setSettingsDraft(prev => ({ ...prev, language: e.target.value }))}
                  >
                    <option value="ar">Arabic</option>
                    <option value="en">English</option>
                  </select>
                </div>
              </div>
              <div className="modal-field">
                <label>AI Model</label>
                <input
                  className="modal-input"
                  value={settingsDraft.ai_model}
                  onChange={e => setSettingsDraft(prev => ({ ...prev, ai_model: e.target.value }))}
                />
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="modal-field">
                  <label>AI Endpoint</label>
                  <input
                    className="modal-input"
                    value={settingsDraft.ai_endpoint}
                    onChange={e => setSettingsDraft(prev => ({ ...prev, ai_endpoint: e.target.value }))}
                  />
                </div>
                <div className="modal-field">
                  <label>AI Timeout (sec)</label>
                  <input
                    className="modal-input"
                    type="number"
                    min="1"
                    max="300"
                    value={settingsDraft.ai_timeout}
                    onChange={e => setSettingsDraft(prev => ({ ...prev, ai_timeout: Number(e.target.value) || 30 }))}
                  />
                </div>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="modal-field">
                  <label>Default Quality</label>
                  <input
                    className="modal-input"
                    type="number"
                    min="1"
                    max="100"
                    value={settingsDraft.default_quality}
                    onChange={e => setSettingsDraft(prev => ({ ...prev, default_quality: Number(e.target.value) || 95 }))}
                  />
                </div>
                <div className="modal-field">
                  <label>Current Runtime</label>
                  <div style={{
                    minHeight: '38px',
                    borderRadius: '8px',
                    border: '1px solid var(--border-2)',
                    background: 'var(--bg-active)',
                    color: 'var(--text-secondary)',
                    display: 'flex',
                    alignItems: 'center',
                    padding: '0 12px',
                    fontSize: '0.85rem',
                  }}>
                    {healthInfo?.status === 'ok'
                      ? `Backend جاهز${healthInfo.version ? ` • v${healthInfo.version}` : ''}`
                      : 'Backend status unavailable'}
                  </div>
                </div>
              </div>
              <label className="snap-toggle" style={{ justifyContent: 'space-between' }}>
                <input
                  type="checkbox"
                  checked={settingsDraft.ai_enabled}
                  onChange={e => setSettingsDraft(prev => ({ ...prev, ai_enabled: e.target.checked }))}
                />
                <span>تفعيل الذكاء الاصطناعي</span>
              </label>
              <label className="snap-toggle" style={{ justifyContent: 'space-between' }}>
                <input
                  type="checkbox"
                  checked={settingsDraft.auto_open_folder}
                  onChange={e => setSettingsDraft(prev => ({ ...prev, auto_open_folder: e.target.checked }))}
                />
                <span>فتح مجلد التصدير تلقائياً</span>
              </label>
              {settingsError && (
                <div className="ai-error"><TriangleAlert size={13} /> {settingsError}</div>
              )}
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost btn-sm" onClick={() => setShowSettingsModal(false)}>إلغاء</button>
              <button className="btn btn-primary btn-sm" onClick={persistSettings} disabled={isSavingSettings}>
                {isSavingSettings ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
              </button>
            </div>
          </div>
        </div>
      )}

      {false && showSaveProjectModal && (
        <div className="modal-overlay" onClick={() => setShowSaveProjectModal(false)}>
          <div className="modal-box" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <span>حفظ المشروع</span>
              <button className="modal-close" onClick={() => setShowSaveProjectModal(false)}><X size={16} /></button>
            </div>
            <div className="modal-body">
              <div className="modal-field">
                <label>اسم المشروع</label>
                <input
                  className="modal-input"
                  value={saveProjectDraft}
                  onChange={e => setSaveProjectDraft(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter') saveProject(saveProjectDraft); }}
                  autoFocus
                />
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost btn-sm" onClick={() => setShowSaveProjectModal(false)}>إلغاء</button>
              <button className="btn btn-primary btn-sm" onClick={() => saveProject(saveProjectDraft)}>حفظ</button>
            </div>
          </div>
        </div>
      )}

      {false && showProjectsModal && (
        <div className="modal-overlay" onClick={() => setShowProjectsModal(false)}>
          <div className="modal-box" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <span>فتح مشروع</span>
              <button className="modal-close" onClick={() => setShowProjectsModal(false)}><X size={16} /></button>
            </div>
            <div className="modal-body">
              <div className="modal-field">
                <label>المشاريع المتاحة</label>
                <select
                  className="styled-select"
                  value={selectedProjectId}
                  onChange={e => setSelectedProjectId(e.target.value)}
                >
                  {availableProjects.map(project => (
                    <option key={project.id} value={project.id}>
                      {project.name} ({project.kind})
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost btn-sm" onClick={() => setShowProjectsModal(false)}>إلغاء</button>
              <button className="btn btn-primary btn-sm" onClick={confirmLoadProject}>فتح</button>
            </div>
          </div>
        </div>
      )}

      {false && noticeModal.open && (
        <div className="modal-overlay" onClick={() => setNoticeModal({ open: false, title: '', message: '' })}>
          <div className="modal-box" onClick={e => e.stopPropagation()} style={{ maxWidth: '520px' }}>
            <div className="modal-header">
              <span>{noticeModal.title}</span>
              <button className="modal-close" onClick={() => setNoticeModal({ open: false, title: '', message: '' })}><X size={16} /></button>
            </div>
            <div className="modal-body">
              <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.7, color: 'var(--text-secondary)' }}>
                {noticeModal.message}
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-primary btn-sm" onClick={() => setNoticeModal({ open: false, title: '', message: '' })}>موافق</button>
            </div>
          </div>
        </div>
      )}

      {/* ====== CURVED TEXT MODAL ====== */}
      {showCurvedTextModal && (
        <div
          style={{
            position: 'fixed', inset: 0,
            background: 'rgba(0,0,0,0.65)',
            backdropFilter: 'blur(6px)',
            zIndex: 9999,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
          onClick={() => { setShowCurvedTextModal(false); setEditingCurvedId(null); }}
        >
          <div className="modal-box" onClick={e => e.stopPropagation()} style={{ maxHeight: '90vh', overflowY: 'auto' }}>
            <div className="modal-header">
              <span>{editingCurvedId ? '✏ تعديل النص المقوس' : '🔄 نص مقوس على قوس'}</span>
              <button className="modal-close" onClick={() => { setShowCurvedTextModal(false); setEditingCurvedId(null); }}><X size={16} /></button>
            </div>
            <div className="modal-body">
              <div className="modal-field">
                <label>النص</label>
                <input className="modal-input" value={curvedTextValue}
                  onChange={e => setCurvedTextValue(e.target.value)}
                  placeholder="اكتب النص هنا..."
                  autoFocus />
              </div>
              <div className="modal-field">
                <label>الخط</label>
                <select className="styled-select" value={curvedTextFont} onChange={e => setCurvedTextFont(e.target.value)}>
                  {sectionConfig.fonts.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
                </select>
              </div>
              <div className="modal-field">
                <label>حجم الحرف: {curvedTextSize}px</label>
                <input type="range" className="range-slider" min="12" max="120" value={curvedTextSize}
                  onChange={e => setCurvedTextSize(Number(e.target.value))} />
              </div>
              <div className="modal-field">
                <label>نصف القطر: {curvedTextRadius}px</label>
                <input type="range" className="range-slider" min="60" max="400" value={curvedTextRadius}
                  onChange={e => setCurvedTextRadius(Number(e.target.value))} />
              </div>
              <div className="modal-field">
                <label>زاوية البدء: {curvedTextStartAngle}°</label>
                <input type="range" className="range-slider" min="0" max="360" value={curvedTextStartAngle}
                  onChange={e => setCurvedTextStartAngle(Number(e.target.value))} />
              </div>
              <div className="modal-field">
                <label>اللون</label>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <div className="color-input-wrapper"><input type="color" value={curvedTextColor} onChange={e => setCurvedTextColor(e.target.value)} /></div>
                  <input className="color-hex" value={curvedTextColor} onChange={e => setCurvedTextColor(e.target.value)} maxLength={7} />
                </div>
              </div>

              {/* ── Live SVG Preview ── */}
              <div style={{ background: 'var(--bg-active)', borderRadius: '8px', padding: '12px', textAlign: 'center', minHeight: '120px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {curvedTextValue ? (
                  <svg
                    width="100%" height="150"
                    viewBox="-150 -150 300 300"
                    overflow="visible"
                    style={{ maxWidth: '100%' }}
                  >
                    <defs>
                      <path
                        id="modal-prev-arc"
                        d={(() => {
                          const r = curvedTextRadius;
                          const a1 = (curvedTextStartAngle * Math.PI) / 180;
                          const isBottom = curvedTextStartAngle > 0 && curvedTextStartAngle < 180;
                          const sweep = isBottom ? 0 : 1;
                          const a2 = a1 + (179 * Math.PI / 180);
                          return `M ${r * Math.cos(a1)} ${r * Math.sin(a1)} A ${r} ${r} 0 0 ${sweep} ${r * Math.cos(a2)} ${r * Math.sin(a2)}`;
                        })()}
                      />
                    </defs>
                    <circle cx="0" cy="0" r={curvedTextRadius} fill="none" stroke="rgba(99,102,241,0.15)" strokeWidth="1" strokeDasharray="4 3" />
                    <text
                      fontFamily={curvedTextFont}
                      fontSize={curvedTextSize}
                      fill={curvedTextColor}
                      textAnchor="middle"
                      direction="rtl"
                    >
                      <textPath href="#modal-prev-arc" startOffset="50%">{curvedTextValue}</textPath>
                    </text>
                  </svg>
                ) : (
                  <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>أدخل النص للمعاينة</span>
                )}
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost btn-sm" onClick={() => { setShowCurvedTextModal(false); setEditingCurvedId(null); }}>إلغاء</button>
              <button className="btn btn-primary btn-sm" onClick={commitCurvedText}>
                {editingCurvedId ? '✦ تحديث' : '✦ إضافة للوحة'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ====== SVG FILTER MODAL ====== */}
      {showFilterModal && (
        <div
          style={{
            position: 'fixed', inset: 0,
            background: 'rgba(0,0,0,0.65)',
            backdropFilter: 'blur(6px)',
            zIndex: 9999,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
          onClick={() => setShowFilterModal(false)}
        >
          <div className="modal-box" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <span>✨ فلاتر SVG للعنصر المحدد</span>
              <button className="modal-close" onClick={() => setShowFilterModal(false)}><X size={16} /></button>
            </div>
            <div className="modal-body">
              {!activeObject ? (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', padding: '20px 0' }}>
                  الرجاء تحديد عنصر أولاً لتطبيق الفلاتر عليه
                </p>
              ) : (
                <>
                  <div className="modal-field">
                    <label>ضبابية (Blur): {blurAmount}px</label>
                    <input type="range" className="range-slider" min="0" max="20" step="0.5" value={blurAmount}
                      onChange={e => {
                        const n = Number(e.target.value);
                        setBlurAmount(n);
                        if (!fabricCanvas || !activeObject) return;
                        if (n === 0) {
                          activeObject.filters = activeObject.filters?.filter(f => f.type !== 'Blur') || [];
                        } else {
                          const blurFilter = new fabric.filters.Blur({ blur: n / 100 });
                          activeObject.filters = [blurFilter, ...(activeObject.filters?.filter(f => f.type !== 'Blur') || [])];
                        }
                        activeObject.applyFilters();
                        fabricCanvas.requestRenderAll();
                      }}
                    />
                  </div>
                  <div className="sep" />
                  <div className="modal-field">
                    <label>إضاءة (Brightness)</label>
                    <input type="range" className="range-slider" min="-1" max="1" step="0.05" defaultValue="0"
                      onChange={e => {
                        const n = Number(e.target.value);
                        if (!fabricCanvas || !activeObject) return;
                        const bf = new fabric.filters.Brightness({ brightness: n });
                        activeObject.filters = [bf, ...(activeObject.filters?.filter(f => f.type !== 'Brightness') || [])];
                        activeObject.applyFilters();
                        fabricCanvas.requestRenderAll();
                      }}
                    />
                  </div>
                  <div className="modal-field">
                    <label>تشبع الألوان (Saturation)</label>
                    <input type="range" className="range-slider" min="-1" max="1" step="0.05" defaultValue="0"
                      onChange={e => {
                        const n = Number(e.target.value);
                        if (!fabricCanvas || !activeObject) return;
                        const sf = new fabric.filters.Saturation({ saturation: n });
                        activeObject.filters = [sf, ...(activeObject.filters?.filter(f => f.type !== 'Saturation') || [])];
                        activeObject.applyFilters();
                        fabricCanvas.requestRenderAll();
                      }}
                    />
                  </div>
                  <div className="modal-field">
                    <label>درامية (Contrast)</label>
                    <input type="range" className="range-slider" min="-1" max="1" step="0.05" defaultValue="0"
                      onChange={e => {
                        const n = Number(e.target.value);
                        if (!fabricCanvas || !activeObject) return;
                        const cf = new fabric.filters.Contrast({ contrast: n });
                        activeObject.filters = [cf, ...(activeObject.filters?.filter(f => f.type !== 'Contrast') || [])];
                        activeObject.applyFilters();
                        fabricCanvas.requestRenderAll();
                      }}
                    />
                  </div>
                  <div className="sep" />
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    <button className="btn btn-ghost btn-sm" onClick={() => {
                      if (!fabricCanvas || !activeObject) return;
                      const gf = new fabric.filters.Grayscale();
                      activeObject.filters = [gf];
                      activeObject.applyFilters();
                      fabricCanvas.requestRenderAll();
                    }}>تدرج رمادي</button>
                    <button className="btn btn-ghost btn-sm" onClick={() => {
                      if (!fabricCanvas || !activeObject) return;
                      const sf = new fabric.filters.Sepia();
                      activeObject.filters = [sf];
                      activeObject.applyFilters();
                      fabricCanvas.requestRenderAll();
                    }}>سيبيا عتيق</button>
                    <button className="btn btn-ghost btn-sm" onClick={() => {
                      if (!fabricCanvas || !activeObject) return;
                      const ivf = new fabric.filters.Invert();
                      activeObject.filters = [ivf];
                      activeObject.applyFilters();
                      fabricCanvas.requestRenderAll();
                    }}>عكس الألوان</button>
                    <button className="btn btn-danger btn-sm" onClick={() => {
                      if (!fabricCanvas || !activeObject) return;
                      activeObject.filters = [];
                      activeObject.applyFilters();
                      fabricCanvas.requestRenderAll();
                      setBlurAmount(0);
                    }}>مسح الكل</button>
                  </div>
                </>
              )}
            </div>
            <div className="modal-footer">
              <button className="btn btn-primary btn-sm" onClick={() => setShowFilterModal(false)}>تطبيق وإغلاق</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
