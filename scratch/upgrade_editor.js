const fs = require('fs');

let content = fs.readFileSync('frontend/src/App.jsx', 'utf8');

// 1. Add states
const stateTarget = "const [charSpacing, setCharSpacing] = useState(0);";
const stateAdd = `const [charSpacing, setCharSpacing] = useState(0);
  const [skewY, setSkewY] = useState(0);
  const [isLocked, setIsLocked] = useState(false);
  const [isDashed, setIsDashed] = useState(false);`;
content = content.replace(stateTarget, stateAdd);

// 2. Add to syncPropsFromObject
const syncTarget = "setSkewX(Math.round(obj.skewX || 0));";
const syncAdd = `setSkewX(Math.round(obj.skewX || 0));
    setSkewY(Math.round(obj.skewY || 0));
    setIsLocked(obj.lockMovementX === true);
    setIsDashed(!!(obj.strokeDashArray && obj.strokeDashArray.length > 0));`;
content = content.replace(syncTarget, syncAdd);

// 3. Add Handlers
const handlerTarget = "const handleSkewXChange = (val) => { const n = Number(val); setSkewX(n); applyProp('skewX', n); };";
const handlerAdd = `const handleSkewXChange = (val) => { const n = Number(val); setSkewX(n); applyProp('skewX', n); };
  const handleSkewYChange = (val) => { const n = Number(val); setSkewY(n); applyProp('skewY', n); };

  const toggleLock = () => {
    if (!fabricCanvas || !activeObject) return;
    const locked = !isLocked;
    activeObject.set({
      lockMovementX: locked, lockMovementY: locked,
      lockRotation: locked, lockScalingX: locked, lockScalingY: locked,
      hasControls: !locked
    });
    setIsLocked(locked);
    fabricCanvas.requestRenderAll();
  };

  const toggleDashed = () => {
    if (!fabricCanvas || !activeObject) return;
    const dashed = !isDashed;
    activeObject.set('strokeDashArray', dashed ? [10, 5] : null);
    setIsDashed(dashed);
    fabricCanvas.requestRenderAll();
  };

  const handleGroup = () => {
    if (!fabricCanvas || !activeObject) return;
    if (activeObject.type === 'activeSelection') {
      const group = activeObject.toGroup();
      fabricCanvas.requestRenderAll();
      setActiveObject(group);
    }
  };

  const handleUngroup = () => {
    if (!fabricCanvas || !activeObject) return;
    if (activeObject.type === 'group') {
      const sel = activeObject.toActiveSelection();
      fabricCanvas.requestRenderAll();
      setActiveObject(sel);
    }
  };`;
content = content.replace(handlerTarget, handlerAdd);

// 4. Update UI in style tab
// Replace the delete duplicate buttons
const uiGroupTarget = `<div className="sep" />
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button className="btn btn-ghost btn-sm" style={{ flex: 1 }} onClick={duplicateSelected}><Copy size={13} /> تكرار</button>
                    <button className="btn btn-danger btn-sm" onClick={deleteSelected}><Trash2 size={13} /></button>
                  </div>`;
const uiGroupAdd = `<div className="sep" />
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                    <button className={\`btn \${isLocked ? 'btn-primary' : 'btn-ghost'} btn-sm\`} onClick={toggleLock}>
                      🔒 {isLocked ? 'مقفول' : 'قفل'}
                    </button>
                    <button className="btn btn-ghost btn-sm" onClick={duplicateSelected}>
                      <Copy size={13} style={{display:'inline', verticalAlign:'middle'}} /> تكرار
                    </button>
                    {activeObject.type === 'activeSelection' && (
                      <button className="btn btn-primary btn-sm" onClick={handleGroup}>
                        📦 تجميع
                      </button>
                    )}
                    {activeObject.type === 'group' && (
                      <button className="btn btn-ghost btn-sm" onClick={handleUngroup} style={{border: '1px solid var(--primary)'}}>
                        📦 فك التجميع
                      </button>
                    )}
                  </div>
                  <div style={{ display: 'flex', marginTop: '6px' }}>
                    <button className="btn btn-danger btn-sm" style={{ width: '100%' }} onClick={deleteSelected}><Trash2 size={13} style={{display:'inline', verticalAlign:'middle'}} /> حذف</button>
                  </div>`;

// 5. Update UI in stroke section
const strokeTarget = `<span className="control-value">{strokeWidth}px</span>
                        </div>
                      </div>
                      <div className="sep" />`;
const strokeAdd = `<span className="control-value">{strokeWidth}px</span>
                        </div>
                      </div>
                      <div className="control-row" style={{ marginTop: '8px' }}>
                        <span className="control-label">تأثير</span>
                        <label className="snap-toggle" style={{width: 'auto'}}>
                          <input type="checkbox" checked={isDashed} onChange={toggleDashed} />
                          <span>خط متقطع</span>
                        </label>
                      </div>
                      <div className="sep" />`;

// 6. Update UI in position (Skew Y)
const skewYTarget = `<span className="control-value" style={{ minWidth: '35px' }}>{skewX}°</span>
                    </div>
                  </div>`;
const skewYAdd = `<span className="control-value" style={{ minWidth: '35px' }}>{skewX}°</span>
                    </div>
                  </div>
                  <div className="control-row" style={{ marginTop: '8px' }}>
                    <span className="control-label">ميلان رأسي</span>
                    <div className="range-row" style={{ flex: 1 }}>
                      <input type="range" className="range-slider" min="-89" max="89" value={skewY} onChange={e => handleSkewYChange(e.target.value)} />
                      <span className="control-value" style={{ minWidth: '35px' }}>{skewY}°</span>
                    </div>
                  </div>`;

content = content.replace(uiGroupTarget, uiGroupAdd);
content = content.replace(strokeTarget, strokeAdd);
content = content.replace(skewYTarget, skewYAdd);

fs.writeFileSync('frontend/src/App.jsx', content, 'utf8');
console.log("Successfully upgraded editor!");
