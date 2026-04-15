import sys

filepath = r'frontend\src\App.jsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ---------------------------------------------------------------
# FIX 1: Replace placeGeneratedImage (simple, no seed/section support)
# ---------------------------------------------------------------
OLD1 = (
    "  const placeGeneratedImage = useCallback((imageDataUrl) => {\n"
    "    if (!fabricCanvas || !imageDataUrl) return;\n"
    "    const imgEl = new window.Image();\n"
    "    imgEl.src = imageDataUrl;\n"
    "    imgEl.onload = () => {\n"
    "      const fImg = new fabric.FabricImage(imgEl);\n"
    "      if (fImg.width > fabricCanvas.width * 0.5) fImg.scaleToWidth(fabricCanvas.width * 0.5);\n"
    "      fImg.set({ left: (fabricCanvas.width - fImg.getScaledWidth()) / 2, top: (fabricCanvas.height - fImg.getScaledHeight()) / 2 });\n"
    "      fabricCanvas.add(fImg);\n"
    "      fabricCanvas.setActiveObject(fImg);\n"
    "      fabricCanvas.renderAll();\n"
    "      setAiPrompt('');\n"
    "    };\n"
    "  }, [fabricCanvas]);"
)

NEW1 = (
    "  // Tracks the last AI-generated image so edit/merge mode can replace it\n"
    "  const lastAiImageRef = React.useRef(null);\n"
    "\n"
    "  const placeGeneratedImage = useCallback((imageDataUrl, replaceExisting = false) => {\n"
    "    if (!fabricCanvas || !imageDataUrl) return;\n"
    "    const imgEl = new window.Image();\n"
    "    imgEl.src = imageDataUrl;\n"
    "    imgEl.onload = () => {\n"
    "      // In edit/merge mode: remove the previous AI image before placing the new one\n"
    "      if (replaceExisting && lastAiImageRef.current) {\n"
    "        try { fabricCanvas.remove(lastAiImageRef.current); } catch (_) {}\n"
    "        lastAiImageRef.current = null;\n"
    "      }\n"
    "      const fImg = new fabric.FabricImage(imgEl);\n"
    "      fImg.__isAiGenerated = true;\n"
    "      const maxW = section === 'signature' ? 0.82 : section === 'icon' ? 0.42 : 0.5;\n"
    "      const maxH = section === 'signature' ? 0.42 : 0.62;\n"
    "      if (fImg.width > fabricCanvas.width * maxW) fImg.scaleToWidth(fabricCanvas.width * maxW);\n"
    "      if (fImg.getScaledHeight() > fabricCanvas.height * maxH) fImg.scaleToHeight(fabricCanvas.height * maxH);\n"
    "      fImg.set({ left: (fabricCanvas.width - fImg.getScaledWidth()) / 2, top: (fabricCanvas.height - fImg.getScaledHeight()) / 2 });\n"
    "      fabricCanvas.add(fImg);\n"
    "      fabricCanvas.setActiveObject(fImg);\n"
    "      fabricCanvas.renderAll();\n"
    "      lastAiImageRef.current = fImg;\n"
    "      setAiPrompt('');\n"
    "    };\n"
    "  }, [fabricCanvas, section]);"
)

# ---------------------------------------------------------------
# FIX 2: Replace handleGenerateLogoViaApi
# ---------------------------------------------------------------
OLD2 = (
    "  const handleGenerateLogoViaApi = async () => {\n"
    "    if (!isAiEnabled || !aiPrompt.trim() || !fabricCanvas) return;\n"
    "    setIsGenerating(true); setAiError('');\n"
    "    try {\n"
    "      const data = await generateLogo({ prompt: aiPrompt, remove_background: true });\n"
    "      placeGeneratedImage(data.image_data);\n"
    "    } catch {"
)

NEW2 = (
    "  const handleGenerateLogoViaApi = async (isNew = false) => {\n"
    "    if (!isAiEnabled || !aiPrompt.trim() || !fabricCanvas) return;\n"
    "    setIsGenerating(true); setAiError('');\n"
    "    try {\n"
    "      const data = await generateLogo({ prompt: aiPrompt, remove_background: true, section });\n"
    "      // isNew=true  -> 'new' button  -> always add fresh image\n"
    "      // isNew=false -> 'edit/merge'  -> replace the last AI image\n"
    "      placeGeneratedImage(data.image_data, !isNew);\n"
    "    } catch {"
)

# Apply fixes, normalizing line endings for matching
content_lf = content.replace('\r\n', '\n')
old1_lf = OLD1.replace('\r\n', '\n')
old2_lf = OLD2.replace('\r\n', '\n')

if old1_lf in content_lf:
    content_lf = content_lf.replace(old1_lf, NEW1, 1)
    print('[OK] FIX 1 applied: placeGeneratedImage updated')
else:
    print('[FAIL] FIX 1: old text not found')
    idx = content_lf.find('const placeGeneratedImage')
    if idx >= 0:
        print('Found at char', idx)
        print(repr(content_lf[idx: idx+400]))
    sys.exit(1)

if old2_lf in content_lf:
    content_lf = content_lf.replace(old2_lf, NEW2, 1)
    print('[OK] FIX 2 applied: handleGenerateLogoViaApi updated')
else:
    print('[FAIL] FIX 2: old text not found')
    idx = content_lf.find('handleGenerateLogoViaApi')
    if idx >= 0:
        print('Found at char', idx)
        print(repr(content_lf[idx: idx+300]))
    sys.exit(1)

# Write back with original line endings (CRLF for Windows)
with open(filepath, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content_lf)

print('[OK] File written successfully')
