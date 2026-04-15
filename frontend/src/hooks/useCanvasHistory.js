import { useCallback, useRef, useState } from 'react';

import { SERIALIZED_CANVAS_PROPS } from './canvasSerialization.js';

export function useCanvasHistory({ fabricCanvas, refreshLayers }) {
  const historyRef = useRef({ stack: [], idx: -1, paused: false });
  const [, setRevision] = useState(0);

  const syncHistoryState = useCallback(() => {
    setRevision((current) => current + 1);
  }, []);

  const pauseHistory = useCallback(() => {
    historyRef.current.paused = true;
  }, []);

  const resumeHistory = useCallback(() => {
    historyRef.current.paused = false;
  }, []);

  const resetHistory = useCallback(() => {
    historyRef.current = { stack: [], idx: -1, paused: false };
    syncHistoryState();
  }, [syncHistoryState]);

  const saveSnapshot = useCallback((canvasInstance) => {
    if (!canvasInstance || historyRef.current.paused) return;
    const snapshot = JSON.stringify({
      ...canvasInstance.toJSON(SERIALIZED_CANVAS_PROPS),
      backgroundColor: canvasInstance.backgroundColor,
    });
    const currentHistory = historyRef.current;
    const nextStack = currentHistory.stack.slice(0, currentHistory.idx + 1);
    nextStack.push(snapshot);
    if (nextStack.length > 40) {
      nextStack.shift();
    }
    currentHistory.stack = nextStack;
    currentHistory.idx = nextStack.length - 1;
    syncHistoryState();
  }, [syncHistoryState]);

  const restoreSnapshot = useCallback(async (canvasInstance, jsonStr) => {
    if (!canvasInstance || !jsonStr) return;
    const data = JSON.parse(jsonStr);
    await canvasInstance.loadFromJSON(data);
    if (data.backgroundColor) {
      canvasInstance.backgroundColor = data.backgroundColor;
    }
    canvasInstance.requestRenderAll();
  }, []);

  const undo = useCallback(async () => {
    if (!fabricCanvas) return;
    const currentHistory = historyRef.current;
    if (currentHistory.idx <= 0) return;
    currentHistory.idx -= 1;
    currentHistory.paused = true;
    await restoreSnapshot(fabricCanvas, currentHistory.stack[currentHistory.idx]);
    currentHistory.paused = false;
    refreshLayers(fabricCanvas);
    syncHistoryState();
  }, [fabricCanvas, refreshLayers, restoreSnapshot, syncHistoryState]);

  const redo = useCallback(async () => {
    if (!fabricCanvas) return;
    const currentHistory = historyRef.current;
    if (currentHistory.idx >= currentHistory.stack.length - 1) return;
    currentHistory.idx += 1;
    currentHistory.paused = true;
    await restoreSnapshot(fabricCanvas, currentHistory.stack[currentHistory.idx]);
    currentHistory.paused = false;
    refreshLayers(fabricCanvas);
    syncHistoryState();
  }, [fabricCanvas, refreshLayers, restoreSnapshot, syncHistoryState]);

  return {
    historyRef,
    pauseHistory,
    resumeHistory,
    resetHistory,
    saveSnapshot,
    restoreSnapshot,
    undo,
    redo,
    canUndo: historyRef.current.idx > 0,
    canRedo: historyRef.current.idx < historyRef.current.stack.length - 1,
  };
}
