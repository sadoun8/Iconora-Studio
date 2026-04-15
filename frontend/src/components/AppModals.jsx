import React from 'react';
import { TriangleAlert, X } from 'lucide-react';

import { getUiCopy } from '../i18n.js';

export function SettingsModal({
  open,
  onClose,
  language,
  settingsDraft,
  setSettingsDraft,
  healthInfo,
  settingsError,
  isSavingSettings,
  onSave,
}) {
  if (!open) return null;

  const copy = getUiCopy(language);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '560px' }}>
        <div className="modal-header">
          <span>{copy.settings.title}</span>
          <button className="modal-close" onClick={onClose}><X size={16} /></button>
        </div>
        <div className="modal-body">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="modal-field">
              <label>{copy.settings.theme}</label>
              <select
                className="styled-select"
                value={settingsDraft.theme}
                onChange={(e) => setSettingsDraft((prev) => ({ ...prev, theme: e.target.value }))}
              >
                <option value="dark">{copy.settings.dark}</option>
                <option value="light">{copy.settings.light}</option>
              </select>
            </div>
            <div className="modal-field">
              <label>{copy.settings.language}</label>
              <select
                className="styled-select"
                value={settingsDraft.language}
                onChange={(e) => setSettingsDraft((prev) => ({ ...prev, language: e.target.value }))}
              >
                <option value="ar">{copy.settings.arabic}</option>
                <option value="en">{copy.settings.english}</option>
              </select>
            </div>
          </div>
          <div className="modal-field">
            <label>{copy.settings.aiModel}</label>
            <input
              className="modal-input"
              value={settingsDraft.ai_model}
              onChange={(e) => setSettingsDraft((prev) => ({ ...prev, ai_model: e.target.value }))}
            />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="modal-field">
              <label>{copy.settings.aiEndpoint}</label>
              <input
                className="modal-input"
                value={settingsDraft.ai_endpoint}
                onChange={(e) => setSettingsDraft((prev) => ({ ...prev, ai_endpoint: e.target.value }))}
              />
            </div>
            <div className="modal-field">
              <label>{copy.settings.aiTimeout}</label>
              <input
                className="modal-input"
                type="number"
                min="1"
                max="300"
                value={settingsDraft.ai_timeout}
                onChange={(e) => setSettingsDraft((prev) => ({ ...prev, ai_timeout: Number(e.target.value) || 30 }))}
              />
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="modal-field">
              <label>{copy.settings.defaultQuality}</label>
              <input
                className="modal-input"
                type="number"
                min="1"
                max="100"
                value={settingsDraft.default_quality}
                onChange={(e) => setSettingsDraft((prev) => ({ ...prev, default_quality: Number(e.target.value) || 95 }))}
              />
            </div>
            <div className="modal-field">
              <label>{copy.settings.currentRuntime}</label>
              <div
                style={{
                  minHeight: '38px',
                  borderRadius: '8px',
                  border: '1px solid var(--border-2)',
                  background: 'var(--bg-active)',
                  color: 'var(--text-secondary)',
                  display: 'flex',
                  alignItems: 'center',
                  padding: '0 12px',
                  fontSize: '0.85rem',
                }}
              >
                {healthInfo?.status === 'ok'
                  ? `${copy.settings.backendReady}${healthInfo.version ? ` • v${healthInfo.version}` : ''}`
                  : copy.settings.backendUnavailable}
              </div>
            </div>
          </div>
          <label className={`snap-toggle ${settingsDraft.ai_enabled ? 'active' : ''}`} style={{ justifyContent: 'space-between' }}>
            <input
              type="checkbox"
              checked={settingsDraft.ai_enabled}
              onChange={(e) => setSettingsDraft((prev) => ({ ...prev, ai_enabled: e.target.checked }))}
            />
            <span>{copy.settings.aiEnabled}</span>
          </label>
          <label className={`snap-toggle ${settingsDraft.auto_open_folder ? 'active' : ''}`} style={{ justifyContent: 'space-between' }}>
            <input
              type="checkbox"
              checked={settingsDraft.auto_open_folder}
              onChange={(e) => setSettingsDraft((prev) => ({ ...prev, auto_open_folder: e.target.checked }))}
            />
            <span>{copy.settings.autoOpen}</span>
          </label>
          {settingsError && (
            <div className="ai-error"><TriangleAlert size={13} /> {settingsError}</div>
          )}
        </div>
        <div className="modal-footer">
          <button className="btn btn-ghost btn-sm" onClick={onClose}>{copy.settings.cancel}</button>
          <button className="btn btn-primary btn-sm" onClick={onSave} disabled={isSavingSettings}>
            {isSavingSettings ? copy.settings.saving : copy.settings.save}
          </button>
        </div>
      </div>
    </div>
  );
}

export function SaveProjectModal({
  open,
  onClose,
  value,
  onChange,
  onSave,
}) {
  if (!open) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <span>حفظ المشروع</span>
          <button className="modal-close" onClick={onClose}><X size={16} /></button>
        </div>
        <div className="modal-body">
          <div className="modal-field">
            <label>اسم المشروع</label>
            <input
              className="modal-input"
              value={value}
              onChange={(e) => onChange(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') onSave(); }}
              autoFocus
            />
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-ghost btn-sm" onClick={onClose}>إلغاء</button>
          <button className="btn btn-primary btn-sm" onClick={onSave}>حفظ</button>
        </div>
      </div>
    </div>
  );
}

export function OpenProjectModal({
  open,
  onClose,
  projects,
  selectedProjectId,
  onSelect,
  onOpen,
}) {
  if (!open) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <span>فتح مشروع</span>
          <button className="modal-close" onClick={onClose}><X size={16} /></button>
        </div>
        <div className="modal-body">
          <div className="modal-field">
            <label>المشاريع المتاحة</label>
            <select
              className="styled-select"
              value={selectedProjectId}
              onChange={(e) => onSelect(e.target.value)}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name} ({project.kind})
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-ghost btn-sm" onClick={onClose}>إلغاء</button>
          <button className="btn btn-primary btn-sm" onClick={onOpen}>فتح</button>
        </div>
      </div>
    </div>
  );
}

export function NoticeModal({
  open,
  title,
  message,
  onClose,
}) {
  if (!open) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '520px' }}>
        <div className="modal-header">
          <span>{title}</span>
          <button className="modal-close" onClick={onClose}><X size={16} /></button>
        </div>
        <div className="modal-body">
          <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.7, color: 'var(--text-secondary)' }}>
            {message}
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-primary btn-sm" onClick={onClose}>موافق</button>
        </div>
      </div>
    </div>
  );
}
