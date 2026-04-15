const fs = require('fs');
let content = fs.readFileSync('frontend/src/App.jsx', 'utf8');

// 1. Snapping Logic update
const snapStart = content.indexOf('  // ── Snapping ──');
const snapEnd = content.indexOf('}, [fabricCanvas, snapEnabled]);') + '}, [fabricCanvas, snapEnabled]);'.length;

const newSnap = `  // ── Snapping ──
  useEffect(() => {
    if (!fabricCanvas || !snapEnabled) {
      const svgEl = document.getElementById('snap-overlay');
      if (svgEl) svgEl.innerHTML = '';
      return;
    }
    const SNAP_DIST = 8;

    const onMoving = (e) => {
      const obj = e.target;
      if (!obj) return;
      
      const cw = fabricCanvas.width, ch = fabricCanvas.height;
      const ow = obj.getScaledWidth(), oh = obj.getScaledHeight();
      let left = obj.left, top = obj.top;

      const snapH = [];
      const snapV = [];

      const cx = cw / 2, cy = ch / 2;
      const ocx = left + ow / 2, ocy = top + oh / 2;

      let snapped = false;

      if (Math.abs(ocx - cx) < SNAP_DIST) { left = cx - ow / 2; snapV.push(cx); snapped = true; }
      if (Math.abs(ocy - cy) < SNAP_DIST) { top = cy - oh / 2; snapH.push(cy); snapped = true; }
      if (Math.abs(left) < SNAP_DIST) { left = 0; snapV.push(0); snapped = true; }
      if (Math.abs(top) < SNAP_DIST) { top = 0; snapH.push(0); snapped = true; }
      if (Math.abs(left + ow - cw) < SNAP_DIST) { left = cw - ow; snapV.push(cw); snapped = true; }
      if (Math.abs(top + oh - ch) < SNAP_DIST) { top = ch - oh; snapH.push(ch); snapped = true; }

      if (snapped) {
        obj.set({ left, top });
        obj.setCoords();
      }

      const paths = [];
      snapV.forEach(x => paths.push(\`<line x1="\${x}" y1="0" x2="\${x}" y2="\${ch}" stroke="#6366f1" stroke-width="1" stroke-dasharray="4 4" opacity="0.7" />\`));
      snapH.forEach(y => paths.push(\`<line x1="0" y1="\${y}" x2="\${cw}" y2="\${y}" stroke="#6366f1" stroke-width="1" stroke-dasharray="4 4" opacity="0.7" />\`));
      
      const svgEl = document.getElementById('snap-overlay');
      if (svgEl) svgEl.innerHTML = paths.join('');
    };

    const onMoved = () => { 
      const svgEl = document.getElementById('snap-overlay');
      if (svgEl) svgEl.innerHTML = '';
    };

    fabricCanvas.on('object:moving', onMoving);
    fabricCanvas.on('object:modified', onMoved);
    return () => {
      fabricCanvas.off('object:moving', onMoving);
      fabricCanvas.off('object:modified', onMoved);
    };
  }, [fabricCanvas, snapEnabled]);`;

content = content.slice(0, snapStart) + newSnap + content.slice(snapEnd);

// 2. SVG ID add
const svgTarget = /<svg className="snap-lines-overlay"[^>]*>[\s\S]*?<\/svg>/g;
content = content.replace(svgTarget, `<svg id="snap-overlay" className="snap-lines-overlay" style={{
              position: 'absolute', inset: 0, pointerEvents: 'none',
              width: canvasSize.w, height: canvasSize.h,
            }}>
            </svg>`);

fs.writeFileSync('frontend/src/App.jsx', content, 'utf8');
console.log("Snapping fixed!");
