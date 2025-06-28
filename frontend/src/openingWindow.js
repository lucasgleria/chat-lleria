import React, { useState } from "react";
import BaseLayout from "./components/BaseLayout";

function OpeningWindow({ onStartQuestion }) {
  const [isHovered, setIsHovered] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleStartClick = async () => {
    setIsLoading(true);
    // Simular um pequeno delay para feedback visual
    await new Promise(resolve => setTimeout(resolve, 300));
    onStartQuestion();
  };

  return (
    <BaseLayout maxWidth="2xl">
      <div className="text-center">
        {/* Ícone animado */}
        <div className="relative mb-8">
          <div className="relative">
            <img
              src="/chatbot.png"
              alt="Chat Icon"
              className={`w-24 h-24 md:w-32 md:h-32 mx-auto transform transition-all duration-500 ${
                isHovered ? 'scale-110 rotate-3' : 'scale-100'
              } animate-bounceYZ`}
              onError={(e) => { 
                e.target.onerror = null; 
                e.target.src="https://placehold.co/128x128/3B82F6/ffffff?text=🤖"; 
              }}
            />
            
            {/* Efeito de brilho */}
            <div
              className={`absolute inset-0 rounded-full transition-opacity duration-500 ${
                isHovered ? 'opacity-100' : 'opacity-0'
              }`}
              style={{
                background: 'radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%)',
                filter: 'blur(20px)'
              }}
            />
          </div>
        </div>

        {/* Título com gradiente */}
        <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
          <span className="text-gray-900">Welcome to </span>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 animate-gradient">
            Chat lleria
          </span>
        </h1>

        {/* Descrição */}
        <div className="mb-8 md:mb-10">
          <p className="text-lg md:text-xl text-gray-700 leading-relaxed mb-4">
            Do you want to know more about Lucas?
          </p>
          <p className="text-base md:text-lg text-gray-600">
            First let's customize your experience!
          </p>
        </div>

        {/* Botão principal */}
        <div className="relative">
          <button
            onClick={handleStartClick}
            disabled={isLoading}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            className={`
              relative px-8 md:px-12 py-4 md:py-5 text-lg md:text-xl font-semibold rounded-2xl transition-all duration-300 transform
              ${isLoading 
                ? 'bg-gray-400 cursor-not-allowed scale-95' 
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 hover:scale-105 shadow-lg hover:shadow-2xl active:scale-95'
              }
              text-white
            `}
          >
            {isLoading ? (
              <div className="flex items-center justify-center space-x-3">
                <div className="animate-spin rounded-full h-5 w-5 md:h-6 md:w-6 border-b-2 border-white"></div>
                <span>Preparing...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-3">
                <span>Customize</span>
                <svg 
                  className={`w-5 h-5 md:w-6 md:h-6 transition-transform duration-300 ${isHovered ? 'translate-x-2' : ''}`} 
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
        <div className="mt-8 md:mt-12 pt-6 md:pt-8 border-t border-gray-200">
          <div className="flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-6 text-sm text-gray-500">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Personalized</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '0.5s' }}></div>
              <span>Intelligent</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '1s' }}></div>
              <span>Interactive</span>
            </div>
          </div>
        </div>
      </div>
    </BaseLayout>
  );
}

export default OpeningWindow;