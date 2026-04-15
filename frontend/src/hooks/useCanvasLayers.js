import { useCallback, useState } from 'react';

function getObjectUid(obj) {
  if (!obj) return '';
  if (!obj.__uid) {
    obj.__uid = Math.random().toString(36).slice(2);
  }
  return obj.__uid;
}

export function useCanvasLayers({ fabricCanvas, getLayerLabel }) {
  const [layers, setLayers] = useState([]);
  const [layerStates, setLayerStates] = useState({});

  const refreshLayers = useCallback((canvasInstance = fabricCanvas) => {
    if (!canvasInstance) return;
    const objects = canvasInstance.getObjects().slice().reverse();
    setLayers(objects.map((obj, index) => ({
      id: index,
      obj,
      label: getLayerLabel(obj),
    })));
  }, [fabricCanvas, getLayerLabel]);

  const updateLayers = useCallback(() => {
    if (fabricCanvas) {
      refreshLayers(fabricCanvas);
    }
  }, [fabricCanvas, refreshLayers]);

  const applyLayerStatesToCanvas = useCallback((canvasInstance, nextLayerStates = {}) => {
    if (!canvasInstance) return;
    canvasInstance.getObjects().forEach((obj) => {
      const id = getObjectUid(obj);
      const currentState = nextLayerStates[id] || { visible: true, locked: false };
      const visible = currentState.visible !== false;
      const locked = currentState.locked === true;
      obj.set('visible', visible);
      obj.set('selectable', visible && !locked);
      obj.set('evented', visible && !locked);
    });
    canvasInstance.requestRenderAll();
  }, []);

  const toggleLayerVisibility = useCallback((obj) => {
    if (!obj) return;
    const id = getObjectUid(obj);
    setLayerStates((prev) => {
      const currentState = prev[id] || { visible: true, locked: false };
      const visible = !currentState.visible;
      obj.set('visible', visible);
      obj.set('selectable', visible && !currentState.locked);
      obj.set('evented', visible && !currentState.locked);
      fabricCanvas?.requestRenderAll();
      return { ...prev, [id]: { ...currentState, visible } };
    });
  }, [fabricCanvas]);

  const toggleLayerLock = useCallback((obj) => {
    if (!obj) return;
    const id = getObjectUid(obj);
    setLayerStates((prev) => {
      const currentState = prev[id] || { visible: true, locked: false };
      const locked = !currentState.locked;
      obj.set('selectable', currentState.visible && !locked);
      obj.set('evented', currentState.visible && !locked);
      fabricCanvas?.requestRenderAll();
      return { ...prev, [id]: { ...currentState, locked } };
    });
  }, [fabricCanvas]);

  const clearLayers = useCallback(() => {
    setLayers([]);
    setLayerStates({});
  }, []);

  return {
    layers,
    layerStates,
    setLayerStates,
    refreshLayers,
    updateLayers,
    applyLayerStatesToCanvas,
    toggleLayerVisibility,
    toggleLayerLock,
    clearLayers,
  };
}
