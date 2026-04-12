import React from 'react';
import { TriangleAlert, X } from 'lucide-react';

export function SettingsModal({
  open,
  onClose,
  settingsDraft,
  setSettingsDraft,
  healthInfo,
  settingsError,
  isSavingSettings,
  onSave,
}) {
  if (!open) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()} style={{ maxWidth: '560px' }}>
        <div className="modal-header">
          <span>إعدادات التطبيق</span>
          <button className="modal-close" onClick={onClose}><X size={16} /></button>
        </div>
        <div className="modal-body">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="modal-field">
              <label>Theme</label>
              <select
                className="styled-select"
                value={settingsDraft.theme}
                onChange={e => setSettingsDraft(prev => ({ ...prev, theme: e.target.value }))}
              >
                <option value="dark">Dark</option>
                <option value="light">Light</option>
              </select>
            </div>
            <div className="modal-field">
              <label>Language</label>
              <select
                className="styled-select"
                value={settingsDraft.language}
                onChange={e => setSettingsDraft(prev => ({ ...prev, language: e.target.value }))}
              >
                <option value="ar">Arabic</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>
          <div className="modal-field">
            <label>AI Model</label>
            <input
              className="modal-input"
              value={settingsDraft.ai_model}
              onChange={e => setSettingsDraft(prev => ({ ...prev, ai_model: e.target.value }))}
            />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="modal-field">
              <label>AI Endpoint</label>
              <input
                className="modal-input"
                value={settingsDraft.ai_endpoint}
                onChange={e => setSettingsDraft(prev => ({ ...prev, ai_endpoint: e.target.value }))}
              />
            </div>
            <div className="modal-field">
              <label>AI Timeout (sec)</label>
              <input
                className="modal-input"
                type="number"
                min="1"
                max="300"
                value={settingsDraft.ai_timeout}
                onChange={e => setSettingsDraft(prev => ({ ...prev, ai_timeout: Number(e.target.value) || 30 }))}
              />
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="modal-field">
              <label>Default Quality</label>
              <input
                className="modal-input"
                type="number"
                min="1"
                max="100"
                value={settingsDraft.default_quality}
                onChange={e => setSettingsDraft(prev => ({ ...prev, default_quality: Number(e.target.value) || 95 }))}
              />
            </div>
            <div className="modal-field">
              <label>Current Runtime</label>
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
                  ? `Backend جاهز${healthInfo.version ? ` • v${healthInfo.version}` : ''}`
                  : 'Backend status unavailable'}
              </div>
            </div>
          </div>
          <label className="snap-toggle" style={{ justifyContent: 'space-between' }}>
            <input
              type="checkbox"
              checked={settingsDraft.ai_enabled}
              onChange={e => setSettingsDraft(prev => ({ ...prev, ai_enabled: e.target.checked }))}
            />
            <span>تفعيل الذكاء الاصطناعي</span>
          </label>
          <label className="snap-toggle" style={{ justifyContent: 'space-between' }}>
            <input
              type="checkbox"
              checked={settingsDraft.auto_open_folder}
              onChange={e => setSettingsDraft(prev => ({ ...prev, auto_open_folder: e.target.checked }))}
            />
            <span>فتح مجلد التصدير تلقائياً</span>
          </label>
          {settingsError && (
            <div className="ai-error"><TriangleAlert size={13} /> {settingsError}</div>
          )}
        </div>
        <div className="modal-footer">
          <button className="btn btn-ghost btn-sm" onClick={onClose}>إلغاء</button>
          <button className="btn btn-primary btn-sm" onClick={onSave} disabled={isSavingSettings}>
            {isSavingSettings ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
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
      <div className="modal-box" onClick={e => e.stopPropagation()}>
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
              onChange={e => onChange(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') onSave(); }}
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
      <div className="modal-box" onClick={e => e.stopPropagation()}>
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
              onChange={e => onSelect(e.target.value)}
            >
              {projects.map(project => (
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
      <div className="modal-box" onClick={e => e.stopPropagation()} style={{ maxWidth: '520px' }}>
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
