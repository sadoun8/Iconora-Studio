import { Layers, Settings2, Sparkles, Star, Wand2 } from 'lucide-react';

import { getUiCopy } from '../../i18n.js';

const SIDEBAR_TABS = [
  { id: 'tools', icon: <Settings2 size={15} /> },
  { id: 'templates', icon: <Star size={15} /> },
  { id: 'icons', icon: <Sparkles size={15} /> },
  { id: 'ai', icon: <Wand2 size={15} /> },
  { id: 'layers', icon: <Layers size={15} /> },
];

export default function SidebarTabBar({ sidebarTab, setSidebarTab, language }) {
  const copy = getUiCopy(language);

  return (
    <div className="sidebar-tabbar">
      {SIDEBAR_TABS.map((tab) => (
        <button
          key={tab.id}
          className={`sidebar-tab-btn ${sidebarTab === tab.id ? 'active' : ''}`}
          onClick={() => setSidebarTab(tab.id)}
          title={copy.tabs[tab.id]}
        >
          {tab.icon}
        </button>
      ))}
    </div>
  );
}
