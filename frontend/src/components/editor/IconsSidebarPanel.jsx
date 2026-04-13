import { Sparkles } from 'lucide-react';

export default function IconsSidebarPanel({
  icons,
  ornaments,
  addSvgIcon,
}) {
  return (
    <>
      <div className="sidebar-section">
        <div className="section-label"><Sparkles size={12} /> مكتبة أيقونات</div>
        <div className="icons-grid">
          {icons.map((icon) => (
            <button
              key={icon.label}
              title={icon.label}
              onClick={() => addSvgIcon(icon)}
              className="icon-grid-btn"
            >
              {icon.emoji}
            </button>
          ))}
        </div>
      </div>
      <div className="sidebar-section">
        <div className="section-label" style={{ color: '#fbbf24' }}>👑 زخارف فاخرة</div>
        <div className="icons-grid">
          {ornaments.map((ornament) => (
            <button
              key={ornament.label}
              title={ornament.label}
              onClick={() => addSvgIcon(ornament)}
              className="icon-grid-btn ornament"
            >
              {ornament.emoji}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}
