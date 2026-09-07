import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Sparkles, Award } from 'lucide-react';

export const RoleSelector: React.FC = () => {
  const { users, currentUser, setCurrentUser } = useAuth();

  const handleUserChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const userId = parseInt(e.target.value, 10);
    const selected = users.find((u) => u.id === userId);
    if (selected) {
      setCurrentUser(selected);
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'officer':
        return <Shield size={14} />;
      case 'startup':
        return <Sparkles size={14} />;
      case 'evaluator':
        return <Award size={14} />;
      default:
        return null;
    }
  };

  return (
    <header className="role-bar">
      <div className="brand-section">
        <span className="brand-badge">SIH 26136</span>
        <div>
          <div className="brand-title">GovTech Innovation & Pilot Lifecycle Platform</div>
          <div className="brand-sub">Challenge-to-Pilot Workflow with Explainable Decision Support</div>
        </div>
      </div>

      <div className="role-selector-container">
        <span className="role-selector-label">Demo Persona:</span>
        <select
          className="user-select"
          value={currentUser?.id || ''}
          onChange={handleUserChange}
        >
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.name} ({u.role.toUpperCase()})
            </option>
          ))}
        </select>

        {currentUser && (
          <div className="active-persona-pill">
            {getRoleIcon(currentUser.role)}
            <span className={`role-tag role-${currentUser.role}`}>{currentUser.role}</span>
            <span>{currentUser.name}</span>
          </div>
        )}
      </div>
    </header>
  );
};
