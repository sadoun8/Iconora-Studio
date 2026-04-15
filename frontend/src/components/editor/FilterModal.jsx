/* eslint-disable react-hooks/immutability */
import React from 'react';
import { X } from 'lucide-react';
import * as fabric from 'fabric';

export default function FilterModal({
  open,
  onClose,
  blurAmount, setBlurAmount,
  fabricCanvas,
  activeObject
}) {
  if (!open) return null;

  return (
    <div
      style={{
        position: 'fixed', inset: 0,
        background: 'rgba(0,0,0,0.65)',
        backdropFilter: 'blur(6px)',
        zIndex: 9999,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}
      onClick={onClose}
    >
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span>✨ فلاتر SVG للعنصر المحدد</span>
          <button className="modal-close" onClick={onClose}><X size={16} /></button>
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
          <button className="btn btn-primary btn-sm" onClick={onClose}>تطبيق وإغلاق</button>
        </div>
      </div>
    </div>
  );
}
