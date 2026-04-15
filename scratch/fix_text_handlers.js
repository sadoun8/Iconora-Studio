const fs = require('fs');
let content = fs.readFileSync('frontend/src/App.jsx', 'utf8');

const anchor = "const handleItalicToggle = () => { const next = !isItalic; setIsItalic(next); applyProp('fontStyle', next ? 'italic' : 'normal'); };";
if (content.includes(anchor) && !content.includes('handleUnderlineToggle')) {
    const replacement = anchor + "\n  const handleUnderlineToggle = () => { const next = !isUnderline; setIsUnderline(next); applyProp('underline', next); };\n  const handleLinethroughToggle = () => { const next = !isLinethrough; setIsLinethrough(next); applyProp('linethrough', next); };";
    content = content.replace(anchor, replacement);
    fs.writeFileSync('frontend/src/App.jsx', content, 'utf8');
}
