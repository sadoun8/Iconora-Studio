import {
  Download,
  FolderOpen,
  Maximize2,
  Redo2,
  Save,
  Settings2,
  Sparkles,
  Undo2,
  Wand2,
  ZoomIn, ZoomOut,
} from 'lucide-react';

/**
 * EditorTopbar
 *
 * Props:
 *  canUndo, canRedo, undo, redo
 *  zoom, changeZoom, resetZoom
 *  selectedCanvasLabel, sectionConfig, fabricCanvas, setCanvasSize
 *  snapEnabled, setSnapEnabled
 *  isAiEnabled, section, openAiWorkspace
 *  openSettingsModal
 *  openSaveProjectModal, loadProjectFromApi, importProjectFile, exportProjectFile
 *  exportIcoViaApi, exportSvg, exportPngViaApi
 */
export default function EditorTopbar({
  canUndo, canRedo, undo, redo,
  zoom, changeZoom, resetZoom,
  selectedCanvasLabel, sectionConfig, fabricCanvas, setCanvasSize,
  snapEnabled, setSnapEnabled,
  isAiEnabled, section, openAiWorkspace,
  openSettingsModal,
  openSaveProjectModal, loadProjectFromApi, importProjectFile, exportProjectFile,
  exportIcoViaApi, exportSvg, exportPngViaApi,
}) {
  return (
    <header className="topbar">
      <div className="topbar-brand">
        <div className="logo-icon"><Sparkles size={16} color="white" /></div>
        <span className="brand-name">Iconora <span className="brand-accent">Studio</span></span>
        <span className="badge">v3.0</span>
      </div>

      {/* Center controls */}
      <div className="topbar-center" style={{ gap: '6px' }}>
        <button className="history-btn" onClick={undo} disabled={!canUndo} title="تراجع Ctrl+Z"><Undo2 size={15} /></button>
        <button className="history-btn" onClick={redo} disabled={!canRedo} title="إعادة Ctrl+Y"><Redo2 size={15} /></button>
        <div className="sep-v" />
        <button className="history-btn" onClick={() => changeZoom(-10)} title="تصغير"><ZoomOut size={15} /></button>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', minWidth: '36px', textAlign: 'center' }}>{zoom}%</span>
        <button className="history-btn" onClick={() => changeZoom(10)} title="تكبير"><ZoomIn size={15} /></button>
        <button className="history-btn" onClick={resetZoom} title="إعادة الضبط"><Maximize2 size={14} /></button>
        <div className="sep-v" />
        <select
          className="styled-select"
          style={{ width: 'auto', padding: '5px 8px', fontSize: '0.78rem' }}
          value={selectedCanvasLabel}
          onChange={(e) => {
            const s = sectionConfig.sizes.find(x => x.label === e.target.value);
            if (s && fabricCanvas) {
              fabricCanvas.setDimensions({ width: s.w, height: s.h });
              fabricCanvas.requestRenderAll();
              setCanvasSize({ w: s.w, h: s.h });
            }
          }}
        >
          {sectionConfig.sizes.map(s => <option key={s.label}>{s.label}</option>)}
        </select>
        <label className="snap-toggle" title="محاذاة تلقائية">
          <input type="checkbox" checked={snapEnabled} onChange={e => setSnapEnabled(e.target.checked)} />
          <span>تجاذب</span>
        </label>
      </div>

      {/* Actions */}
      <div className="topbar-actions">
        <button
          className="btn btn-ghost btn-sm"
          onClick={openAiWorkspace}
          title="انتقل إلى مساحة عمل الذكاء الاصطناعي"
          style={{
            color: isAiEnabled ? 'var(--success)' : 'var(--danger)',
            borderColor: isAiEnabled ? 'rgba(34,197,94,0.25)' : 'rgba(239,68,68,0.25)',
          }}
        >
          <Wand2 size={14} /> {isAiEnabled ? 'AI On' : 'AI Off'}
        </button>
        <div className="sep-v" />
        <button className="btn btn-ghost btn-sm" onClick={openSettingsModal}><Settings2 size={14} /> إعدادات</button>
        <div className="sep-v" />
        <button className="btn btn-ghost btn-sm" onClick={openSaveProjectModal}><Save size={14} /> حفظ</button>
        <button className="btn btn-ghost btn-sm" onClick={loadProjectFromApi}><FolderOpen size={14} /> فتح</button>
        <button className="btn btn-ghost btn-sm" onClick={importProjectFile}><FolderOpen size={14} /> استيراد</button>
        <button className="btn btn-ghost btn-sm" onClick={exportProjectFile}><Download size={14} /> تصدير</button>
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
  );
}
