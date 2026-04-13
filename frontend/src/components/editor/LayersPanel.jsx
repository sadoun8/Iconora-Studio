import { Eye, EyeOff, Layers, Lock, Unlock, X } from 'lucide-react';

export default function LayersPanel({
  layers,
  layerStates,
  activeObject,
  selectLayer,
  toggleLayerVisibility,
  toggleLayerLock,
  deleteLayer,
}) {
  return (
    <div className="sidebar-section">
      <div className="section-label" style={{ justifyContent: 'space-between' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Layers size={12} /> الطبقات ({layers.length})
        </span>
      </div>
      {layers.length === 0 ? (
        <div className="empty-layers">لا توجد عناصر بعد</div>
      ) : (
        <div className="layers-list">
          {layers.map((layer, index) => {
            const id = layer.obj.__uid;
            const state = layerStates[id] || { visible: true, locked: false };
            return (
              <div
                key={index}
                className={`layer-item ${activeObject === layer.obj ? 'active' : ''}`}
                onClick={() => !state.locked && selectLayer(layer.obj)}
              >
                <button
                  className="layer-action-btn"
                  onClick={(event) => {
                    event.stopPropagation();
                    toggleLayerVisibility(layer.obj);
                  }}
                  title={state.visible ? 'إخفاء' : 'إظهار'}
                >
                  {state.visible ? <Eye size={12} /> : <EyeOff size={12} />}
                </button>
                <button
                  className="layer-action-btn"
                  onClick={(event) => {
                    event.stopPropagation();
                    toggleLayerLock(layer.obj);
                  }}
                  title={state.locked ? 'فتح' : 'قفل'}
                >
                  {state.locked ? <Lock size={12} /> : <Unlock size={12} />}
                </button>
                <span className="layer-name">{layer.label}</span>
                <button
                  className="layer-delete"
                  onClick={(event) => {
                    event.stopPropagation();
                    deleteLayer(layer.obj);
                  }}
                >
                  <X size={12} />
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
