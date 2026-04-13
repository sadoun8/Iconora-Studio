import { Star } from 'lucide-react';

export default function TemplatesSidebarPanel({ templates, applyTemplate }) {
  return (
    <div className="sidebar-section">
      <div className="section-label"><Star size={12} /> قوالب جاهزة</div>
      <div className="templates-grid">
        {templates.map((template) => (
          <div
            key={template.id}
            className="template-card"
            onClick={() => applyTemplate(template)}
          >
            <div className="template-preview">{template.emoji}</div>
            {template.label}
          </div>
        ))}
      </div>
    </div>
  );
}
