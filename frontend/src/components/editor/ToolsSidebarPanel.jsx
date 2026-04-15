import {
  AlignCenter,
  Circle,
  FlipHorizontal,
  FlipVertical,
  Hexagon,
  Image as ImageIcon,
  MousePointer2,
  Pen,
  RefreshCw,
  Sliders,
  Square,
  Star,
  Type,
} from 'lucide-react';

const DRAW_SWATCHES = ['#0f1115', '#ffffff', '#6366f1', '#f59e0b', '#ec4899', '#22c55e', '#c9a227', '#ef4444'];

export default function ToolsSidebarPanel({
  activeTool,
  activateSelectTool,
  section,
  setActiveTool,
  drawColor,
  setDrawColor,
  drawSize,
  setDrawSize,
  onRefreshDrawingBrush,
  addText,
  addRect,
  addCircle,
  addPolygon,
  addStar,
  loadImage,
  addCurvedText,
  applyGoldGradient,
  applySilverGradient,
  applyPurpleGradient,
  toggleFlipX,
  toggleFlipY,
  onOpenFilters,
}) {
  return (
    <>
      <div className="sidebar-section">
        <div className="section-label">وضع التحرير</div>
        <div className="tool-grid">
          <button className={`tool-btn ${activeTool === 'select' ? 'active' : ''}`} onClick={activateSelectTool}>
            <MousePointer2 size={17} /> تحديد
          </button>
          {section === 'signature' && (
            <button className={`tool-btn ${activeTool === 'draw' ? 'active' : ''}`} onClick={() => setActiveTool('draw')}>
              <Pen size={17} /> فرشاة
            </button>
          )}
        </div>
      </div>

      {section === 'signature' && activeTool === 'draw' && (
        <div className="sidebar-section">
          <div className="section-label">إعدادات الريشة</div>
          <div className="control-row">
            <span className="control-label">اللون</span>
            <div className="color-input-wrapper" style={{ width: 28, height: 28 }}>
              <input type="color" value={drawColor} onChange={(event) => setDrawColor(event.target.value)} />
            </div>
          </div>
          <div className="control-row">
            <span className="control-label">السماكة</span>
            <div className="range-row" style={{ flex: 1 }}>
              <input
                type="range"
                className="range-slider"
                min="1"
                max="30"
                value={drawSize}
                onChange={(event) => setDrawSize(Number(event.target.value))}
              />
              <span className="control-value">{drawSize}px</span>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap', marginTop: '6px' }}>
            {DRAW_SWATCHES.map((color) => (
              <div
                key={color}
                onClick={() => setDrawColor(color)}
                style={{
                  width: 22,
                  height: 22,
                  borderRadius: 4,
                  background: color,
                  cursor: 'pointer',
                  border: drawColor === color ? '2px solid var(--primary)' : '1px solid var(--border-2)',
                  flexShrink: 0,
                }}
              />
            ))}
          </div>
          <button
            className="btn btn-ghost btn-sm"
            style={{ width: '100%', marginTop: '8px' }}
            onClick={onRefreshDrawingBrush}
          >
            <RefreshCw size={13} /> مسح الريشة
          </button>
        </div>
      )}

      <div className="sidebar-section">
        <div className="section-label">إضافة عناصر</div>
        <div className="tool-grid">
          <button className="tool-btn" onClick={addText}><Type size={17} /> نص</button>
          <button className="tool-btn" onClick={addRect}><Square size={17} /> مستطيل</button>
          <button className="tool-btn" onClick={addCircle}><Circle size={17} /> دائرة</button>
          <button className="tool-btn" onClick={addPolygon}><Hexagon size={17} /> مضلع</button>
          <button className="tool-btn" onClick={addStar}><Star size={17} /> نجمة</button>
          <button className="tool-btn" onClick={loadImage}><ImageIcon size={17} /> صورة</button>
        </div>
      </div>

      <div className="sidebar-section">
        <div className="section-label">نص مقوس</div>
        <button className="btn btn-ghost btn-sm" style={{ width: '100%' }} onClick={addCurvedText}>
          <AlignCenter size={14} /> إضافة نص على قوس
        </button>
      </div>

      <div className="sidebar-section">
        <div className="section-label">تدرجات احترافية</div>
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          <button className="gradient-btn" style={{ background: 'linear-gradient(135deg,#bf953f,#fcf6ba,#b38728)' }} onClick={applyGoldGradient} title="ذهبي">ذهبي</button>
          <button className="gradient-btn" style={{ background: 'linear-gradient(135deg,#bdc3c7,#f8f8f8,#7f8c8d)' }} onClick={applySilverGradient} title="فضي">فضي</button>
          <button className="gradient-btn" style={{ background: 'linear-gradient(135deg,#6366f1,#a855f7,#ec4899)' }} onClick={applyPurpleGradient} title="بنفسجي">إبداعي</button>
        </div>
      </div>

      <div className="sidebar-section">
        <div className="section-label">انعكاس</div>
        <div style={{ display: 'flex', gap: '6px' }}>
          <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={toggleFlipX}><FlipHorizontal size={14} /> أفقي</button>
          <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={toggleFlipY}><FlipVertical size={14} /> رأسي</button>
        </div>
      </div>

      <div className="sidebar-section">
        <div className="section-label">فلاتر SVG</div>
        <button className="btn btn-ghost btn-sm" style={{ width: '100%' }} onClick={onOpenFilters}>
          <Sliders size={14} /> إعدادات الفلاتر
        </button>
      </div>
    </>
  );
}
