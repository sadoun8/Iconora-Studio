const fs = require('fs');
const path = require('path');

const targetPath = path.resolve('frontend/src/App.jsx');
let content = fs.readFileSync(targetPath, 'utf8');

// Replace imports
content = content.replace(
  "import ToolsSidebarPanel from './components/editor/ToolsSidebarPanel.jsx';",
  "import ToolsSidebarPanel from './components/editor/ToolsSidebarPanel.jsx';\nimport CurvedTextModal from './components/editor/CurvedTextModal.jsx';\nimport FilterModal from './components/editor/FilterModal.jsx';"
);

// We need to replace everything from {/* ====== CURVED TEXT MODAL ====== */} down to the end of the showFilterModal JSX block.
// The SVG FILTER MODAL ends with:
//         </div>
//       )}
//     </div>
//   );
// }

const startToken = "{/* ====== CURVED TEXT MODAL ====== */}";
const endToken = "{/* ====== SVG FILTER MODAL ====== */}";

const startIndex = content.indexOf(startToken);
if (startIndex === -1) throw new Error("Could not find start token");

// Find where SVG Filter modal ends
const filterIndex = content.indexOf(endToken);
if (filterIndex === -1) throw new Error("Could not find end token for Filter modal");

// Let's find the closing tag corresponding to showFilterModal
const lastDivIndex = content.indexOf("    </div>\n  );\n}");
if (lastDivIndex === -1) {
    const lastDivIndexFallback = content.indexOf("    </div>\r\n  );\r\n}");
    if(lastDivIndexFallback === -1) throw new Error("Could not find closing of the component");
}

let afterModalIndex = content.indexOf("    </div>\n  );\n}", filterIndex);
if (afterModalIndex === -1) {
    afterModalIndex = content.indexOf("    </div>\r\n  );\r\n}", filterIndex);
}

const newModals = `      <CurvedTextModal
        open={showCurvedTextModal}
        onClose={() => { setShowCurvedTextModal(false); setEditingCurvedId(null); }}
        editingCurvedId={editingCurvedId}
        curvedTextValue={curvedTextValue} setCurvedTextValue={setCurvedTextValue}
        curvedTextFont={curvedTextFont} setCurvedTextFont={setCurvedTextFont}
        curvedTextSize={curvedTextSize} setCurvedTextSize={setCurvedTextSize}
        curvedTextRadius={curvedTextRadius} setCurvedTextRadius={setCurvedTextRadius}
        curvedTextStartAngle={curvedTextStartAngle} setCurvedTextStartAngle={setCurvedTextStartAngle}
        curvedTextColor={curvedTextColor} setCurvedTextColor={setCurvedTextColor}
        sectionConfig={sectionConfig}
        commitCurvedText={commitCurvedText}
      />

      <FilterModal
        open={showFilterModal}
        onClose={() => setShowFilterModal(false)}
        blurAmount={blurAmount} setBlurAmount={setBlurAmount}
        fabricCanvas={fabricCanvas}
        activeObject={activeObject}
      />\n`;

content = content.slice(0, startIndex) + newModals + content.slice(afterModalIndex);

fs.writeFileSync(targetPath, content, 'utf8');
console.log("Success");
