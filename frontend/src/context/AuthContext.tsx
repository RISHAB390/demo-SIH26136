import React, { createContext, useContext, useState, useEffect } from 'react';
import type { User } from '../types';
import { api } from '../api/client';

interface AuthContextType {
  currentUser: User | null;
  users: User[];
  setCurrentUser: (user: User) => void;
  loading: boolean;
  refreshUsers: () => Promise<void>;
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

  useEffect(() => {
    refreshUsers();
  }, []);

  const setCurrentUser = (user: User) => {
    setCurrentUserState(user);
    api.setUserId(user.id);
  };

  return (
    <AuthContext.Provider value={{ currentUser, users, setCurrentUser, loading, refreshUsers }}>
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
