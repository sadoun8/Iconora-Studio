import { Loader2, Sparkles, TriangleAlert, Wand2 } from 'lucide-react';

export default function AiSidebarPanel({
  aiPrompt,
  setAiPrompt,
  aiHint,
  isAiEnabled,
  aiError,
  isGenerating,
  onGenerate,
  bootstrapError,
  healthError,
  healthInfo,
}) {
  return (
    <div className="sidebar-section" style={{ flex: 1 }}>
      <div className="section-label"><Wand2 size={12} /> مولد الذكاء الاصطناعي</div>
      <div className="ai-panel">
        <div className="ai-panel-header"><Sparkles size={15} /> توليد بالذكاء الاصطناعي</div>
        <textarea
          className="ai-textarea"
          placeholder={aiHint}
          value={aiPrompt}
          onChange={(event) => setAiPrompt(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && event.ctrlKey && isAiEnabled) {
              onGenerate();
            }
          }}
          disabled={!isAiEnabled}
        />
        {!isAiEnabled && (
          <div className="ai-error"><TriangleAlert size={13} /> الذكاء الاصطناعي معطّل حالياً من الإعدادات.</div>
        )}
        {aiError && (
          <div className="ai-error"><TriangleAlert size={13} /> {aiError}</div>
        )}
        <button
          className={`btn btn-primary btn-full ${isGenerating ? 'generating-indicator' : ''}`}
          onClick={onGenerate}
          disabled={!isAiEnabled || isGenerating || !aiPrompt.trim()}
        >
          {isGenerating ? <><Loader2 size={15} className="animate-spin" /> جارٍ التوليد...</> : <><Wand2 size={15} /> توليد ودمج</>}
        </button>
        <p className="ai-note">
          `Ctrl+Enter` للتوليد السريع
          <br />
          <span style={{ color: 'var(--text-faint)' }}>
            {bootstrapError
              ? 'تم تفعيل بيانات احتياطية للأصول.'
              : healthError
                ? 'تعذر الاتصال بالخادم المحلي على 127.0.0.1:8000.'
                : healthInfo?.status === 'ok'
                  ? `الخادم المحلي متصل${healthInfo.version ? ` • v${healthInfo.version}` : ''}`
                  : 'الخادم المحلي متصل.'}
          </span>
        </p>
      </div>
    </div>
  );
}
