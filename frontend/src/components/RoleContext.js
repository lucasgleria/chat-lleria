import React, { createContext, useContext, useState, useEffect } from 'react';
import { fallbackRoles, getRoleById } from '../data/roles';
import { getApiUrl, API_CONFIG } from '../config/api';

// Create context
const RoleContext = createContext();

// Custom hook to use the context
export const useRole = () => {
  const context = useContext(RoleContext);
  if (!context) {
    throw new Error('useRole must be used within a RoleProvider');
  }
  return context;
};

// Context provider
export const RoleProvider = ({ children }) => {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load roles from backend or use fallback
  const loadRoles = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Try to load from backend
      const response = await fetch(getApiUrl(API_CONFIG.ENDPOINTS.ROLES));
      
      if (response.ok) {
        const data = await response.json();
        setRoles(data.roles || []);
        console.log('Roles loaded from backend:', data.roles.length);
      } else {
        // Use fallback if backend is not available
        console.warn('Backend not available, using fallback roles');
        setRoles(fallbackRoles);
      }
    } catch (err) {
      console.warn('Error loading roles from backend, using fallback:', err.message);
      setRoles(fallbackRoles);
      setError('Unable to load roles from server. Using local configuration.');
    } finally {
      setLoading(false);
    }
  };

  // Load roles on initialization
  useEffect(() => {
    loadRoles();
  }, []);

  // Select role
  const selectRole = (roleId) => {
    const role = roles.find(r => r.id === roleId) || getRoleById(roleId);
    if (role) {
      setSelectedRole(role);
      // Save to localStorage for persistence
      localStorage.setItem('selectedRole', JSON.stringify(role));
      console.log('Role selected:', role.name);
    } else {
      console.error('Role not found:', roleId);
    }
  };

  // Load saved role from localStorage
  const loadSavedRole = () => {
    try {
      const saved = localStorage.getItem('selectedRole');
      if (saved) {
        const role = JSON.parse(saved);
        setSelectedRole(role);
        console.log('Role loaded from localStorage:', role.name);
      }
    } catch (err) {
      console.warn('Error loading role from localStorage:', err);
    }
  };

  // Load saved role when roles are available
  useEffect(() => {
    if (roles.length > 0 && !selectedRole) {
      loadSavedRole();
    }
  }, [roles, selectedRole]);

  // Clear selected role
  const clearSelectedRole = () => {
    setSelectedRole(null);
    localStorage.removeItem('selectedRole');
  };

  // Get role by ID
  const getRole = (roleId) => {
    return roles.find(r => r.id === roleId) || getRoleById(roleId);
  };

  // Check if a role is selected
  const isRoleSelected = (roleId) => {
    return selectedRole && selectedRole.id === roleId;
  };

  // Reload roles
  const reloadRoles = () => {
    loadRoles();
  };

  // Context value
  const value = {
    // State
    roles,
    selectedRole,
    loading,
    error,
    
    // Actions
    selectRole,
    clearSelectedRole,
    getRole,
    isRoleSelected,
    reloadRoles,
    
    // Utilities
    hasRoles: roles.length > 0,
    defaultRole: roles.find(r => r.id === 'recruiter') || fallbackRoles[0]
  };

  return (
    <RoleContext.Provider value={value}>
      {children}
    </RoleContext.Provider>
  );
};

export default RoleContext; 