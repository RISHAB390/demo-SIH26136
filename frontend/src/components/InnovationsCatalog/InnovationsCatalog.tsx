import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import type { CatalogItem } from '../../types';
import { X } from 'lucide-react';

export const InnovationsCatalog: React.FC = () => {
  const [items, setItems] = useState<CatalogItem[]>([]);
  const [selectedItem, setSelectedItem] = useState<CatalogItem | null>(null);

  useEffect(() => {
    api.getInnovationsCatalog().then(setItems).catch(console.error);
  }, []);

  return (
    <div>
      <div className="dashboard-header">
        <div className="dashboard-title-group">
          <h1>🏆 National Innovations Catalog</h1>
          <div className="dashboard-subtitle">
            Proven startup solutions available for government procurement across departments
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '24px' }}>
        {items.map((item, idx) => (
          <div key={idx} className="content-card">
            <h3 className="card-title" style={{ fontSize: '1.2rem', marginBottom: '8px' }}>{item.startup_name}</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
              <span className="meta-chip">{item.startup_sector}</span>
              {item.dpiit_status && <span className="meta-chip" style={{ background: '#ffedd5', color: '#c2410c' }}>DPIIT</span>}
              {item.women_led && <span className="meta-chip" style={{ background: '#f3e8ff', color: '#7e22ce' }}>Women-led</span>}
              {item.make_in_india_class && <span className="meta-chip" style={{ background: '#dbeafe', color: '#1d4ed8' }}>{item.make_in_india_class === 'class_1' ? 'Class-I' : 'Class-II'}</span>}
              <span style={{ padding: '4px 8px', background: '#ecfdf5', color: '#059669', borderRadius: '4px', fontSize: '12px', fontWeight: 600 }}>✅ Proven — Recommend Scale</span>
            </div>
            
            <div style={{ fontSize: '13px', color: '#475569', marginBottom: '16px' }}>
              <div><strong>Challenge:</strong> {item.challenge_title}</div>
              <div><strong>Budget:</strong> {item.challenge_budget_band}</div>
              {item.evaluation_score !== null && <div><strong>Score:</strong> {item.evaluation_score}/100</div>}
              <div style={{ marginTop: '8px' }}>
                <strong>Pilot Scope:</strong> {item.pilot_scope.length > 100 ? item.pilot_scope.substring(0, 100) + '...' : item.pilot_scope}
              </div>
            </div>

            <button
              className="btn btn-primary"
              style={{ width: '100%' }}
              onClick={() => setSelectedItem(item)}
            >
              Scale This Solution
            </button>
          </div>
        ))}
        {items.length === 0 && (
          <div style={{ padding: '24px', color: '#64748b' }}>No proven innovations cataloged yet.</div>
        )}
      </div>

      {selectedItem && (
        <div className="modal-overlay">
          <div className="modal-dialog">
            <div className="modal-header">
              <h3 className="modal-title">Procure This Solution</h3>
              <button className="modal-close-btn" onClick={() => setSelectedItem(null)}><X size={18} /></button>
            </div>
            <div className="modal-body">
              <p>Contact your procurement department to acquire <strong>{selectedItem.startup_name}'s</strong> solution for <strong>{selectedItem.challenge_title}</strong>.</p>
              <div style={{ padding: '16px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', margin: '16px 0' }}>
                <div style={{ fontSize: '12px', color: '#64748b', fontWeight: 600 }}>Reference ID:</div>
                <div style={{ fontWeight: 700, fontSize: '16px' }}>{selectedItem.application_reference_id}</div>
              </div>
              <p style={{ fontSize: '13px', color: '#64748b' }}>This solution has been independently piloted and verified. Use this reference when raising a procurement request.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
