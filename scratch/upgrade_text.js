const fs = require('fs');
let content = fs.readFileSync('frontend/src/App.jsx', 'utf8');

// 1. Add Gradients into the Style properties tab
const goldGradientFn = content.match(/const applyGoldGradient = \(\) => \{[\s\S]*?\};/);
let gradientButtons = ``;
if (goldGradientFn) {
    gradientButtons = `<div className="sep" />
                  <div className="panel-title">تدرجات احترافية (Gradients)</div>
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    <button className="btn btn-ghost btn-sm" onClick={applyGoldGradient} style={{ background: 'linear-gradient(45deg, #bf953f, #fcf6ba, #aa771c)', color: '#000', fontWeight: 'bold', border: 'none', flex: 1 }}>ذهبي ✨</button>
                    <button className="btn btn-ghost btn-sm" onClick={applySilverGradient} style={{ background: 'linear-gradient(45deg, #bdc3c7, #f8f8f8, #7f8c8d)', color: '#000', fontWeight: 'bold', border: 'none', flex: 1 }}>فضي 💿</button>
                    <button className="btn btn-ghost btn-sm" onClick={applyPurpleGradient} style={{ background: 'linear-gradient(45deg, #a8c0ff, #3f2b96)', color: '#fff', fontWeight: 'bold', border: 'none', flex: 1 }}>ليلي 🌌</button>
                  </div>`;
}

// Locate where to insert gradients in Style Tab (after shadowBlur control row)
const shadowRegex = /<input type="range" className="range-slider" min="0" max="40" value=\{shadowBlur\} onChange=\{e => handleShadowChange\(e\.target\.value\)\} \/>\s*<span className="control-value">\{shadowBlur\}px<\/span>\s*<\/div>\s*<\/div>/;
const matchShadow = content.match(shadowRegex);
if(matchShadow) {
    const insertPoint = matchShadow.index + matchShadow[0].length;
    content = content.slice(0, insertPoint) + '\\n' + gradientButtons + content.slice(insertPoint);
}

// 2. Add text styles (Underline / Linethrough) & State syncing
const syncTarget = "setIsItalic(obj.fontStyle === 'italic');";
const syncAdd = `setIsItalic(obj.fontStyle === 'italic');\n      setIsUnderline(obj.underline || false);\n      setIsLinethrough(obj.linethrough || false);`;
content = content.replace(syncTarget, syncAdd);

const stateTarget = "const [isItalic, setIsItalic] = useState(false);";
const stateAdd = `const [isItalic, setIsItalic] = useState(false);\n  const [isUnderline, setIsUnderline] = useState(false);\n  const [isLinethrough, setIsLinethrough] = useState(false);`;
content = content.replace(stateTarget, stateAdd);

const handlerTarget = "const handleItalicToggle = () => { const v = !isItalic; setIsItalic(v); applyProp('fontStyle', v ? 'italic' : 'normal'); };";
const handlerAdd = `const handleItalicToggle = () => { const v = !isItalic; setIsItalic(v); applyProp('fontStyle', v ? 'italic' : 'normal'); };\n  const handleUnderlineToggle = () => { const v = !isUnderline; setIsUnderline(v); applyProp('underline', v); };\n  const handleLinethroughToggle = () => { const v = !isLinethrough; setIsLinethrough(v); applyProp('linethrough', v); };`;
content = content.replace(handlerTarget, handlerAdd);

const textButtonsRegex = /<button className=\{\`btn btn-ghost btn-sm \$\{isItalic \? 'prop-active' : ''\}\`\} onClick=\{handleItalicToggle\}><Italic size=\{13\} \/><\/button>/;
const textButtonsMatch = content.match(textButtonsRegex);
if(textButtonsMatch) {
    const insertPt = textButtonsMatch.index + textButtonsMatch[0].length;
    const addHTML = `\n                    <button className={\`btn btn-ghost btn-sm \${isUnderline ? 'prop-active' : ''}\`} onClick={handleUnderlineToggle} style={{textDecoration: 'underline'}}>U</button>\n                    <button className={\`btn btn-ghost btn-sm \${isLinethrough ? 'prop-active' : ''}\`} onClick={handleLinethroughToggle} style={{textDecoration: 'line-through'}}>S</button>`;
    content = content.slice(0, insertPt) + addHTML + content.slice(insertPt);
}

fs.writeFileSync('frontend/src/App.jsx', content, 'utf8');
console.log("Text tools & Gradients upgraded!");
