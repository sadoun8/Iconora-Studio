import { Loader2, Sparkles, TriangleAlert, Wand2 } from 'lucide-react';

import { getUiCopy } from '../../i18n.js';

export default function AiSidebarPanel({
  aiPrompt,
  setAiPrompt,
  aiDebugInfo,
  aiHint,
  language,
  isAiEnabled,
  aiError,
  isGenerating,
  onGenerate,
  bootstrapError,
  healthError,
  healthInfo,
}) {
  const copy = getUiCopy(language);
  const debugOutput = aiDebugInfo ? JSON.stringify(aiDebugInfo, null, 2) : '';

  return (
    <div className="sidebar-section" style={{ flex: 1 }}>
      <div className="section-label"><Wand2 size={12} /> {copy.ai.title}</div>
      <div className="ai-panel">
        <div className="ai-panel-header"><Sparkles size={15} /> {copy.ai.subtitle}</div>
        <textarea
          className="ai-textarea"
          placeholder={aiHint}
          value={aiPrompt}
          onChange={(event) => setAiPrompt(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && event.ctrlKey && isAiEnabled) {
              onGenerate(false);
            }
          }}
          disabled={!isAiEnabled}
        />
        {!isAiEnabled && (
          <div className="ai-error"><TriangleAlert size={13} /> {copy.ai.disabled}</div>
        )}
        {aiError && (
          <div className="ai-error"><TriangleAlert size={13} /> {aiError}</div>
        )}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 60px', gap: '6px' }}>
          <button
            className={`btn btn-primary ${isGenerating ? 'generating-indicator' : ''}`}
            onClick={() => onGenerate(false)}
            disabled={!isAiEnabled || isGenerating || !aiPrompt.trim()}
          >
            {isGenerating ? <><Loader2 size={15} className="animate-spin" /> ...</> : <><Wand2 size={15} /> {copy.ai.refine}</>}
          </button>
          <button
            className="btn btn-ghost"
            style={{ padding: '0', border: '1px solid var(--border-2)' }}
            onClick={() => onGenerate(true)}
            disabled={!isAiEnabled || isGenerating || !aiPrompt.trim()}
            title={copy.ai.freshTitle}
          >
            {copy.ai.fresh} ✨
          </button>
        </div>
        <p className="ai-note">
          {copy.ai.shortcut}
          <br />
          <span style={{ color: 'var(--text-faint)' }}>
            {bootstrapError
              ? copy.ai.fallback
              : healthError
                ? copy.ai.healthError
                : healthInfo?.status === 'ok'
                  ? `${copy.ai.healthOk}${healthInfo.version ? ` • v${healthInfo.version}` : ''}`
                  : copy.ai.healthOk}
          </span>
        </p>
        <div className="ai-debug-section">
          <div className="ai-debug-label">{copy.ai.debugTitle}</div>
          <textarea
            className="ai-debug-output"
            value={debugOutput}
            placeholder={copy.ai.debugPlaceholder}
            readOnly
            spellCheck={false}
          />
        </div>
      </div>
    </div>
  );
}
