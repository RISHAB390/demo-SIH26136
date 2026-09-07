import React from 'react';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const normalized = status.toLowerCase().replace(/\s+/g, '_');
  const label = status.replace(/_/g, ' ');

  return (
    <span className={`status-badge badge-${normalized}`}>
      <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'currentColor', display: 'inline-block' }} />
      {label}
    </span>
  );
};
