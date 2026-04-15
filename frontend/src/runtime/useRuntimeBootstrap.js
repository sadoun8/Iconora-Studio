import { useEffect, useState } from 'react';

import { fetchBootstrap, getHealth, getSettings } from '../lib/api.js';
import { FALLBACK_BOOTSTRAP } from './bootstrapFallback.js';

function getLocalizedAiHint(section, runtimeHints, runtimeSettings) {
  if (runtimeSettings?.language === 'en') {
    if (section === 'icon') {
      return 'Example: flat mobile app icon, blue lightning symbol on a dark background';
    }
    if (section === 'signature') {
      return 'Example: elegant Arabic signature for "Mohammed" in gold calligraphy';
    }
    return 'Example: calm lion in a flat vector style for a tech brand, no text';
  }

  return runtimeHints[section] || FALLBACK_BOOTSTRAP.ai_hints[section];
}

export function mergeBootstrapPayload(payload) {
  return {
    ...FALLBACK_BOOTSTRAP,
    ...(payload || {}),
    fonts: { ...FALLBACK_BOOTSTRAP.fonts, ...((payload && payload.fonts) || {}) },
    templates: { ...FALLBACK_BOOTSTRAP.templates, ...((payload && payload.templates) || {}) },
    icons: { ...FALLBACK_BOOTSTRAP.icons, ...((payload && payload.icons) || {}) },
    sizes: { ...FALLBACK_BOOTSTRAP.sizes, ...((payload && payload.sizes) || {}) },
    ornaments: (payload && payload.ornaments) || FALLBACK_BOOTSTRAP.ornaments,
    settings: { ...FALLBACK_BOOTSTRAP.settings, ...((payload && payload.settings) || {}) },
    ai_hints: { ...FALLBACK_BOOTSTRAP.ai_hints, ...((payload && payload.ai_hints) || {}) },
  };
}

export function getSectionConfig(section, bootstrap) {
  const runtimeTemplates = bootstrap.templates || FALLBACK_BOOTSTRAP.templates;
  const runtimeSizes = bootstrap.sizes || FALLBACK_BOOTSTRAP.sizes;
  const runtimeIcons = bootstrap.icons || FALLBACK_BOOTSTRAP.icons;
  const runtimeFonts = bootstrap.fonts || FALLBACK_BOOTSTRAP.fonts;
  const runtimeHints = bootstrap.ai_hints || FALLBACK_BOOTSTRAP.ai_hints;
  const runtimeSettings = bootstrap.settings || FALLBACK_BOOTSTRAP.settings;

  if (section === 'icon') {
    return {
      templates: runtimeTemplates.icon || FALLBACK_BOOTSTRAP.templates.icon,
      sizes: runtimeSizes.icon || FALLBACK_BOOTSTRAP.sizes.icon,
      icons: runtimeIcons.icon || FALLBACK_BOOTSTRAP.icons.icon,
      defaultSize: (runtimeSizes.icon || FALLBACK_BOOTSTRAP.sizes.icon)?.[0] || { w: 512, h: 512 },
      fonts: runtimeFonts.general || FALLBACK_BOOTSTRAP.fonts.general,
      aiHint: getLocalizedAiHint('icon', runtimeHints, runtimeSettings),
    };
  }

  if (section === 'signature') {
    return {
      templates: runtimeTemplates.signature || FALLBACK_BOOTSTRAP.templates.signature,
      sizes: runtimeSizes.signature || FALLBACK_BOOTSTRAP.sizes.signature,
      icons: runtimeIcons.signature || FALLBACK_BOOTSTRAP.icons.signature,
      defaultSize: (runtimeSizes.signature || FALLBACK_BOOTSTRAP.sizes.signature)?.[0] || { w: 800, h: 300 },
      fonts: runtimeFonts.signature || FALLBACK_BOOTSTRAP.fonts.signature,
      aiHint: getLocalizedAiHint('signature', runtimeHints, runtimeSettings),
    };
  }

  return {
    templates: runtimeTemplates.logo || FALLBACK_BOOTSTRAP.templates.logo,
    sizes: runtimeSizes.logo || FALLBACK_BOOTSTRAP.sizes.logo,
    icons: runtimeIcons.logo || FALLBACK_BOOTSTRAP.icons.logo,
    defaultSize: (runtimeSizes.logo || FALLBACK_BOOTSTRAP.sizes.logo)?.[0] || { w: 800, h: 800 },
    fonts: runtimeFonts.general || FALLBACK_BOOTSTRAP.fonts.general,
    aiHint: getLocalizedAiHint('logo', runtimeHints, runtimeSettings),
  };
}

export function useRuntimeBootstrap(defaultSettingsDraft) {
  const [bootstrap, setBootstrap] = useState(FALLBACK_BOOTSTRAP);
  const [bootstrapError, setBootstrapError] = useState('');
  const [healthInfo, setHealthInfo] = useState(null);
  const [healthError, setHealthError] = useState('');
  const [settingsDraft, setSettingsDraft] = useState(defaultSettingsDraft);
  const [settingsError, setSettingsError] = useState('');

  useEffect(() => {
    let mounted = true;

    const loadBootstrapData = async () => {
      try {
        const payload = await fetchBootstrap();
        if (!mounted) return;
        setBootstrap(mergeBootstrapPayload(payload));
        setBootstrapError('');
      } catch (error) {
        if (!mounted) return;
        setBootstrapError(error.message || 'Failed to load runtime assets');
      }
    };

    const loadHealthData = async () => {
      try {
        const payload = await getHealth();
        if (!mounted) return;
        setHealthInfo(payload);
        setHealthError('');
      } catch (error) {
        if (!mounted) return;
        setHealthError(error.message || 'Failed to load backend health');
      }
    };

    const loadSettingsData = async () => {
      try {
        const payload = await getSettings();
        if (!mounted) return;
        setBootstrap((current) => ({
          ...current,
          settings: { ...defaultSettingsDraft, ...(current.settings || {}), ...payload },
        }));
        setSettingsDraft((current) => ({ ...current, ...payload }));
      } catch (error) {
        if (!mounted) return;
        setSettingsError(error.message || 'Failed to load runtime settings');
      }
    };

    loadBootstrapData();
    loadHealthData();
    loadSettingsData();

    return () => {
      mounted = false;
    };
  }, [defaultSettingsDraft]);

  return {
    bootstrap,
    setBootstrap,
    bootstrapError,
    healthInfo,
    setHealthInfo,
    healthError,
    settingsDraft,
    setSettingsDraft,
    settingsError,
    setSettingsError,
  };
}
