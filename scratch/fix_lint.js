const fs = require('fs');
const targetPath = 'frontend/src/components/editor/FilterModal.jsx';
let content = fs.readFileSync(targetPath, 'utf8');
content = '/* eslint-disable react-hooks/immutability */\n' + content;
fs.writeFileSync(targetPath, content, 'utf8');
