const fs = require('fs');
let content = fs.readFileSync('frontend/src/App.jsx', 'utf8');

const regex = /const handleItalicToggle = \(\) => \{ const next = !isItalic; setIsItalic\(next\); applyProp\('fontStyle', next \? 'italic' : 'normal'\); \};/g;

content = content.replace(regex, `const handleItalicToggle = () => { const next = !isItalic; setIsItalic(next); applyProp('fontStyle', next ? 'italic' : 'normal'); };
  const handleUnderlineToggle = () => { const next = !isUnderline; setIsUnderline(next); applyProp('underline', next); };
  const handleLinethroughToggle = () => { const next = !isLinethrough; setIsLinethrough(next); applyProp('linethrough', next); };`);

fs.writeFileSync('frontend/src/App.jsx', content, 'utf8');
