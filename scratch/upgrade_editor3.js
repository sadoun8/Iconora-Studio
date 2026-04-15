const fs = require('fs');
let content = fs.readFileSync('frontend/src/App.jsx', 'utf8');

// 1. Group / Ungroup
const buttonRegex = /<div style={{ display: 'flex', gap: '6px' }}>\s*<button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={duplicateSelected}><Copy size=\{13\} \/> تكرار<\/button>\s*<button className="btn btn-danger btn-sm" onClick=\{deleteSelected\}><Trash2 size=\{13\} \/><\/button>\s*<\/div>/g;

content = content.replace(buttonRegex, `<div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
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
                  </div>`);

// 2. Stroke dashed effect
const strokeRegex = /<span className="control-value">\{strokeWidth\}px<\/span>\s*<\/div>\s*<\/div>/g;
content = content.replace(strokeRegex, `<span className="control-value">{strokeWidth}px</span>
                        </div>
                      </div>
                      <div className="control-row" style={{ marginTop: '8px' }}>
                        <span className="control-label">تأثير الحد</span>
                        <label className="snap-toggle" style={{width: 'auto'}}>
                          <input type="checkbox" checked={isDashed} onChange={toggleDashed} />
                          <span>متقطع</span>
                        </label>
                      </div>`);

// 3. Skew Y
const skewXRegex = /<div className="control-row" style={{ marginTop: '8px' }}>\s*<span className="control-label">ميلان<\/span>\s*<div className="range-row" style={{ flex: 1 }}>\s*<input type="range" className="range-slider" min="-89" max="89" value=\{skewX\} onChange=\{e => handleSkewXChange\(e\.target\.value\)\} \/>\s*<span className="control-value" style={{ minWidth: '35px' }}>\{skewX\}°<\/span>\s*<\/div>\s*<\/div>/g;

content = content.replace(skewXRegex, `<div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">ميلان أفقي</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="-89" max="89" value={skewX} onChange={e => handleSkewXChange(e.target.value)} />
                      <span className="control-value" style={{ minWidth: '35px' }}>{skewX}°</span>
                    </div>
                  </div>
                  <div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">ميلان رأسي</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="-89" max="89" value={skewY} onChange={e => handleSkewYChange(e.target.value)} />
                      <span className="control-value" style={{ minWidth: '35px' }}>{skewY}°</span>
                    </div>
                  </div>`);

fs.writeFileSync('frontend/src/App.jsx', content, 'utf8');
console.log("Upgrades 3 applied via regex successfully!");
