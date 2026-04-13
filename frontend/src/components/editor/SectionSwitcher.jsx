import { Hexagon, LayoutTemplate, PenLine } from 'lucide-react';

const SECTIONS = [
  { id: 'logo', icon: <LayoutTemplate size={14} />, label: 'لوجو' },
  { id: 'icon', icon: <Hexagon size={14} />, label: 'أيقونات' },
  { id: 'signature', icon: <PenLine size={14} />, label: 'توقيع' },
];

/**
 * SectionSwitcher
 *
 * Props:
 *  section      – القسم النشط ('logo' | 'icon' | 'signature')
 *  setSection   – دالة لتغيير القسم
 */
export default function SectionSwitcher({ section, setSection }) {
  return (
    <div className="sidebar-section-switcher sidebar-section-switcher-side">
      {SECTIONS.map(tab => (
        <button
          key={tab.id}
          onClick={() => setSection(tab.id)}
          className={`section-tab panel-section-tab ${section === tab.id ? 'active' : ''}`}
        >
          {tab.icon} {tab.label}
        </button>
      ))}
    </div>
  );
}
