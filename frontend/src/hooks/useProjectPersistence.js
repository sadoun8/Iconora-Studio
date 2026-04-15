import { useCallback } from 'react';

import {
  createProject,
  exportProject,
  getProject,
  importProject as importProjectApi,
  listProjects,
  updateProject,
} from '../lib/api.js';
import { SERIALIZED_CANVAS_PROPS } from './canvasSerialization.js';

export function useProjectPersistence({
  fabricCanvas,
  section,
  canvasSize,
  fontFamily,
  layerStates,
  zoom,
  currentProjectId,
  currentProjectName,
  selectedProjectId,
  setSection,
  setCanvasSize,
  setLayerStates,
  applyLayerStatesToCanvas,
  setZoom,
  setFontFamily,
  setActiveTool,
  setActiveObject,
  setCurrentProjectId,
  setCurrentProjectName,
  setShowSaveProjectModal,
  setSaveProjectDraft,
  setShowProjectsModal,
  setAvailableProjects,
  setSelectedProjectId,
  refreshLayers,
  saveSnapshot,
  isApplyingProjectRef,
  showNotice,
}) {
  const buildProjectPayload = useCallback((nameOverride = '') => {
    if (!fabricCanvas) return null;
    return {
      id: currentProjectId || undefined,
      name: nameOverride || currentProjectName || `Iconora ${section}`,
      kind: section,
      canvas: fabricCanvas.toJSON(SERIALIZED_CANVAS_PROPS),
      assets: {
        fonts: [fontFamily],
      },
      editor: {
        section,
        canvas_size: canvasSize,
        background: fabricCanvas.backgroundColor || '#ffffff',
        zoom,
        layer_states: layerStates,
      },
      export_defaults: {
        format: section === 'icon' ? 'ico' : 'png',
        width: canvasSize.w,
        height: canvasSize.h,
        transparent: false,
      },
    };
  }, [canvasSize, currentProjectId, currentProjectName, fabricCanvas, fontFamily, layerStates, section, zoom]);

  const applyLoadedProject = useCallback(async (project) => {
    if (!fabricCanvas) return;
    isApplyingProjectRef.current = true;
    try {
      const nextSection = ['logo', 'icon', 'signature'].includes(project.kind) ? project.kind : section;
      setSection(nextSection);

      const canvasData = project.canvas || {};
      const nextSize = project.editor?.canvas_size;
      if (nextSize?.w && nextSize?.h) {
        fabricCanvas.setDimensions({ width: nextSize.w, height: nextSize.h });
        setCanvasSize({ w: nextSize.w, h: nextSize.h });
      }

      await fabricCanvas.loadFromJSON(canvasData);
      fabricCanvas.backgroundColor = project.editor?.background || canvasData.backgroundColor || '#ffffff';

      const nextLayerStates = project.editor?.layer_states || {};
      setLayerStates(nextLayerStates);
      applyLayerStatesToCanvas(fabricCanvas, nextLayerStates);

      const nextZoom = Math.max(10, Math.min(400, Number(project.editor?.zoom || 100)));
      fabricCanvas.setViewportTransform([1, 0, 0, 1, 0, 0]);
      fabricCanvas.setZoom(nextZoom / 100);
      setZoom(nextZoom);

      const loadedFont = project.assets?.fonts?.[0];
      if (loadedFont) {
        setFontFamily(loadedFont);
      }

      setActiveTool('select');
      setActiveObject(null);
      fabricCanvas.requestRenderAll();
      refreshLayers(fabricCanvas);
      saveSnapshot(fabricCanvas);
      setCurrentProjectId(project.id || '');
      setCurrentProjectName(project.name || '');
    } finally {
      isApplyingProjectRef.current = false;
    }
  }, [
    applyLayerStatesToCanvas,
    fabricCanvas,
    isApplyingProjectRef,
    refreshLayers,
    saveSnapshot,
    section,
    setActiveObject,
    setActiveTool,
    setCanvasSize,
    setFontFamily,
    setLayerStates,
    setSection,
    setZoom,
  ]);

  const saveProject = useCallback(async (nameOverride = '') => {
    if (!fabricCanvas) return false;
    const proposedName = (nameOverride || currentProjectName || `Iconora ${section}`).trim();
    if (!proposedName) {
      showNotice('اسم المشروع', 'يرجى إدخال اسم صالح للمشروع.');
      return false;
    }
    try {
      const payload = buildProjectPayload(proposedName);
      const project = currentProjectId
        ? await updateProject(currentProjectId, payload)
        : await createProject(payload);
      setCurrentProjectId(project.id || '');
      setCurrentProjectName(project.name || proposedName);
      setShowSaveProjectModal(false);
      showNotice('تم الحفظ', `تم حفظ المشروع: ${project.name}`);
      return true;
    } catch (error) {
      showNotice('تعذر الحفظ', error.message);
      return false;
    }
  }, [buildProjectPayload, currentProjectId, currentProjectName, fabricCanvas, section, showNotice]);

  const openSaveProjectModal = useCallback(() => {
    setSaveProjectDraft(currentProjectName || `Iconora ${section}`);
    setShowSaveProjectModal(true);
  }, [currentProjectName, section]);

  const loadProjectFromApi = useCallback(async () => {
    if (!fabricCanvas) return;
    try {
      const result = await listProjects();
      const projects = result.projects || [];
      if (!projects.length) {
        showNotice('فتح مشروع', 'لا توجد مشاريع محفوظة حالياً.');
        return;
      }
      setAvailableProjects(projects);
      setSelectedProjectId(projects[0]?.id || '');
      setShowProjectsModal(true);
    } catch (error) {
      showNotice('تعذر الفتح', error.message);
    }
  }, [fabricCanvas, showNotice]);

  const confirmLoadProject = useCallback(async () => {
    if (!selectedProjectId) {
      showNotice('فتح مشروع', 'يرجى اختيار مشروع أولاً.');
      return;
    }
    try {
      const project = await getProject(selectedProjectId);
      await applyLoadedProject(project);
      setShowProjectsModal(false);
      showNotice('تم الفتح', `تم فتح المشروع: ${project.name}`);
    } catch (error) {
      showNotice('تعذر الفتح', error.message);
    }
  }, [applyLoadedProject, selectedProjectId, showNotice]);

  const exportProjectFile = useCallback(async () => {
    if (!currentProjectId) {
      showNotice('تصدير المشروع', 'احفظ المشروع أولاً قبل تصديره كملف.');
      return;
    }
    try {
      const result = await exportProject(currentProjectId);
      const payload = result.document || result;
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${(currentProjectName || payload.name || 'iconora_project').replace(/[<>:"/\\|?*]+/g, '_')}.iconora`;
      link.click();
      URL.revokeObjectURL(url);
      showNotice('تم التصدير', 'تم تصدير ملف المشروع بنجاح.');
    } catch (error) {
      showNotice('تعذر التصدير', error.message);
    }
  }, [currentProjectId, currentProjectName, showNotice]);

  const importProjectFile = useCallback(() => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.iconora,.json,application/json';
    input.onchange = async (event) => {
      const file = event.target.files?.[0];
      if (!file) return;
      try {
        const text = await file.text();
        const documentData = JSON.parse(text);
        const imported = await importProjectApi(documentData, file.name.replace(/\.(iconora|json)$/i, ''));
        await applyLoadedProject(imported);
        showNotice('تم الاستيراد', `تم استيراد المشروع: ${imported.name}`);
      } catch (error) {
        showNotice('تعذر الاستيراد', error.message || 'فشل في قراءة ملف المشروع.');
      }
    };
    input.click();
  }, [applyLoadedProject, showNotice]);

  return {
    applyLoadedProject,
    saveProject,
    openSaveProjectModal,
    loadProjectFromApi,
    confirmLoadProject,
    exportProjectFile,
    importProjectFile,
  };
}
