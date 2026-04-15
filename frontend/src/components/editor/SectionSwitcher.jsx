import { Hexagon, LayoutTemplate, PenLine } from 'lucide-react';

import { getUiCopy } from '../../i18n.js';

const SECTIONS = [
  { id: 'logo', icon: <LayoutTemplate size={14} /> },
  { id: 'icon', icon: <Hexagon size={14} /> },
  { id: 'signature', icon: <PenLine size={14} /> },
];

export default function SectionSwitcher({ section, setSection, language }) {
  const copy = getUiCopy(language);

  return (
    <div className="sidebar-section-switcher sidebar-section-switcher-side">
      {SECTIONS.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setSection(tab.id)}
          className={`section-tab panel-section-tab ${section === tab.id ? 'active' : ''}`}
        >
          {tab.icon} {copy.sections[tab.id]}
        </button>
      ))}
    </div>
  );
}
