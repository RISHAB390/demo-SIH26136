import React, { createContext, useContext, useState, useEffect } from 'react';
import type { User } from '../types';
import { api } from '../api/client';

interface AuthContextType {
  currentUser: User | null;
  users: User[];
  setCurrentUser: (user: User) => void;
  loading: boolean;
  refreshUsers: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [users, setUsers] = useState<User[]>([]);
  const [currentUser, setCurrentUserState] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUsers = async () => {
    try {
      const data = await api.getUsers();
      setUsers(data);
      const savedId = api.getSavedUserId();
      if (savedId) {
        const found = data.find((u) => u.id === savedId);
        if (found) {
          setCurrentUserState(found);
          api.setUserId(found.id);
          return;
        }
      }
      // Default to the first officer if available
      if (data.length > 0 && !currentUser) {
        const defaultUser = data.find((u) => u.role === 'officer') || data[0];
        setCurrentUserState(defaultUser);
        api.setUserId(defaultUser.id);
      }
    } catch (err) {
      console.error('Failed to load demo users:', err);
    } finally {
      setLoading(false);
    }
  };

  // Attempt to refresh token on mount
  useEffect(() => {
    const attemptRefresh = async () => {
      try {
        await api.refreshToken();
        await refreshUsers();
      } catch (e) {
        console.warn('Refresh token failed, user not logged in');
        await refreshUsers();
      }
    };
    attemptRefresh();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const resp = await api.login(email, password);
      // Expected shape { access_token: string, token_type?: string }
      const token = resp?.access_token || resp?.token || '';
      if (token) {
        api.setToken(token);
        localStorage.setItem('sih_demo_token', token);
      }
      // After successful login, fetch users and set the logged‑in user
      const data = await api.getUsers();
      setUsers(data);
      const found = data.find((u) => u.email === email);
      if (found) {
        setCurrentUserState(found);
        api.setUserId(found.id);
      }
    } catch (err) {
      console.error('Login failed:', err);
      throw err;
    }
  };

  const logout = async () => {
    try {
      await api.logout();
    } finally {
      setCurrentUserState(null);
      api.setUserId(null as any);
    }
  };

  const setCurrentUser = (user: User) => {
    setCurrentUserState(user);
    api.setUserId(user.id);
  };

  return (
    <AuthContext.Provider
      value={{ currentUser, users, setCurrentUser, loading, refreshUsers, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
