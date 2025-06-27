// QuestionWindow.js
import React, { useState } from "react";

function QuestionWindow({ onAnswerSelected }) {
  const [isHovered, setIsHovered] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    setIsLoading(true);
    // Simular um pequeno delay para feedback visual
    await new Promise(resolve => setTimeout(resolve, 300));
    onAnswerSelected();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4">
      <div className="max-w-2xl mx-auto text-center">
        {/* Card principal com efeitos visuais */}
        <div className="relative group">
          {/* Efeito de borda animada */}
          <div className="absolute inset-0 rounded-3xl p-0.5 pointer-events-none overflow-hidden">
            <div className="absolute inset-0 rounded-3xl transition-all duration-1000 ease-out">
              <div
                className="absolute inset-0 rounded-3xl"
                style={{
                  background: `conic-gradient(from 0deg, transparent 0deg, transparent 280deg, #10B981 280deg, #10B981 300deg, #10B981 320deg, transparent 320deg, transparent 360deg)`,
                  animation: 'rotate 3s linear infinite'
                }}
              />
              <div 
                className="absolute bg-gradient-to-br from-green-50 via-white to-emerald-50" 
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
          <div className="relative bg-white rounded-3xl p-12 shadow-xl border border-gray-200 transition-all duration-500 ease-out">
            {/* Ícone animado */}
            <div className="relative mb-8">
              <div className="relative">
                <div className={`w-24 h-24 mx-auto transform transition-all duration-500 ${
                  isHovered ? 'scale-110 rotate-3' : 'scale-100'
                } animate-bounceYZ`}>
                  <div className="w-full h-full bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center text-white text-4xl shadow-lg">
                    ✨
                  </div>
                </div>
                
                {/* Efeito de brilho */}
                <div
                  className={`absolute inset-0 rounded-full transition-opacity duration-500 ${
                    isHovered ? 'opacity-100' : 'opacity-0'
                  }`}
                  style={{
                    background: 'radial-gradient(circle, rgba(16, 185, 129, 0.3) 0%, transparent 70%)',
                    filter: 'blur(20px)'
                  }}
                />
              </div>
            </div>

            {/* Título com gradiente */}
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-600">
                Before starting...
              </span>
            </h1>

            {/* Descrição */}
            <div className="mb-10">
              <p className="text-xl text-gray-700 leading-relaxed mb-4">
                Answer a quick question to personalize your experience.
              </p>
              <p className="text-lg text-gray-600">
                This will help me provide more relevant answers for you.
              </p>
            </div>

            {/* Lista de benefícios */}
            <div className="mb-10">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="flex flex-col items-center p-4 rounded-xl bg-green-50 border border-green-200">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
                    <span className="text-2xl">🎯</span>
                  </div>
                  <h3 className="font-semibold text-green-800 mb-1">Personalized</h3>
                  <p className="text-sm text-green-600">Responses adapted to your context</p>
                </div>
                
                <div className="flex flex-col items-center p-4 rounded-xl bg-blue-50 border border-blue-200">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-3">
                    <span className="text-2xl">⚡</span>
                  </div>
                  <h3 className="font-semibold text-blue-800 mb-1">Fast</h3>
                  <p className="text-sm text-blue-600">Just one simple question</p>
                </div>
                
                <div className="flex flex-col items-center p-4 rounded-xl bg-purple-50 border border-purple-200">
                  <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-3">
                    <span className="text-2xl">🔒</span>
                  </div>
                  <h3 className="font-semibold text-purple-800 mb-1">Secure</h3>
                  <p className="text-sm text-purple-600">Your data is confidential</p>
                </div>
              </div>
            </div>

            {/* Botão principal */}
            <div className="relative">
              <button
                onClick={handleContinue}
                disabled={isLoading}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className={`
                  relative px-12 py-5 text-xl font-semibold rounded-2xl transition-all duration-300 transform
                  ${isLoading 
                    ? 'bg-gray-400 cursor-not-allowed scale-95' 
                    : 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 hover:scale-105 shadow-lg hover:shadow-2xl active:scale-95'
                  }
                  text-white
                `}
              >
                {isLoading ? (
                  <div className="flex items-center justify-center space-x-3">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                    <span>Preparing...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-3">
                    <span>Continue</span>
                    <svg 
                      className={`w-6 h-6 transition-transform duration-300 ${isHovered ? 'translate-x-2' : ''}`} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </div>
                )}
              </button>

              {/* Efeito de brilho no botão */}
              {!isLoading && (
                <div
                  className={`absolute inset-0 rounded-2xl opacity-0 transition-opacity duration-500 pointer-events-none overflow-hidden ${
                    isHovered ? 'opacity-100' : ''
                  }`}
                >
                  <div
                    className="absolute inset-0"
                    style={{
                      background: 'linear-gradient(135deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%)',
                      transform: 'translateX(-100%)',
                      animation: 'shimmer 2s infinite'
                    }}
                  />
                </div>
              )}
            </div>

            {/* Informações adicionais */}
            <div className="mt-12 pt-8 border-t border-gray-200">
              <div className="bg-gray-50 rounded-xl p-6">
                <div className="flex items-center justify-center space-x-2 mb-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium text-gray-700">Quick and simple process</span>
                </div>
                <p className="text-sm text-gray-600">
                  Takes only a few seconds to set up your personalized experience
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Custom CSS for animations */}
      <style>{`
        /* Animações específicas que não estão no CSS global */
      `}</style>
    </div>
  );
}

export default QuestionWindow;