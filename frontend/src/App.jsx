import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as fabric from 'fabric';
import {
  Sparkles, Type, Download, Layers, MousePointer2, Wand2,
  Loader2, Undo2, Redo2, Trash2, Square, Circle,
  AlignCenter, Bold, Italic, Move, Image as ImageIcon,
  Save, FolderOpen, ChevronDown, X, TriangleAlert, Star,
  Settings2, Palette, Pentagon, PenLine, Hexagon, LayoutTemplate
} from 'lucide-react';
import {
  ICON_SIZES, ICON_TEMPLATES, ICON_SVG_ICONS,
  SIG_SIZES, SIG_TEMPLATES, SIG_SVG_ICONS, SIG_CALLIGRAPHY_FONTS,
  ORNAMENTS
} from './sectionConfigs.js';
import './index.css';

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
    id: 'coffee',
    label: 'مقهى',
    emoji: '☕',
    bg: '#2d1b0e',
    objects: [
      { type: 'rect', fill: '#c8860a', rx: 70, ry: 70, width: 320, height: 320, left: 240, top: 240 },
      { type: 'text', text: 'مَقهى', fontSize: 80, fontFamily: 'Amiri', fill: '#fff', left: 270, top: 288, fontWeight: 'bold' },
      { type: 'text', text: 'C A F É', fontSize: 20, fontFamily: 'Outfit', fill: '#c8860a', left: 318, top: 420, charSpacing: 250 },
    ]
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
    ]
  },
  {
    id: 'elegant',
    label: 'أناقة',
    emoji: '✨',
    bg: '#080808',
    objects: [
      { type: 'text', text: 'LUXE', fontSize: 96, fontFamily: 'Georgia', fill: '#c9a227', left: 230, top: 310, fontWeight: 'bold' },
      { type: 'text', text: '— النخبـة —', fontSize: 26, fontFamily: 'Amiri', fill: '#64748b', left: 290, top: 435 },
    ]
  },
  {
    id: 'minimal',
    label: 'مينيمال',
    emoji: '◻️',
    bg: '#f8fafc',
    objects: [
      { type: 'rect', fill: '#0f1115', rx: 10, ry: 10, width: 340, height: 100, left: 230, top: 350 },
      { type: 'text', text: 'BRAND', fontSize: 50, fontFamily: 'Outfit', fill: '#ffffff', left: 265, top: 368, fontWeight: '700', charSpacing: 200 },
    ]
  },
  {
    id: 'sports',
    label: 'رياضة',
    emoji: '🏆',
    bg: '#0a1628',
    objects: [
      { type: 'rect', fill: '#f59e0b', rx: 0, ry: 0, width: 400, height: 12, left: 200, top: 390 },
      { type: 'text', text: 'CHAMPIONS', fontSize: 54, fontFamily: 'Outfit', fill: '#ffffff', left: 200, top: 310, fontWeight: '800', charSpacing: 80 },
      { type: 'text', text: 'أبطال', fontSize: 40, fontFamily: 'Cairo', fill: '#f59e0b', left: 320, top: 415, fontWeight: 'bold' },
    ]
  },
  {
    id: 'restaurant',
    label: 'مطعم',
    emoji: '🍽️',
    bg: '#1a0a04',
    objects: [
      { type: 'circle', fill: 'transparent', stroke: '#b45309', strokeWidth: 4, radius: 160, left: 240, top: 240 },
      { type: 'text', text: 'مطعــم', fontSize: 62, fontFamily: 'Amiri', fill: '#fbbf24', left: 280, top: 318, fontWeight: 'bold' },
      { type: 'text', text: 'RESTAURANT', fontSize: 16, fontFamily: 'Outfit', fill: '#b45309', left: 263, top: 407, charSpacing: 180 },
    ]
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
    ]
  },
  {
    id: 'medical',
    label: 'طب',
    emoji: '⚕️',
    bg: '#f0fdf4',
    objects: [
      { type: 'circle', fill: '#16a34a', radius: 100, left: 300, top: 200 },
      { type: 'rect', fill: '#ffffff', rx: 4, ry: 4, width: 30, height: 100, left: 370, top: 250 },
      { type: 'rect', fill: '#ffffff', rx: 4, ry: 4, width: 100, height: 30, left: 335, top: 285 },
      { type: 'text', text: 'عيادة الشفاء', fontSize: 38, fontFamily: 'Cairo', fill: '#15803d', left: 275, top: 440, fontWeight: 'bold' },
    ]
  },
];

// Built-in SVG icon library (paths only)
const SVG_ICONS = [
  { label: 'نجمة', emoji: '⭐', svg: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' },
  { label: 'قلب', emoji: '❤', svg: 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z' },
  { label: 'برق', emoji: '⚡', svg: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z' },
  { label: 'صاروخ', emoji: '🚀', svg: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z' },
  { label: 'خاتم', emoji: '💎', svg: 'M6 2l-4 6 10 14L22 8l-4-6H6zM3.43 8L6.37 4h11.26l2.94 4H3.43zm8.57 11.8L4.56 10h14.88L12 19.8z' },
  { label: 'شعلة', emoji: '🔥', svg: 'M13.5 0.67s.74 2.65.74 4.8c0 2.06-1.35 3.73-3.41 3.73-2.07 0-3.63-1.67-3.63-3.73l.03-.36C5.21 7.51 4 10.62 4 14c0 4.42 3.58 8 8 8s8-3.58 8-8C20 8.61 17.41 3.8 13.5.67zM11.71 19c-1.78 0-3.22-1.4-3.22-3.14 0-1.62 1.05-2.76 2.81-3.12 1.77-.36 3.6-1.21 4.62-2.58.39 1.29.59 2.65.59 4.04 0 2.65-2.15 4.8-4.8 4.8z' },
  { label: 'ورقة', emoji: '🍃', svg: 'M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1-2.3A4.49 4.49 0 0 0 8 20C19 20 22 3 22 3c-1 2-8 2-8 2z' },
  { label: 'موجة', emoji: '🌊', svg: 'M2 8c1.5-2 3-2 4.5 0s3 2 4.5 0 3-2 4.5 0 3 2 4.5 0M2 14c1.5-2 3-2 4.5 0s3 2 4.5 0 3-2 4.5 0 3 2 4.5 0' },
  { label: 'هلال', emoji: '🌙', svg: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' },
  { label: 'عين', emoji: '👁', svg: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zm11 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6z' },
  { label: 'جبل', emoji: '⛰️', svg: 'M3 17l6-12 4 7 2.5-4L21 17H3z' },
  { label: 'اللانهاية', emoji: '∞', svg: 'M18.6 6.62c-1.44 0-2.8.56-3.77 1.53L12 10.66 10.48 12h.01L7.8 14.39c-.64.64-1.49.99-2.4.99-1.87 0-3.39-1.51-3.39-3.38S3.53 8.62 5.4 8.62c.91 0 1.76.35 2.44 1.03l1.13 1 1.51-1.34L9.22 8.2C8.2 7.18 6.84 6.62 5.4 6.62 2.42 6.62 0 9.04 0 12s2.42 5.38 5.4 5.38c1.44 0 2.8-.56 3.77-1.53l2.83-2.51.01.01L13.52 12h-.01l2.69-2.39c.64-.64 1.49-.99 2.4-.99 1.87 0 3.39 1.51 3.39 3.38s-1.52 3.38-3.39 3.38c-.9 0-1.76-.35-2.44-1.03l-1.14-1.01-1.51 1.34 1.27 1.12c1.02 1.01 2.37 1.57 3.82 1.57 2.98 0 5.4-2.41 5.4-5.38s-2.42-5.38-5.4-5.38z' },
];


// ============================================================
// HELPERS
// ============================================================
function getLayerLabel(obj) {
  if (!obj) return 'عنصر';
  if (obj.type === 'i-text' || obj.type === 'text') {
    return `نص: "${(obj.text || '').slice(0, 16)}..."`;
  }
  if (obj.type === 'image') return '🖼️ صورة ذكاء اصطناعي';
  if (obj.type === 'rect') return '▭ مستطيل';
  if (obj.type === 'circle') return '○ دائرة';
  if (obj.type === 'polygon') return '⬡ مضلع';
  return obj.type || 'عنصر';
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

  // ── Section navigation: 'logo' | 'icon' | 'signature' ──
  const [section, setSection] = useState('logo');

  // Derived section-specific config (changes when section changes)
  const sectionConfig = (() => {
    if (section === 'icon') return {
      templates: ICON_TEMPLATES,
      sizes: ICON_SIZES,
      icons: ICON_SVG_ICONS,
      defaultSize: { w: 512, h: 512 },
      fonts: ALL_FONTS,
      aiHint: 'مثال: أيقونة تطبيق بتصميم مسطح، رمز البرق الأزرق على خلفية داكنة',
    };
    if (section === 'signature') return {
      templates: SIG_TEMPLATES,
      sizes: SIG_SIZES,
      icons: SIG_SVG_ICONS,
      defaultSize: { w: 800, h: 300 },
      fonts: [...SIG_CALLIGRAPHY_FONTS, ...ALL_FONTS.filter(f => !SIG_CALLIGRAPHY_FONTS.find(s => s.value === f.value))],
      aiHint: 'مثال: توقيع إلكتروني أنيق باسم "محمد" بخط عربي ذهبي على خلفية داكنة',
    };
    return {
      templates: TEMPLATES,
      sizes: CANVAS_SIZES,
      icons: SVG_ICONS,
      defaultSize: { w: 800, h: 800 },
      fonts: ALL_FONTS,
      aiHint: 'مثال: أسد هادئ بأسلوب فيكتور مسطح لشركة تقنية، لا نص',
    };
  })();

  // AI State
  const [aiPrompt, setAiPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [aiError, setAiError] = useState('');

  // Object Properties (synced from active object)
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

  // --------------------------------------------------------
  // CANVAS INIT
  // --------------------------------------------------------
  useEffect(() => {
    const canvas = new fabric.Canvas(canvasRef.current, {
      width: 800,
      height: 800,
      backgroundColor: '#ffffff',
      preserveObjectStacking: true,
      selectionBorderColor: '#6366f1',
      selectionColor: 'rgba(99,102,241,0.08)',
      selectionLineWidth: 1.5,
    });
    setFabricCanvas(canvas);

    // Selection events
    const onSelect = (e) => {
      const obj = e.selected?.[0];
      setActiveObject(obj || null);
      syncPropsFromObject(obj);
    };
    const onDeselect = () => {
      setActiveObject(null);
    };

    canvas.on('selection:created', onSelect);
    canvas.on('selection:updated', onSelect);
    canvas.on('selection:cleared', onDeselect);

    // Object modified → save to history + refresh layers
    canvas.on('object:modified', () => {
      saveSnapshot(canvas);
      refreshLayers(canvas);
      const obj = canvas.getActiveObject();
      if (obj) syncPropsFromObject(obj);
    });

    canvas.on('object:added', () => {
      saveSnapshot(canvas);
      refreshLayers(canvas);
    });

    canvas.on('object:removed', () => {
      saveSnapshot(canvas);
      refreshLayers(canvas);
    });

    // Initial snapshot
    saveSnapshot(canvas);

    return () => canvas.dispose();
  }, []); // eslint-disable-line

  // ── When section changes: resize canvas + clear ──
  useEffect(() => {
    if (!fabricCanvas) return;
    const { w, h } = sectionConfig.defaultSize;
    historyRef.current.paused = true;
    fabricCanvas.clear();
    fabricCanvas.backgroundColor = '#ffffff';
    fabricCanvas.setDimensions({ width: w, height: h });
    fabricCanvas.requestRenderAll();
    setCanvasSize({ w, h });
    setLayers([]);
    setActiveObject(null);
    historyRef.current = { stack: [], idx: -1, paused: false };
    setHistory([]);
    setHistoryIndex(-1);
  }, [section]); // eslint-disable-line

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

  // --------------------------------------------------------
  // HISTORY (Undo / Redo)
  // --------------------------------------------------------
  const saveSnapshot = useCallback((canvas) => {
    if (!canvas || historyRef.current.paused) return;
    // Include background in snapshot
    const json = JSON.stringify({
      ...canvas.toJSON(['id']),
      backgroundColor: canvas.backgroundColor,
    });
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
    // Restore background color explicitly (Fabric v6 fix)
    if (data.backgroundColor) {
      canvas.backgroundColor = data.backgroundColor;
    }
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
      fontFamily: 'Cairo',
      fill: '#0f1115',
      fontSize: 56,
      fontWeight: 'bold',
    });
    fabricCanvas.add(text);
    fabricCanvas.setActiveObject(text);
    fabricCanvas.renderAll();
    text.enterEditing();
  };

  const addRect = () => {
    if (!fabricCanvas) return;
    const r = new fabric.Rect({
      left: fabricCanvas.width / 2 - 100,
      top: fabricCanvas.height / 2 - 60,
      fill: '#6366f1', width: 200, height: 120, rx: 12, ry: 12,
    });
    fabricCanvas.add(r);
    fabricCanvas.setActiveObject(r);
    fabricCanvas.renderAll();
  };

  const addCircle = () => {
    if (!fabricCanvas) return;
    const c = new fabric.Circle({
      left: fabricCanvas.width / 2 - 80,
      top: fabricCanvas.height / 2 - 80,
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
      pts.push({
        x: 80 * Math.cos((i * 2 * Math.PI) / 6),
        y: 80 * Math.sin((i * 2 * Math.PI) / 6),
      });
    }
    const p = new fabric.Polygon(pts, {
      left: fabricCanvas.width / 2 - 80,
      top: fabricCanvas.height / 2 - 80,
      fill: '#ec4899',
    });
    fabricCanvas.add(p);
    fabricCanvas.setActiveObject(p);
    fabricCanvas.renderAll();
  };

  const addSvgIcon = (icon) => {
    if (!fabricCanvas) return;
    // Parse an SVG string and add as a Fabric Path
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
    // Fabric v6: clone() returns a Promise
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

  const handleFillChange = (val) => {
    setFillColor(val);
    applyProp('fill', val);
  };

  const handleStrokeChange = (val) => {
    setStrokeColor(val);
    applyProp('stroke', val);
  };

  const handleStrokeWidthChange = (val) => {
    const n = Number(val);
    setStrokeWidth(n);
    applyProp('strokeWidth', n);
  };

  const handleOpacityChange = (val) => {
    const n = Number(val);
    setOpacity(n);
    applyProp('opacity', n / 100);
  };

  const handleFontSizeChange = (val) => {
    const n = Number(val);
    setFontSize(n);
    applyProp('fontSize', n);
  };

  const handleFontFamilyChange = (val) => {
    setFontFamily(val);
    applyProp('fontFamily', val);
  };

  const handleBoldToggle = () => {
    const next = !isBold;
    setIsBold(next);
    applyProp('fontWeight', next ? 'bold' : 'normal');
  };

  const handleItalicToggle = () => {
    const next = !isItalic;
    setIsItalic(next);
    applyProp('fontStyle', next ? 'italic' : 'normal');
  };

  const handleShadowChange = (val) => {
    const n = Number(val);
    setShadowBlur(n);
    if (!fabricCanvas || !activeObject) return;
    if (n === 0) {
      activeObject.set('shadow', null);
    } else {
      activeObject.set('shadow', new fabric.Shadow({
        color: 'rgba(0,0,0,0.4)', blur: n, offsetX: 4, offsetY: 4,
      }));
    }
    fabricCanvas.renderAll();
  };

  const handleCornerRadiusChange = (val) => {
    const n = Number(val);
    setCornerRadius(n);
    applyProp('rx', n);
    applyProp('ry', n);
  };

  const handlePosXChange = (val) => {
    const n = Number(val);
    setPosX(n);
    applyProp('left', n);
  };

  const handlePosYChange = (val) => {
    const n = Number(val);
    setPosY(n);
    applyProp('top', n);
  };

  const handleAngleChange = (val) => {
    const n = Number(val);
    setAngle(n);
    applyProp('angle', n);
  };

  const handleSkewXChange = (val) => {
    const n = Number(val);
    setSkewX(n);
    applyProp('skewX', n);
  };

  const handleCharSpacingChange = (val) => {
    const n = Number(val);
    setCharSpacing(n);
    applyProp('charSpacing', n);
  };

  // Canvas background color — using direct property (Fabric v6+)
  const handleCanvasBg = (val) => {
    if (!fabricCanvas) return;
    fabricCanvas.backgroundColor = val;
    fabricCanvas.requestRenderAll();
  };

  // --------------------------------------------------------
  // TEMPLATES
  // --------------------------------------------------------
  const applyTemplate = (tpl) => {
    if (!fabricCanvas) return;

    // Pause history during bulk load
    historyRef.current.paused = true;
    fabricCanvas.clear();

    // Set background color using Fabric v6+ direct property
    const solidBg = tpl.bg.startsWith('linear-gradient') || tpl.bg.startsWith('radial-gradient')
      ? (tpl.bg.includes('#2d1b0e') ? '#2d1b0e' : tpl.bg.includes('#0f0c29') ? '#0f0c29' : '#0a0a0a')
      : tpl.bg;
    fabricCanvas.backgroundColor = solidBg;

    // Scale positions to canvas size based on the section's design default dimension
    const defW = sectionConfig.defaultSize.w;
    const defH = sectionConfig.defaultSize.h;
    const scaleX = fabricCanvas.width / defW;
    const scaleY = fabricCanvas.height / defH;
    const scaleFont = Math.min(scaleX, scaleY);

    tpl.objects.forEach(o => {
      // Build scaled props, remove undefined
      const base = { ...o };
      delete base.type;
      if (o.text !== undefined) delete base.text;

      const scaledProps = {
        ...base,
        left: (o.left || 100) * scaleX,
        top: (o.top || 100) * scaleY,
        ...(o.fontSize && { fontSize: o.fontSize * scaleFont }),
        ...(o.width && { width: o.width * scaleX }),
        ...(o.height && { height: o.height * scaleY }),
        ...(o.radius && { radius: o.radius * scaleFont }),
        ...(o.rx && { rx: o.rx * scaleFont, ry: o.rx * scaleFont }),
      };

      let obj;
      if (o.type === 'text') {
        obj = new fabric.IText(o.text, scaledProps);
      } else if (o.type === 'rect') {
        obj = new fabric.Rect(scaledProps);
      } else if (o.type === 'circle') {
        obj = new fabric.Circle(scaledProps);
      }
      if (obj) fabricCanvas.add(obj);
    });

    // Resume history and save snapshot
    historyRef.current.paused = false;
    fabricCanvas.requestRenderAll();
    refreshLayers(fabricCanvas);
    saveSnapshot(fabricCanvas);
  };

  // --------------------------------------------------------
  // SAVE / LOAD
  // --------------------------------------------------------
  const saveProject = () => {
    if (!fabricCanvas) return;
    const json = JSON.stringify({ version: '2.0', canvas: fabricCanvas.toJSON() });
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `iconora_project_${Date.now()}.json`;
    a.click();
  };

  const loadProject = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = async (e) => {
      const file = e.target.files?.[0];
      if (!file || !fabricCanvas) return;
      const reader = new FileReader();
      reader.onload = async (ev) => {
        try {
          const data = JSON.parse(ev.target.result);
          const canvasData = data.canvas || data;
          await fabricCanvas.loadFromJSON(canvasData);
          if (canvasData.backgroundColor) {
            fabricCanvas.backgroundColor = canvasData.backgroundColor;
          }
          fabricCanvas.requestRenderAll();
          refreshLayers(fabricCanvas);
          saveSnapshot(fabricCanvas);
        } catch (err) {
          console.error('Load error:', err);
          alert('خطأ في قراءة الملف');
        }
      };
      reader.readAsText(file);
    };
    input.click();
  };

  const loadImage = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
      const file = e.target.files?.[0];
      if (!file || !fabricCanvas) return;
      const url = URL.createObjectURL(file);
      const imgEl = new window.Image();
      imgEl.src = url;
      imgEl.onload = () => {
        const fImg = new fabric.FabricImage(imgEl);
        if (fImg.width > fabricCanvas.width * 0.8) {
          fImg.scaleToWidth(fabricCanvas.width * 0.8);
        }
        fImg.set({ left: 40, top: 40 });
        fabricCanvas.add(fImg);
        fabricCanvas.setActiveObject(fImg);
        fabricCanvas.renderAll();
      };
    };
    input.click();
  };

  const applyGoldGradient = () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (!active) return;
    // We create a linear gold gradient bounds based on the object size
    const grad = new fabric.Gradient({
      type: 'linear',
      coords: { x1: 0, y1: 0, x2: active.width, y2: active.height },
      colorStops: [
        { offset: 0, color: '#bf953f' },
        { offset: 0.25, color: '#fcf6ba' },
        { offset: 0.5, color: '#b38728' },
        { offset: 0.75, color: '#fbf5b7' },
        { offset: 1, color: '#aa771c' },
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
    if (active) {
      active.set('flipX', !active.flipX);
      fabricCanvas.requestRenderAll();
    }
  };
  
  const toggleFlipY = () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (active) {
      active.set('flipY', !active.flipY);
      fabricCanvas.requestRenderAll();
    }
  };

  // Export PNG with quality options
  const exportPng = (multiplier = 2) => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (active) {
      fabricCanvas.discardActiveObject();
      fabricCanvas.requestRenderAll();
    }
    // Small delay to ensure deselect renders
    setTimeout(() => {
      const dataUrl = fabricCanvas.toDataURL({ format: 'png', multiplier });
      if (active) {
        fabricCanvas.setActiveObject(active);
        fabricCanvas.requestRenderAll();
      }
      const qualityLabel = multiplier === 1 ? '1x' : multiplier === 2 ? '2x' : '4x';
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = `iconora_${qualityLabel}_${Date.now()}.png`;
      a.click();
    }, 80);
  };

  const exportSvg = () => {
    if (!fabricCanvas) return;
    const svg = fabricCanvas.toSVG();
    const blob = new Blob([svg], { type: 'image/svg+xml' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `iconora_${Date.now()}.svg`;
    a.click();
  };

  const exportIco = async () => {
    if (!fabricCanvas) return;
    const active = fabricCanvas.getActiveObject();
    if (active) {
      fabricCanvas.discardActiveObject();
      fabricCanvas.requestRenderAll();
    }
    
    // We export a 256x256 PNG for the ICO
    const multiplier = 256 / fabricCanvas.width;
    const dataUrl = fabricCanvas.toDataURL({ format: 'png', multiplier });
    
    if (active) {
      fabricCanvas.setActiveObject(active);
      fabricCanvas.requestRenderAll();
    }

    try {
      const resp = await fetch(dataUrl);
      const blob = await resp.blob();
      const arrayBuffer = await blob.arrayBuffer();
      const pngUint8 = new Uint8Array(arrayBuffer);
      
      // Construct ICO header
      const header = new Uint8Array(22);
      header[2] = 1; // Type ICO
      header[4] = 1; // 1 image
      header[6] = 0; // width 0 means 256
      header[7] = 0; // height 0 means 256
      header[10] = 1; // Planes
      header[12] = 32; // Bits per pixel
      
      // PNG Size
      const size = pngUint8.length;
      header[14] = size & 0xff;
      header[15] = (size >> 8) & 0xff;
      header[16] = (size >> 16) & 0xff;
      header[17] = (size >> 24) & 0xff;
      
      // Offset
      header[18] = 22; // Starts immediately after header
      
      const icoBlob = new Blob([header, pngUint8], { type: 'image/x-icon' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(icoBlob);
      a.download = `iconora_favicon_${Date.now()}.ico`;
      a.click();
    } catch(err) {
      console.error("Failed to make ICO", err);
    }
  };

  // --------------------------------------------------------
  // AI GENERATION
  // --------------------------------------------------------
  const handleGenerateLogo = async () => {
    if (!aiPrompt.trim() || !fabricCanvas) return;
    setIsGenerating(true);
    setAiError('');
    try {
      const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const resp = await fetch(`${baseUrl}/api/generate-logo`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: aiPrompt, remove_background: true }),
      });
      if (!resp.ok) throw new Error('فشل الاتصال بمحرك الذكاء الاصطناعي');
      const data = await resp.json();
      const imgEl = new window.Image();
      imgEl.src = data.image_data;
      imgEl.onload = () => {
        const fImg = new fabric.FabricImage(imgEl);
        if (fImg.width > fabricCanvas.width * 0.5) {
          fImg.scaleToWidth(fabricCanvas.width * 0.5);
        }
        fImg.set({
          left: (fabricCanvas.width - fImg.getScaledWidth()) / 2,
          top: (fabricCanvas.height - fImg.getScaledHeight()) / 2,
        });
        fabricCanvas.add(fImg);
        fabricCanvas.setActiveObject(fImg);
        fabricCanvas.renderAll();
        setAiPrompt('');
      };
    } catch (err) {
      setAiError('تعذر توليد الشعار! ربما الوصف طويل جداً أو حدث خطأ في الخادم.');
    } finally {
      setIsGenerating(false);
    }
  };

  // --------------------------------------------------------
  // SELECT LAYER
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

  // ============================================================
  // RENDER
  // ============================================================
  return (
    <div className="app-container" dir="rtl">

      {/* ====== TOPBAR ====== */}
      <header className="topbar">
        {/* Brand */}
        <div className="topbar-brand">
          <div className="logo-icon">
            <Sparkles size={16} color="white" />
          </div>
          <span className="brand-name">Iconora <span className="brand-accent">Studio</span></span>
          <span className="badge">v2.0</span>
        </div>

        {/* ── Section Navigation ── */}
        <nav style={{ display: 'flex', gap: '4px', background: 'var(--bg-active)', borderRadius: '10px', padding: '3px' }}>
          {[
            { id: 'logo',      icon: <LayoutTemplate size={14} />, label: 'لوجو' },
            { id: 'icon',      icon: <Hexagon size={14} />,        label: 'أيقونات' },
            { id: 'signature', icon: <PenLine size={14} />,        label: 'توقيع' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setSection(tab.id)}
              style={{
                display: 'flex', alignItems: 'center', gap: '6px',
                padding: '6px 14px',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                fontSize: '0.8rem',
                fontWeight: section === tab.id ? 700 : 400,
                background: section === tab.id ? 'var(--primary)' : 'transparent',
                color:      section === tab.id ? '#ffffff' : 'var(--text-muted)',
                transition: 'all 0.2s',
              }}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </nav>
        {/* Center: History + Canvas Size */}
        <div className="topbar-center" style={{ gap: '6px' }}>
          <button className="history-btn" onClick={undo} disabled={!canUndo} title="تراجع (Ctrl+Z)">
            <Undo2 size={16} />
          </button>
          <button className="history-btn" onClick={redo} disabled={!canRedo} title="إعادة (Ctrl+Y)">
            <Redo2 size={16} />
          </button>

          <div className="sep" style={{ width: '1px', height: '20px', margin: '0 4px', background: 'var(--border-2)' }} />

          <select
            className="styled-select"
            style={{ width: 'auto', padding: '5px 8px', fontSize: '0.78rem' }}
            onChange={(e) => {
              const s = CANVAS_SIZES.find(x => x.label === e.target.value);
              if (s && fabricCanvas) {
                fabricCanvas.setDimensions({ width: s.w, height: s.h });
                fabricCanvas.requestRenderAll();
                setCanvasSize({ w: s.w, h: s.h });
              }
            }}
          >
            {sectionConfig.sizes.map(s => (
              <option key={s.label}>{s.label}</option>
            ))}
          </select>
        </div>

        {/* Actions */}
        <div className="topbar-actions">
          <button className="btn btn-ghost btn-sm" onClick={saveProject} title="حفظ المشروع">
            <Save size={15} /> حفظ مشروع (JSON)
          </button>
          <button className="btn btn-ghost btn-sm" onClick={loadProject} title="فتح مشروع">
            <FolderOpen size={15} /> فتح
          </button>
          <div style={{ width: '1px', height: '20px', background: 'var(--border-2)', margin: '0 4px' }} />
          
          {section === 'icon' && (
            <button className="btn btn-ghost btn-sm" style={{ color: '#fcd34d' }} onClick={exportIco} title="تصدير كأيقونة ويندوز/مواقع">
              <Download size={15} /> ICO
            </button>
          )}

          <button className="btn btn-ghost btn-sm" onClick={exportSvg}>
            <Download size={15} /> SVG
          </button>
          {/* PNG quality split button */}
          <div style={{ display: 'flex', borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--primary-dark)' }}>
            <button
              className="btn btn-primary btn-sm"
              style={{ borderRadius: 0, borderRight: '1px solid rgba(255,255,255,0.15)', gap: '6px' }}
              onClick={() => exportPng(2)}
              title="تصدير PNG 2× (جودة عالية)"
            >
              <Download size={14} /> PNG
            </button>
            <button
              className="btn btn-primary btn-sm"
              style={{ borderRadius: 0, padding: '6px 8px', fontSize: '0.72rem', fontWeight: 700 }}
              onClick={() => exportPng(1)}
              title="تصدير بالحجم الأصلي"
            >1×</button>
            <button
              className="btn btn-primary btn-sm"
              style={{ borderRadius: 0, padding: '6px 8px', fontSize: '0.72rem', fontWeight: 700 }}
              onClick={() => exportPng(4)}
              title="تصدير فائق الجودة 4×"
            >4×</button>
          </div>
        </div>
      </header>

      {/* ====== WORKSPACE ====== */}
      <main className="workspace">

        {/* ====== LEFT SIDEBAR ====== */}
        <aside className="sidebar">

          {/* Tools */}
          <div className="sidebar-section">
            <div className="section-label"><Settings2 size={12} /> الأدوات</div>
            <div className="tool-grid">
              <button className="tool-btn" onClick={() => fabricCanvas?.discardActiveObject().renderAll()}>
                <MousePointer2 size={18} />
                تحديد
              </button>
              <button className="tool-btn" onClick={addText}>
                <Type size={18} />
                نص
              </button>
              <button className="tool-btn" onClick={addRect}>
                <Square size={18} />
                مستطيل
              </button>
              <button className="tool-btn" onClick={addCircle}>
                <Circle size={18} />
                دائرة
              </button>
              <button className="tool-btn" onClick={addPolygon}>
                <Pentagon size={18} />
                مضلع
              </button>
              <button className="tool-btn" onClick={loadImage}>
                <ImageIcon size={18} />
                صورة
              </button>
            </div>
          </div>

          {/* Templates */}
          <div className="sidebar-section">
            <div className="section-label"><Star size={12} /> قوالب جاهزة</div>
            <div className="templates-grid" style={{ maxHeight: '220px', overflowY: 'auto', paddingBottom: '4px' }}>
              {sectionConfig.templates.map(tpl => (
                <div key={tpl.id} className="template-card" onClick={() => applyTemplate(tpl)}>
                  <div className="template-preview">{tpl.emoji}</div>
                  {tpl.label}
                </div>
              ))}
            </div>
          </div>

          {/* Icons Library */}
          <div className="sidebar-section">
            <div className="section-label"><Sparkles size={12} /> {section === 'signature' ? 'أيقونات الأعمال' : 'مكتبة أيقونات'}</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '5px', maxHeight: '120px', overflowY: 'auto' }}>
              {sectionConfig.icons.map(icon => (
                <button
                  key={icon.label}
                  title={icon.label}
                  onClick={() => addSvgIcon(icon)}
                  style={{
                    background: 'var(--bg-active)',
                    border: '1px solid var(--border-2)',
                    borderRadius: '6px',
                    padding: '8px 4px',
                    cursor: 'pointer',
                    fontSize: '1.2rem',
                    transition: 'all 0.15s',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                  onMouseEnter={e => {
                    e.currentTarget.style.borderColor = 'var(--primary)';
                    e.currentTarget.style.background = 'var(--primary-glow)';
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.borderColor = 'var(--border-2)';
                    e.currentTarget.style.background = 'var(--bg-active)';
                  }}
                >
                  {icon.emoji}
                </button>
              ))}
            </div>
            <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '6px', textAlign: 'center' }}>
              اضغط لإضافة أيقونة قابلة للتعديل
            </p>
          </div>

          {/* Ornaments Library */}
          <div className="sidebar-section">
            <div className="section-label" style={{ color: '#fbbf24' }}>👑 زخارف فاخرة</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '5px' }}>
              {ORNAMENTS.map(orn => (
                <button
                  key={orn.label}
                  title={orn.label}
                  onClick={() => addSvgIcon(orn)}
                  style={{
                    background: '#2d2411',
                    border: '1px solid #785a16',
                    borderRadius: '6px',
                    padding: '8px 4px',
                    cursor: 'pointer',
                    fontSize: '1.2rem',
                    transition: 'all 0.15s',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                  onMouseEnter={e => { e.currentTarget.style.background = '#423315'; }}
                  onMouseLeave={e => { e.currentTarget.style.background = '#2d2411'; }}
                >
                  {orn.emoji}
                </button>
              ))}
            </div>
          </div>

          {/* AI Generator */}
          <div className="sidebar-section" style={{ flex: 1 }}>
            <div className="section-label"><Wand2 size={12} /> مولد الذكاء الاصطناعي</div>
            <div className="ai-panel">
              <div className="ai-panel-header">
                <Sparkles size={15} />
                توليد شعار بالذكاء الاصطناعي
              </div>
              <textarea
                className="ai-textarea"
                placeholder={sectionConfig.aiHint}
                value={aiPrompt}
                onChange={e => setAiPrompt(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Enter' && e.ctrlKey) handleGenerateLogo();
                }}
              />
              {aiError && (
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center', color: 'var(--warning)', fontSize: '0.75rem', background: 'rgba(245,158,11,0.08)', padding: '8px', borderRadius: '6px', border: '1px solid rgba(245,158,11,0.2)' }}>
                  <TriangleAlert size={13} />
                  {aiError}
                </div>
              )}
              <button
                className={`btn btn-primary btn-full ${isGenerating ? 'generating-indicator' : ''}`}
                onClick={handleGenerateLogo}
                disabled={isGenerating || !aiPrompt.trim()}
              >
                {isGenerating ? (
                  <><Loader2 size={15} className="animate-spin" /> جاري التوليد...</>
                ) : (
                  <><Wand2 size={15} /> توليد ودمج</>
                )}
              </button>
              <p className="ai-note">
                Ctrl+Enter للتوليد السريع • يدعم العربية والإنجليزية<br />
                <span style={{ color: 'var(--text-faint)' }}>يتطلب تشغيل: python server.py</span>
              </p>
            </div>
          </div>

          {/* Layers */}
          <div className="sidebar-section">
            <div className="section-label"><Layers size={12} /> الطبقات ({layers.length})</div>
            {layers.length === 0 ? (
              <div className="empty-layers">لا توجد عناصر بعد</div>
            ) : (
              <div className="layers-list">
                {layers.map((l, i) => (
                  <div
                    key={i}
                    className={`layer-item ${activeObject === l.obj ? 'active' : ''}`}
                    onClick={() => selectLayer(l.obj)}
                  >
                    <span className="layer-icon"><Layers size={12} /></span>
                    <span className="layer-name">{l.label}</span>
                    <button
                      className="layer-delete"
                      onClick={e => { e.stopPropagation(); deleteLayer(l.obj); }}
                    >
                      <X size={12} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </aside>

        {/* ====== CANVAS ====== */}
        <div className="canvas-container-outer">
          <div className="canvas-wrapper fade-in">
            <canvas ref={canvasRef} id="main-canvas" />
          </div>

          {/* Zoom info */}
          <div className="canvas-zoom-info">
            <span>{canvasSize.w} × {canvasSize.h} px</span>
            <span>•</span>
            <span>{zoom}%</span>
            {activeObject && (
              <>
                <span>•</span>
                <span style={{ color: 'var(--primary-light)' }}>{getLayerLabel(activeObject)}</span>
              </>
            )}
          </div>
        </div>

        {/* ====== RIGHT PANEL ====== */}
        <aside className="control-panel">
          {activeObject ? (
            <div className="fade-in">
              {/* Tabs */}
              <div className="prop-tabs">
                <button
                  className={`prop-tab ${activePropTab === 'style' ? 'active' : ''}`}
                  onClick={() => setActivePropTab('style')}
                >
                  <Palette size={13} style={{ display: 'inline', marginLeft: '4px' }} />
                  المظهر
                </button>
                {isText && (
                  <button
                    className={`prop-tab ${activePropTab === 'text' ? 'active' : ''}`}
                    onClick={() => setActivePropTab('text')}
                  >
                    <Type size={13} style={{ display: 'inline', marginLeft: '4px' }} />
                    النص
                  </button>
                )}
                <button
                  className={`prop-tab ${activePropTab === 'position' ? 'active' : ''}`}
                  onClick={() => setActivePropTab('position')}
                >
                  <Move size={13} style={{ display: 'inline', marginLeft: '4px' }} />
                  الموضع
                </button>
              </div>

              {/* === STYLE TAB === */}
              {activePropTab === 'style' && (
                <div className="panel-section">
                  {/* Fill */}
                  {activeObject.type !== 'image' && (
                    <>
                      <div className="panel-title">اللون الداخلي</div>
                      <div className="control-row">
                        <div className="color-swatch-row" style={{ width: '100%' }}>
                          <div className="color-input-wrapper">
                            <input type="color" value={fillColor} onChange={e => handleFillChange(e.target.value)} />
                          </div>
                          <input
                            className="color-hex"
                            value={fillColor}
                            onChange={e => handleFillChange(e.target.value)}
                            maxLength={7}
                          />
                        </div>
                      </div>
                      {/* Quick color palette */}
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '8px' }}>
                        {[
                          '#ffffff','#0f1115','#f8fafc','#1e293b','#334155',
                          '#6366f1','#818cf8','#a855f7','#ec4899','#ef4444',
                          '#f59e0b','#22c55e','#14b8a6','#0ea5e9','#c9a227',
                          '#2d1b0e','#0d0d1f','#080808','#0a1628','#f0fdf4',
                        ].map(c => (
                          <div
                            key={c}
                            onClick={() => handleFillChange(c)}
                            title={c}
                            style={{
                              width: 20, height: 20,
                              borderRadius: 4,
                              background: c,
                              cursor: 'pointer',
                              border: fillColor === c
                                ? '2px solid var(--primary)'
                                : '1px solid var(--border-2)',
                              flexShrink: 0,
                              transition: 'transform 0.1s',
                            }}
                            onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.2)'}
                            onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                          />
                        ))}
                      </div>

                      <div className="sep" />

                      {/* Stroke */}
                      <div className="panel-title">الحدود (Stroke)</div>
                      <div className="color-swatch-row" style={{ marginBottom: '8px' }}>
                        <div className="color-input-wrapper">
                          <input type="color" value={strokeColor} onChange={e => handleStrokeChange(e.target.value)} />
                        </div>
                        <input
                          className="color-hex"
                          value={strokeColor}
                          onChange={e => handleStrokeChange(e.target.value)}
                          maxLength={7}
                        />
                      </div>
                      <div className="control-row">
                        <span className="control-label">سُمك الحد</span>
                        <div className="range-row" style={{ flex: 1 }}>
                          <input
                            type="range" className="range-slider"
                            min="0" max="20" value={strokeWidth}
                            onChange={e => handleStrokeWidthChange(e.target.value)}
                          />
                          <span className="control-value">{strokeWidth}px</span>
                        </div>
                      </div>

                      <div className="sep" />
                    </>
                  )}

                  {/* Opacity */}
                  <div className="panel-title">الشفافية (Opacity)</div>
                  <div className="control-row">
                    <div className="range-row" style={{ flex: 1 }}>
                      <input
                        type="range" className="range-slider"
                        min="0" max="100" value={opacity}
                        onChange={e => handleOpacityChange(e.target.value)}
                      />
                      <span className="control-value">{opacity}%</span>
                    </div>
                  </div>

                  <div className="sep" />

                  {/* Shadow */}
                  <div className="panel-title">الظل (Shadow)</div>
                  <div className="control-row">
                    <div className="range-row" style={{ flex: 1 }}>
                      <input
                        type="range" className="range-slider"
                        min="0" max="40" value={shadowBlur}
                        onChange={e => handleShadowChange(e.target.value)}
                      />
                      <span className="control-value">{shadowBlur}px</span>
                    </div>
                  </div>

                  {/* Corner Radius (rect only) */}
                  {isShape && (
                    <>
                      <div className="sep" />
                      <div className="panel-title">انحناء الزوايا</div>
                      <div className="control-row">
                        <div className="range-row" style={{ flex: 1 }}>
                          <input
                            type="range" className="range-slider"
                            min="0" max="100" value={cornerRadius}
                            onChange={e => handleCornerRadiusChange(e.target.value)}
                          />
                          <span className="control-value">{cornerRadius}px</span>
                        </div>
                      </div>
                    </>
                  )}

                  <div className="sep" />

                  {/* Actions */}
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={duplicateSelected}>
                      تكرار
                    </button>
                    <button className="btn btn-danger btn-sm" onClick={deleteSelected}>
                      <Trash2 size={13} />
                    </button>
                  </div>
                </div>
              )}

              {/* === TEXT TAB === */}
              {activePropTab === 'text' && isText && (
                <div className="panel-section">
                  <div className="panel-title">الخط</div>
                  <select
                    className="styled-select"
                    value={fontFamily}
                    onChange={e => handleFontFamilyChange(e.target.value)}
                    style={{ marginBottom: '10px' }}
                  >
                    {sectionConfig.fonts.map(f => (
                      <option key={f.value} value={f.value}>{f.label}</option>
                    ))}
                  </select>

                  <div className="panel-title">حجم الخط</div>
                  <div className="control-row" style={{ marginBottom: '10px' }}>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input
                        type="range" className="range-slider"
                        min="8" max="200" value={fontSize}
                        onChange={e => handleFontSizeChange(e.target.value)}
                      />
                      <span className="control-value">{fontSize}px</span>
                    </div>
                  </div>

                  <div className="panel-title">التنسيق</div>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button
                      className={`btn btn-ghost btn-sm ${isBold ? 'active' : ''}`}
                      style={isBold ? { background: 'var(--primary-glow)', borderColor: 'var(--primary)', color: 'var(--primary-light)' } : {}}
                      onClick={handleBoldToggle}
                    >
                      <Bold size={14} /> غامق
                    </button>
                    <button
                      className={`btn btn-ghost btn-sm ${isItalic ? 'active' : ''}`}
                      style={isItalic ? { background: 'var(--primary-glow)', borderColor: 'var(--primary)', color: 'var(--primary-light)' } : {}}
                      onClick={handleItalicToggle}
                    >
                      <Italic size={14} /> مائل
                    </button>
                  </div>
                  
                  <div className="sep" />
                  
                  <div className="panel-title">تباعد الأحرف (مد الكلمة)</div>
                  <div className="control-row">
                    <div className="range-row" style={{ flex: 1 }}>
                      <input
                        type="range" className="range-slider"
                        min="-200" max="600" value={charSpacing}
                        onChange={e => handleCharSpacingChange(e.target.value)}
                      />
                      <span className="control-value">{charSpacing}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* === POSITION TAB === */}
              {activePropTab === 'position' && (
                <div className="panel-section">
                  <div className="panel-title">الموضع</div>
                  <div className="control-row">
                    <span className="control-label">المحور X</span>
                    <input
                      type="number"
                      className="num-input"
                      value={posX}
                      onChange={e => handlePosXChange(e.target.value)}
                    />
                  </div>
                  <div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">المحور Y</span>
                    <input
                      type="number"
                      className="num-input"
                      value={posY}
                      onChange={e => handlePosYChange(e.target.value)}
                    />
                  </div>

                  <div className="sep" />
                  <div className="panel-title">الزوايا والميول</div>
                  
                  <div className="control-row">
                    <span className="control-label">زاوية الدوران</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input
                        type="range" className="range-slider"
                        min="-180" max="180" value={angle}
                        onChange={e => handleAngleChange(e.target.value)}
                      />
                      <span className="control-value" style={{ minWidth: '35px' }}>{angle}°</span>
                    </div>
                  </div>

                  <div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">الميلان (Skew)</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input
                        type="range" className="range-slider"
                        min="-89" max="89" value={skewX}
                        onChange={e => handleSkewXChange(e.target.value)}
                      />
                      <span className="control-value" style={{ minWidth: '35px' }}>{skewX}°</span>
                    </div>
                  </div>

                  <div className="sep" />
                  <div className="panel-title">محاذاة على اللوحة</div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                    {[
                      { label: 'توسيط أفقي', action: () => { if (!fabricCanvas || !activeObject) return; activeObject.set('left', (fabricCanvas.width - activeObject.getScaledWidth()) / 2); fabricCanvas.renderAll(); } },
                      { label: 'توسيط رأسي', action: () => { if (!fabricCanvas || !activeObject) return; activeObject.set('top', (fabricCanvas.height - activeObject.getScaledHeight()) / 2); fabricCanvas.renderAll(); } },
                    ].map((a) => (
                      <button key={a.label} className="btn btn-ghost btn-sm" onClick={a.action} style={{ fontSize: '0.72rem' }}>
                        {a.label}
                      </button>
                    ))}
                  </div>

                  <div className="sep" />
                  <div className="panel-title">ترتيب الطبقات</div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                    {[
                      { label: 'للأمام', action: () => { fabricCanvas?.bringObjectForward(activeObject); refreshLayers(fabricCanvas); } },
                      { label: 'للخلف', action: () => { fabricCanvas?.sendObjectBackwards(activeObject); refreshLayers(fabricCanvas); } },
                      { label: 'للأعلى', action: () => { fabricCanvas?.bringObjectToFront(activeObject); refreshLayers(fabricCanvas); } },
                      { label: 'للأسفل', action: () => { fabricCanvas?.sendObjectToBack(activeObject); refreshLayers(fabricCanvas); } },
                    ].map((a) => (
                      <button key={a.label} className="btn btn-ghost btn-sm" onClick={a.action} style={{ fontSize: '0.72rem' }}>
                        {a.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Canvas background (always shown) */}
              <div className="panel-section">
                <div className="panel-title">خلفية اللوحة</div>
                <div className="color-swatch-row">
                  <div className="color-input-wrapper">
                    <input type="color" defaultValue="#ffffff" onChange={e => handleCanvasBg(e.target.value)} />
                  </div>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    {['#ffffff', '#0f1115', '#f8fafc', '#1e1b4b', '#0c4a6e'].map(c => (
                      <div
                        key={c}
                        onClick={() => handleCanvasBg(c)}
                        style={{
                          width: 22, height: 22, borderRadius: 4,
                          background: c, cursor: 'pointer',
                          border: '1px solid var(--border-2)',
                        }}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-panel">
              <MousePointer2 size={32} />
              <div>
                <div style={{ fontWeight: 600, marginBottom: '4px', color: 'var(--text-secondary)' }}>لا يوجد عنصر محدد</div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>اضغط على أي عنصر في اللوحة لعرض خصائصه</div>
              </div>
            </div>
          )}

          {/* Canvas bg is available even with no selection */}
          {!activeObject && (
            <div className="panel-section">
              <div className="panel-title">خلفية اللوحة</div>
              <div className="color-swatch-row">
                <div className="color-input-wrapper">
                  <input type="color" defaultValue="#ffffff" onChange={e => handleCanvasBg(e.target.value)} />
                </div>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  {['#ffffff', '#0f1115', '#f8fafc', '#1e1b4b', '#0c4a6e'].map(c => (
                    <div
                      key={c}
                      onClick={() => handleCanvasBg(c)}
                      style={{
                        width: 22, height: 22, borderRadius: 4,
                        background: c, cursor: 'pointer',
                        border: '1px solid var(--border-2)',
                      }}
                    />
                  ))}
                </div>
              </div>
            </div>
          )}
        </aside>
      </main>
    </div>
  );
}
