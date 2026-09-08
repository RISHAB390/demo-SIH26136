import React from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { RoleSelector } from './components/RoleSelector';
import { OfficerDashboard } from './components/OfficerDashboard/OfficerDashboard';
import { StartupDashboard } from './components/StartupDashboard/StartupDashboard';
import { EvaluatorDashboard } from './components/EvaluatorDashboard/EvaluatorDashboard';
import { Footer } from './components/Footer';
import { Loader2 } from 'lucide-react';

const DashboardRouter: React.FC = () => {
  const { currentUser, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', gap: 12 }}>
        <Loader2 size={36} className="animate-spin" color="#2563eb" />
        <div style={{ color: '#64748b', fontSize: 14 }}>Connecting to SIH Platform backend & PostgreSQL...</div>
      </div>
    );
  }

  if (!currentUser) {
    return (
      <div className="empty-state" style={{ margin: '40px auto', maxWidth: 480 }}>
        <div className="empty-state-title">No Active User Selected</div>
        <div className="empty-state-sub">Please select a seeded persona from the top navigation bar.</div>
      </div>
    );
  }

  switch (currentUser.role) {
    case 'officer':
      return <OfficerDashboard key={currentUser.id} />;
    case 'startup':
      return <StartupDashboard key={currentUser.id} />;
    case 'evaluator':
      return <EvaluatorDashboard key={currentUser.id} />;
    default:
      return <div>Unknown role: {currentUser.role}</div>;
  }
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <div className="app-container">
        <RoleSelector />
        <main className="main-content">
          <DashboardRouter />
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
};

export default App;
