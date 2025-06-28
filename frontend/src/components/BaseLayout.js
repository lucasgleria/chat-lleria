import React from 'react';

const BaseLayout = ({ children, className = "", maxWidth = "2xl", showBackButton = false, onBack, headerContent }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4">
      <div className={`w-full max-w-${maxWidth} mx-auto`}>
        {/* Container principal com tamanho consistente */}
        <div className="relative group">
          {/* Efeito de borda animada */}
          <div className="absolute inset-0 rounded-3xl p-0.5 pointer-events-none overflow-hidden">
            <div className="absolute inset-0 rounded-3xl transition-all duration-1000 ease-out">
              <div
                className="absolute inset-0 rounded-3xl"
                style={{
                  background: `conic-gradient(from 0deg, transparent 0deg, transparent 280deg, #3B82F6 280deg, #3B82F6 300deg, #3B82F6 320deg, transparent 320deg, transparent 360deg)`,
                  animation: 'rotate 3s linear infinite'
                }}
              />
              <div 
                className="absolute bg-gradient-to-br from-blue-50 via-white to-indigo-50" 
                style={{
                  top: '2px',
                  left: '2px',
                  right: '2px',
                  bottom: '2px',
                  borderRadius: '1.5rem'
                }}
              />
            </div>
          </div>

          {/* Conteúdo principal */}
          <div className={`relative bg-white rounded-3xl shadow-xl border border-gray-200 transition-all duration-500 ease-out ${className}`}>
            {/* Header opcional */}
            {headerContent && (
              <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 rounded-t-3xl">
                <div className="flex items-center justify-between">
                  {showBackButton && (
                    <button
                      onClick={onBack}
                      className="text-gray-600 hover:text-gray-800 transition-colors duration-200 p-2 rounded-lg hover:bg-gray-100"
                      aria-label="Voltar"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                      </svg>
                    </button>
                  )}
                  <div className="flex-1">
                    {headerContent}
                  </div>
                </div>
              </div>
            )}

            {/* Conteúdo principal */}
            <div className="p-6 md:p-8 lg:p-12">
              {children}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BaseLayout; 