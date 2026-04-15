const fs = require('fs');

// 1. Update ai_models.py
let modelsContent = fs.readFileSync('backend/schemas/ai_models.py', 'utf8');
modelsContent = modelsContent.replace('    remove_background: bool = True', '    remove_background: bool = True\n    seed: int | None = None');
modelsContent = modelsContent.replace('    image_data: str', '    image_data: str\n    seed: int | None = None');
fs.writeFileSync('backend/schemas/ai_models.py', modelsContent, 'utf8');

// 2. Update routes_ai.py
let routesContent = fs.readFileSync('backend/api/routes_ai.py', 'utf8');
routesContent = routesContent.replace(
    'seed = random.randint(1, 1000000)',
    'seed = req.seed if req.seed else random.randint(1, 1000000000)'
);
routesContent = routesContent.replace(
    '?width=512&height=512&nologo=true&model=flux&seed={seed}',
    '?width=1024&height=1024&nologo=true&enhance=true&model=flux&seed={seed}'
);
routesContent = routesContent.replace(
    'return {"image_data": f"data:image/png;base64,{base64_img}"}',
    'return {"image_data": f"data:image/png;base64,{base64_img}", "seed": seed}'
);
fs.writeFileSync('backend/api/routes_ai.py', routesContent, 'utf8');

// 3. Update AiSidebarPanel.jsx
let sidebarContent = fs.readFileSync('frontend/src/components/editor/AiSidebarPanel.jsx', 'utf8');

// Update Ctrl+Enter
sidebarContent = sidebarContent.replace('onGenerate();', 'onGenerate(false);');

// Update buttons
const btnRegex = /<button[\s\S]*?onClick=\{onGenerate\}[\s\S]*?<\/button>/g;
sidebarContent = sidebarContent.replace(btnRegex, `<div style={{ display: 'grid', gridTemplateColumns: '1fr 60px', gap: '6px' }}>
          <button
            className={\`btn btn-primary \${isGenerating ? 'generating-indicator' : ''}\`}
            onClick={() => onGenerate(false)}
            disabled={!isAiEnabled || isGenerating || !aiPrompt.trim()}
          >
            {isGenerating ? <><Loader2 size={15} className="animate-spin" /> ...</> : <><Wand2 size={15} /> تعديل / دمج</>}
          </button>
          <button
            className="btn btn-ghost"
            style={{ padding: '0', border: '1px solid var(--border-2)' }}
            onClick={() => onGenerate(true)}
            disabled={!isAiEnabled || isGenerating || !aiPrompt.trim()}
            title="توليد شعار جديد بالكامل"
          >
            جديد ✨
          </button>
        </div>`);
fs.writeFileSync('frontend/src/components/editor/AiSidebarPanel.jsx', sidebarContent, 'utf8');

// 4. Update App.jsx
let appContent = fs.readFileSync('frontend/src/App.jsx', 'utf8');

const stateTarget = `const [aiError, setAiError] = useState('');`;
appContent = appContent.replace(stateTarget, `const [aiError, setAiError] = useState('');\n  const [aiSeed, setAiSeed] = useState(null);`);

const genRegex = /const handleGenerateLogoViaApi = async \(\) => {[\s\S]*?setIsGenerating\(false\); \}\s*\n\s*\};/;
appContent = appContent.replace(genRegex, `const handleGenerateLogoViaApi = async (isNew = false) => {
    if (!isAiEnabled || !aiPrompt.trim() || !fabricCanvas) return;
    setIsGenerating(true); setAiError('');
    try {
      let currentSeed = aiSeed;
      if (isNew || !currentSeed) {
         currentSeed = Math.floor(Math.random() * 1000000000);
         setAiSeed(currentSeed);
      }
      const data = await generateLogo({ prompt: aiPrompt, remove_background: true, seed: currentSeed });
      placeGeneratedImage(data.image_data);
    } catch {
      setAiError('تعذر توليد الشعار! ربما حدث خطأ في الخادم.');
    } finally { setIsGenerating(false); }
  };`);

fs.writeFileSync('frontend/src/App.jsx', appContent, 'utf8');
console.log("AI upgraded!");
