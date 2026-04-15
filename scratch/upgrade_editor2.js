const fs = require('fs');
let content = fs.readFileSync('frontend/src/App.jsx', 'utf8');

// The handlers and states are already there. We just need to inject the JSX in the correct places.

// 1. Group / Ungroup / Lock / Duplicate
const duplicateIdx = content.indexOf('<button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={duplicateSelected}><Copy size={13} /> تكرار</button>');
if (duplicateIdx > -1) {
    const parentStart = content.lastIndexOf('<div style={{ display: \\'flex\\', gap: \\'6px\\' }}>', duplicateIdx);
    const parentEnd = content.indexOf('</div>', duplicateIdx) + 6;
    
    if (parentStart > -1 && parentEnd > -1) {
        const replacement = `<div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                    <button className={\`btn \${isLocked ? 'btn-primary' : 'btn-ghost'} btn-sm\`} onClick={toggleLock}>
                      {isLocked ? 'مقفول 🔒' : 'قفل 🔓'}
                    </button>
                    <button className="btn btn-ghost btn-sm" onClick={duplicateSelected}><Copy size={13} style={{display:'inline', marginBottom:'-2px'}} /> تكرار</button>
                    {activeObject.type === 'activeSelection' && (
                      <button className="btn btn-primary btn-sm" onClick={handleGroup}>📦 تجميع</button>
                    )}
                    {activeObject.type === 'group' && (
                      <button className="btn btn-ghost btn-sm" style={{border: '1px solid var(--primary)'}} onClick={handleUngroup}>📦 فك التجميع</button>
                    )}
                  </div>
                  <div style={{ display: 'flex', marginTop: '6px' }}>
                    <button className="btn btn-danger btn-sm" onClick={deleteSelected} style={{width:'100%'}}><Trash2 size={13} style={{display:'inline', marginBottom:'-2px'}} /> حذف</button>
                  </div>`;
        content = content.slice(0, parentStart) + replacement + content.slice(parentEnd);
    }
}

// 2. Stroke dashed effect
const strokeIdx = content.indexOf('<span className="control-value">{strokeWidth}px</span>');
if (strokeIdx > -1) {
    const sectionEnd = content.indexOf('</div>\n                      </div>\n                      <div className="sep" />', strokeIdx);
    if (sectionEnd > -1) {
         // insert after the range-row closes
         const insertPoint = sectionEnd + '</div>\n                      </div>'.length;
         const add = `\n                      <div className="control-row" style={{ marginTop: '8px' }}>
                        <span className="control-label">تأثير الحد</span>
                        <label className="snap-toggle" style={{width: 'auto'}}>
                          <input type="checkbox" checked={isDashed} onChange={toggleDashed} />
                          <span>خط متقطع</span>
                        </label>
                      </div>`;
         content = content.slice(0, insertPoint) + add + content.slice(insertPoint);
    } else {
        const sectionEndFallback = content.indexOf('</div>\\r\\n                      </div>\\r\\n                      <div className="sep" />', strokeIdx);
        if(sectionEndFallback > -1) {
             const insertPoint = sectionEndFallback + '</div>\\r\\n                      </div>'.length;
             const add = `\\r\\n                      <div className="control-row" style={{ marginTop: '8px' }}>\\r\\n                        <span className="control-label">تأثير الحد</span>\\r\\n                        <label className="snap-toggle" style={{width: 'auto'}}>\\r\\n                          <input type="checkbox" checked={isDashed} onChange={toggleDashed} />\\r\\n                          <span>خط متقطع</span>\\r\\n                        </label>\\r\\n                      </div>`;
             content = content.slice(0, insertPoint) + add + content.slice(insertPoint);
        }
    }
}

// 3. Skew Y
const skewXIdx = content.indexOf('onChange={e => handleSkewXChange(e.target.value)} />');
if (skewXIdx > -1) {
    const endSkewXRow = content.indexOf('</div>', skewXIdx) + 6;
    const finalEnd = content.indexOf('</div>', endSkewXRow) + 6;
    if (finalEnd > -1) {
        const add = `\n                  <div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">ميلان رأسي</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="-89" max="89" value={skewY} onChange={e => handleSkewYChange(e.target.value)} />
                      <span className="control-value" style={{ minWidth: '35px' }}>{skewY}°</span>
                    </div>
                  </div>`;
        content = content.slice(0, finalEnd) + add + content.slice(finalEnd);
    }
}

fs.writeFileSync('frontend/src/App.jsx', content, 'utf8');
console.log("Upgrades applied to UI successfully!");
