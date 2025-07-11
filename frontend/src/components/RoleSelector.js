import React, { useState } from 'react';
import { useRole } from './RoleContext';
import RoleCard from './RoleCard';
import BaseLayout from './BaseLayout';

const RoleSelector = ({ onRoleSelected, onBack }) => {
  const { roles, loading, error, selectRole, selectedRole, isRoleSelected } = useRole();
  const [isSelecting, setIsSelecting] = useState(false);

  const handleRoleSelect = async (roleId) => {
    setIsSelecting(true);
    
    try {
      selectRole(roleId);
      
      // Simular um pequeno delay para feedback visual
      await new Promise(resolve => setTimeout(resolve, 300));
      
      if (onRoleSelected) {
        onRoleSelected(roleId);
      }
    } catch (err) {
      console.error('Error selecting role:', err);
    } finally {
      setIsSelecting(false);
    }
  };

  const handleContinue = () => {
    if (selectedRole && onRoleSelected) {
      onRoleSelected(selectedRole.id);
    }
  };

  const handleBack = () => {
    if (onBack) {
      onBack();
    }
  };

  // Loading state
  if (loading) {
    return (
      <BaseLayout maxWidth="md">
        <div className="text-center">
          {/* Spinner animado */}
          <div className="relative mb-8">
            <div className="w-16 h-16 md:w-20 md:h-20 mx-auto relative">
              <div className="absolute inset-0 rounded-full border-4 border-blue-200"></div>
              <div 
                className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-600 animate-spin"
                style={{ animationDuration: '1s' }}
              ></div>
              <div className="absolute inset-0 rounded-full border-4 border-transparent border-r-purple-600 animate-spin"
                style={{ animationDuration: '1.5s', animationDirection: 'reverse' }}
              ></div>
              <div className="absolute inset-2 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
                <span className="text-xl md:text-2xl">🤖</span>
              </div>
            </div>
          </div>

          <h3 className="text-xl md:text-2xl font-bold text-gray-800 mb-4">Loading profiles...</h3>
          <p className="text-gray-600 mb-6">Preparing interaction options for you</p>

          {/* Indicadores de progresso */}
          <div className="flex items-center justify-center space-x-2 mb-6">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-pink-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" style={{ animationDelay: '0.6s' }}></div>
          </div>

          {/* Informações adicionais */}
          <div className="bg-gray-50 rounded-xl p-4">
            <p className="text-sm text-gray-600">
              Setting up personalized profiles for a unique experience
            </p>
          </div>
        </div>
      </BaseLayout>
    );
  }

  // Error state
  if (error) {
    return (
      <BaseLayout maxWidth="md">
        <div className="text-center">
          {/* Animated error icon */}
          <div className="relative mb-8">
            <div className="w-20 h-20 md:w-24 md:h-24 mx-auto relative">
              <div className="w-full h-full bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white text-3xl md:text-4xl shadow-lg animate-pulse">
                ⚠️
              </div>
              {/* Glow effect */}
              <div
                className="absolute inset-0 rounded-full"
                style={{
                  background: 'radial-gradient(circle, rgba(245, 158, 11, 0.3) 0%, transparent 70%)',
                  filter: 'blur(20px)',
                  animation: 'pulse 2s infinite'
                }}
              />
            </div>
          </div>

          <h3 className="text-xl md:text-2xl font-bold text-gray-800 mb-4">Oops! Something went wrong</h3>
          <p className="text-gray-600 mb-6">Unable to load profiles at the moment</p>

          {/* Error message */}
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 md:px-6 py-4 rounded-xl mb-8">
            <div className="flex items-center space-x-3">
              <span className="text-xl md:text-2xl">💡</span>
              <p className="text-sm md:text-base font-medium">{error}</p>
            </div>
          </div>

          {/* Botão de tentar novamente */}
          <button
            onClick={() => window.location.reload()}
            className="bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white px-6 md:px-8 py-3 md:py-4 rounded-xl hover:scale-105 transition-all duration-300 transform font-medium shadow-lg hover:shadow-xl active:scale-95"
          >
            <div className="flex items-center justify-center space-x-3">
              <svg className="w-4 h-4 md:w-5 md:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>Try Again</span>
            </div>
          </button>

          {/* Informações adicionais */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="bg-gray-50 rounded-xl p-4">
              <p className="text-sm text-gray-600">
                If the problem persists, check your internet connection
              </p>
            </div>
          </div>
        </div>
      </BaseLayout>
    );
  }

  return (
    <BaseLayout 
      maxWidth="6xl" 
      showBackButton={true} 
      onBack={handleBack}
      headerContent={
        <div>
          <h1 className="text-xl md:text-2xl lg:text-3xl font-bold text-gray-900">Choose your Profile</h1>
          <p className="text-gray-600 mt-1 text-sm md:text-base">Select how you would like to interact with the assistant</p>
        </div>
      }
    >
      <div className="space-y-6">
        {/* Mobile selected role indicator */}
        {selectedRole && (
          <div className="lg:hidden">
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{selectedRole.icon}</span>
                <div className="flex-1">
                  <p className="font-medium text-blue-900">{selectedRole.name}</p>
                  <p className="text-sm text-blue-700">{selectedRole.description}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Desktop selected role indicator */}
        {selectedRole && (
          <div className="hidden lg:flex items-center justify-center">
            <div className="flex items-center space-x-3 bg-blue-50 px-4 py-3 rounded-xl border border-blue-200">
              <span className="text-2xl">{selectedRole.icon}</span>
              <div>
                <p className="text-sm font-medium text-blue-900">
                  {selectedRole.name} selected
                </p>
                <p className="text-xs text-blue-700">{selectedRole.description}</p>
              </div>
            </div>
          </div>
        )}

        {/* Grid de Roles */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
          {roles.map((role, index) => (
            <div
              key={role.id}
              className="animate-fadeInUp"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <RoleCard
                role={role}
                isSelected={isRoleSelected(role.id)}
                onSelect={handleRoleSelect}
                disabled={isSelecting}
              />
            </div>
          ))}
        </div>

        {/* Botão de Continuar */}
        {selectedRole && (
          <div className="text-center pt-4">
            <button
              onClick={handleContinue}
              disabled={isSelecting}
              className={`
                relative inline-flex items-center px-8 md:px-10 py-4 md:py-5 rounded-2xl font-medium text-white transition-all duration-300 transform
                ${isSelecting 
                  ? 'bg-gray-400 cursor-not-allowed scale-95' 
                  : 'bg-gradient-to-r hover:scale-105 shadow-lg hover:shadow-2xl active:scale-95'
                }
              `}
              style={{
                background: isSelecting 
                  ? undefined 
                  : `linear-gradient(135deg, ${selectedRole.color}, ${selectedRole.color}dd)`
              }}
            >
              {isSelecting ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 md:h-6 md:w-6 border-b-2 border-white mr-3"></div>
                  <span>Loading...</span>
                </>
              ) : (
                <>
                  <span className="mr-3">Continue as</span>
                  <span className="text-xl md:text-2xl mr-3 animate-pulse">{selectedRole.icon}</span>
                  <span className="font-semibold">{selectedRole.name}</span>
                  <svg className="w-5 h-5 md:w-6 md:h-6 ml-3 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </>
              )}
            </button>
          </div>
        )}

        {/* Informações adicionais */}
        <div className="text-center pt-6">
          <div className="relative bg-white rounded-2xl p-6 md:p-8 shadow-lg border border-gray-200 max-w-2xl mx-auto">
            <div className="text-3xl md:text-4xl mb-4 animate-bounceYZ">💡</div>
            <h3 className="text-lg md:text-xl font-bold text-gray-900 mb-3">Tip</h3>
            <p className="text-gray-600 text-sm md:text-base leading-relaxed mb-4">
              You can switch profiles at any time during the conversation. 
              Each profile offers a personalized experience based on your context.
            </p>
            
            {/* Indicadores visuais */}
            <div className="flex items-center justify-center space-x-4 text-xs text-gray-500">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span>Personalized</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '0.5s' }}></div>
                <span>Interactive</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" style={{ animationDelay: '1s' }}></div>
                <span>Flexible</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </BaseLayout>
  );
};

export default RoleSelector; 