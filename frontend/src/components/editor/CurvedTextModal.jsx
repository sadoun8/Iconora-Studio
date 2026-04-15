import React from 'react';
import { X } from 'lucide-react';

// Gradient presets for curved text
const CURVED_GRADIENTS = [
  { label: 'ذهبي ✨', stops: ['#bf953f', '#fcf6ba', '#aa771c'], bg: 'linear-gradient(135deg,#bf953f,#fcf6ba,#b38728)', textColor: '#7a5c0a' },
  { label: 'فضي 💿', stops: ['#bdc3c7', '#f8f8f8', '#7f8c8d'], bg: 'linear-gradient(135deg,#bdc3c7,#f8f8f8,#7f8c8d)', textColor: '#444' },
  { label: 'ليلي 🌌', stops: ['#6366f1', '#a855f7', '#ec4899'], bg: 'linear-gradient(135deg,#6366f1,#a855f7,#ec4899)', textColor: '#fff' },
];

export default function CurvedTextModal({
  open,
  onClose,
  editingCurvedId,
  curvedTextValue, setCurvedTextValue,
  curvedTextFont, setCurvedTextFont,
  curvedTextSize, setCurvedTextSize,
  curvedTextRadius, setCurvedTextRadius,
  curvedTextStartAngle, setCurvedTextStartAngle,
  curvedTextColor, setCurvedTextColor,
  sectionConfig,
  commitCurvedText
}) {
  if (!open) return null;

  return (
    // Transparent pointer-events-none backdrop — does NOT block canvas clicks
    <div
      style={{
        position: 'fixed', inset: 0,
        zIndex: 9998,
        pointerEvents: 'none',
      }}
    >
      {/* Actual panel — pointer-events restored only on the panel itself */}
      <div
        onClick={e => e.stopPropagation()}
        style={{
          position: 'absolute',
          top: '80px',
          left: '16px',
          width: '300px',
          maxHeight: 'calc(100vh - 100px)',
          overflowY: 'auto',
          background: 'var(--bg-panel)',
          border: '1px solid var(--border-1)',
          borderRadius: '14px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.45)',
          pointerEvents: 'auto',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Header */}
        <div className="modal-header" style={{ borderRadius: '14px 14px 0 0', padding: '10px 14px', cursor: 'default', flexShrink: 0 }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>
            {editingCurvedId ? '✏ تعديل النص المقوس' : '🔄 نص مقوس على قوس'}
          </span>
          <button className="modal-close" onClick={onClose}><X size={14} /></button>
        </div>

        {/* Body */}
        <div className="modal-body" style={{ padding: '12px 14px', overflowY: 'auto' }}>

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

          {/* Color row */}
          <div className="modal-field">
            <label>اللون</label>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '8px' }}>
              <div className="color-input-wrapper">
                <input type="color" value={curvedTextColor} onChange={e => setCurvedTextColor(e.target.value)} />
              </div>
              <input className="color-hex" value={curvedTextColor}
                onChange={e => setCurvedTextColor(e.target.value)} maxLength={7} />
            </div>
            {/* Quick swatches */}
            <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap', marginBottom: '8px' }}>
              {['#ffffff','#0f1115','#6366f1','#f59e0b','#ec4899','#22c55e','#ef4444','#14b8a6'].map(c => (
                <div key={c} onClick={() => setCurvedTextColor(c)}
                  style={{ width: 20, height: 20, borderRadius: 4, background: c, cursor: 'pointer',
                    border: curvedTextColor === c ? '2px solid var(--primary)' : '1px solid var(--border-2)', flexShrink: 0 }} />
              ))}
            </div>
            {/* Gradient presets */}
            <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
              {CURVED_GRADIENTS.map(g => (
                <button key={g.label}
                  onClick={() => setCurvedTextColor(g.stops[0])}
                  style={{
                    background: g.bg, color: g.textColor, border: 'none',
                    borderRadius: 6, padding: '3px 8px', fontSize: '0.7rem',
                    fontWeight: 700, cursor: 'pointer', flex: 1,
                    boxShadow: '0 1px 4px rgba(0,0,0,0.3)'
                  }}>{g.label}</button>
              ))}
            </div>
          </div>

          {/* Live SVG Preview */}
          <div style={{ background: 'var(--bg-active)', borderRadius: '8px', padding: '8px', textAlign: 'center',
            minHeight: '100px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: '8px' }}>
            {curvedTextValue ? (
              <svg width="100%" height="120" viewBox="-150 -150 300 300" overflow="visible" style={{ maxWidth: '100%' }}>
                <defs>
                  <path id="modal-prev-arc" d={(() => {
                    const r = curvedTextRadius;
                    const a1 = (curvedTextStartAngle * Math.PI) / 180;
                    const isBottom = curvedTextStartAngle > 0 && curvedTextStartAngle < 180;
                    const sweep = isBottom ? 0 : 1;
                    const a2 = a1 + (179 * Math.PI / 180);
                    return `M ${r * Math.cos(a1)} ${r * Math.sin(a1)} A ${r} ${r} 0 0 ${sweep} ${r * Math.cos(a2)} ${r * Math.sin(a2)}`;
                  })()} />
                </defs>
                <circle cx="0" cy="0" r={curvedTextRadius} fill="none" stroke="rgba(99,102,241,0.15)" strokeWidth="1" strokeDasharray="4 3" />
                <text fontFamily={curvedTextFont} fontSize={curvedTextSize} fill={curvedTextColor}
                  textAnchor="middle" direction="rtl">
                  <textPath href="#modal-prev-arc" startOffset="50%">{curvedTextValue}</textPath>
                </text>
              </svg>
            ) : (
              <span style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>أدخل النص للمعاينة</span>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="modal-footer" style={{ borderRadius: '0 0 14px 14px', padding: '10px 14px', flexShrink: 0 }}>
          <button className="btn btn-ghost btn-sm" onClick={onClose}>إلغاء</button>
          <button className="btn btn-primary btn-sm" onClick={commitCurvedText}>
            {editingCurvedId ? '✦ تحديث' : '✦ إضافة للوحة'}
          </button>
        </div>
      </div>
    </div>
  );
}
