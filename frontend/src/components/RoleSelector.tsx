import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Sparkles, Award, UserCheck } from 'lucide-react';

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
        return <Shield size={13} className="gov-icon-accent" />;
      case 'startup':
        return <Sparkles size={13} className="gov-icon-accent" />;
      case 'evaluator':
        return <Award size={13} className="gov-icon-accent" />;
      default:
        return <UserCheck size={13} className="gov-icon-accent" />;
    }
  };

  return (
    <header className="gov-header">
      {/* Left: Government of Maharashtra Identity & Platform Title */}
      <div className="gov-brand-container">
        {/* Government of Maharashtra Seal & Identity Area */}
        <div className="gov-state-identity">
          <div className="gov-emblem-wrapper" title="महाराष्ट्र शासन | Government of Maharashtra">
            {/* Official State Emblem Emblem Frame / Seal Vector */}
            <svg
              className="gov-emblem-svg"
              viewBox="0 0 100 100"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-label="Government of Maharashtra Seal"
            >
              <circle cx="50" cy="50" r="46" stroke="#D4AF37" strokeWidth="3" fill="#161B22" />
              <circle cx="50" cy="50" r="41" stroke="#D4AF37" strokeWidth="1" strokeDasharray="3 3" />
              {/* Ashoka Pillar / State Inscription representation */}
              <path
                d="M50 18 L53 27 L62 27 L55 33 L57 42 L50 37 L43 42 L45 33 L38 27 L47 27 Z"
                fill="#D4AF37"
              />
              <path
                d="M32 48 C32 44 68 44 68 48 C68 62 50 78 50 78 C50 78 32 62 32 48 Z"
                stroke="#D4AF37"
                strokeWidth="2"
                fill="none"
              />
              <path
                d="M38 52 L50 68 L62 52"
                stroke="#D4AF37"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
              <circle cx="50" cy="54" r="3" fill="#D4AF37" />
              <path d="M40 82 H60" stroke="#D4AF37" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </div>
          <div className="gov-state-text">
            <span className="gov-state-mr">महाराष्ट्र शासन</span>
            <span className="gov-state-en">Government of Maharashtra</span>
          </div>
        </div>

        {/* Subtle Institutional Divider */}
        <div className="gov-header-divider" aria-hidden="true" />

        {/* Platform Title & Subtitle */}
        <div className="gov-platform-identity">
          <h1 className="gov-platform-title">GovTech Innovation & Pilot Lifecycle Platform</h1>
          <p className="gov-platform-subtitle">Challenge-to-Pilot Workflow with Explainable Decision Support</p>
        </div>
      </div>

      {/* Right: Demo Persona Selector & Active User Status */}
      <div className="gov-actions-container">
        <div className="gov-persona-selector-box">
          <label htmlFor="persona-select" className="gov-selector-label">
            Demo Persona:
          </label>
          <select
            id="persona-select"
            className="gov-user-select"
            value={currentUser?.id || ''}
            onChange={handleUserChange}
            aria-label="Select Demo Persona"
          >
            {users.map((u) => (
              <option key={u.id} value={u.id}>
                {u.name} — {u.role.toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        {currentUser && (
          <div className="gov-user-profile-badge">
            <div className="gov-user-avatar">
              {getRoleIcon(currentUser.role)}
            </div>
            <div className="gov-user-info">
              <div className="gov-user-name-row">
                <span className="gov-user-name">{currentUser.name}</span>
                <span className={`gov-role-pill gov-role-${currentUser.role}`}>
                  {currentUser.role}
                </span>
              </div>
              <span className="gov-user-email">{currentUser.email}</span>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

