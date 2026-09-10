import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { RoleSelector } from './components/RoleSelector';
import { OfficerDashboard } from './components/OfficerDashboard/OfficerDashboard';
import { StartupDashboard } from './components/StartupDashboard/StartupDashboard';
import { EvaluatorDashboard } from './components/EvaluatorDashboard/EvaluatorDashboard';
import { Loader2 } from 'lucide-react';
import ProtectedRoute from './components/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="app-container">
          <RoleSelector />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route
                path="/dashboard/officer"
                element={
                  <ProtectedRoute allowedRoles={["officer"]}>
                    <OfficerDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/dashboard/startup"
                element={
                  <ProtectedRoute allowedRoles={["startup"]}>
                    <StartupDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/dashboard/evaluator"
                element={
                  <ProtectedRoute allowedRoles={["evaluator"]}>
                    <EvaluatorDashboard />
                  </ProtectedRoute>
                }
              />
              {/* Redirect unknown routes to landing */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
