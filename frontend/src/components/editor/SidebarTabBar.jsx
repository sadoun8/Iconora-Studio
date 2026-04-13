import { Layers, Settings2, Sparkles, Star, Wand2 } from 'lucide-react';

const SIDEBAR_TABS = [
  { id: 'tools', icon: <Settings2 size={15} />, label: 'أدوات' },
  { id: 'templates', icon: <Star size={15} />, label: 'قوالب' },
  { id: 'icons', icon: <Sparkles size={15} />, label: 'مكتبة' },
  { id: 'ai', icon: <Wand2 size={15} />, label: 'ذكاء' },
  { id: 'layers', icon: <Layers size={15} />, label: 'طبقات' },
];

export default function SidebarTabBar({ sidebarTab, setSidebarTab }) {
  return (
    <div className="sidebar-tabbar">
      {SIDEBAR_TABS.map((tab) => (
        <button
          key={tab.id}
          className={`sidebar-tab-btn ${sidebarTab === tab.id ? 'active' : ''}`}
          onClick={() => setSidebarTab(tab.id)}
          title={tab.label}
        >
          {tab.icon}
        </button>
      ))}
    </div>
  );
}
