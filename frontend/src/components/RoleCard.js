import React from 'react';

const RoleCard = ({ role, isSelected, onSelect, disabled = false }) => {
  const handleClick = () => {
    if (!disabled) {
      onSelect(role.id);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  return (
    <div
      className={`
        relative group cursor-pointer transition-all duration-300 ease-in-out transform
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 active:scale-95'}
        ${isSelected 
          ? 'shadow-xl scale-105' 
          : 'hover:shadow-lg hover:shadow-gray-200'
        }
      `}
      onClick={handleClick}
      onKeyPress={handleKeyPress}
      tabIndex={disabled ? -1 : 0}
      role="button"
      aria-label={`Select profile: ${role.name}`}
      aria-pressed={isSelected}
    >
      {/* Efeito de borda animada - sempre presente mas com transições suaves */}
      <div 
        className={`
          absolute inset-0 rounded-2xl p-0.5 pointer-events-none overflow-hidden
          transition-all duration-700 ease-out
          ${isSelected 
            ? 'opacity-100 scale-100' 
            : 'opacity-0 scale-95'
          }
        `}
      >
        {/* Traço rodando na borda */}
        <div
          className={`
            absolute inset-0 rounded-2xl p-0.5 pointer-events-none overflow-hidden
            transition-all duration-1000 ease-out
            ${isSelected 
              ? 'opacity-100 scale-100' 
              : 'opacity-0 scale-95'
            }
          `}
        >
          <div
            className={`
              absolute inset-0 rounded-2xl transition-all duration-1000 ease-out
              ${isSelected ? 'opacity-100' : 'opacity-0'}
            `}
          >
            {/* Primeiro traço */}
            <div
              className="absolute inset-0 rounded-2xl"
              style={{
                background: `conic-gradient(from 0deg, transparent 0deg, transparent 280deg, ${role.color}20 280deg, ${role.color} 300deg, ${role.color} 320deg, ${role.color}20 320deg, transparent 340deg, transparent 360deg)`, 
                animation: isSelected ? 'rotate 2.5s linear infinite' : 'none'
              }}
            />
            
            {/* Segundo traço (lado oposto) */}
            <div
              className="absolute inset-0 rounded-2xl"
              style={{
                background: `conic-gradient(from 90deg, transparent 0deg, transparent 280deg, ${role.color}20 280deg, ${role.color} 300deg, ${role.color} 320deg, ${role.color}20 320deg, transparent 340deg, transparent 360deg)`,
                animation: isSelected ? 'rotate 2.5s linear infinite' : 'none'
              }}
            />

            {/* Terceiro traço (lado oposto) */}
            <div
              className="absolute inset-0 rounded-2xl"
              style={{
                background: `conic-gradient(from 180deg, transparent 0deg, transparent 280deg, ${role.color}20 280deg, ${role.color} 300deg, ${role.color} 320deg, ${role.color}20 320deg, transparent 340deg, transparent 360deg)`,
                animation: isSelected ? 'rotate 2.5s linear infinite' : 'none'
              }}
            />

            {/* Quarto traço (lado oposto) */}
            <div
              className="absolute inset-0 rounded-2xl"
              style={{
                background: `conic-gradient(from 270deg, transparent 0deg, transparent 280deg, ${role.color}20 280deg, ${role.color} 300deg, ${role.color} 320deg, ${role.color}20 320deg, transparent 340deg, transparent 360deg)`,
                animation: isSelected ? 'rotate 2.5s linear infinite' : 'none'
              }}
            />
            
            <div 
              className="absolute bg-white" 
              style={{
                top: '2px',
                left: '2px',
                right: '2px',
                bottom: '2px',
                borderRadius: '1rem !important',
                borderTopLeftRadius: '1rem !important',
                borderTopRightRadius: '1rem !important',
                borderBottomLeftRadius: '1rem !important',
                borderBottomRightRadius: '1rem !important',
                zIndex: 10
              }}
            />
          </div>
        </div>
      </div>

      {/* Card principal */}
      <div
        className={`
          relative bg-white rounded-2xl p-4 md:p-6 border-2 transition-all duration-900 ease-out h-full
          ${isSelected 
            ? 'border-transparent bg-gradient-to-br from-blue-50 to-blue-100' 
            : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
          }
        `}
        style={{
          background: isSelected 
            ? `linear-gradient(135deg, ${role.color}15, ${role.color}05)`
            : 'white',
          borderRadius: '1rem',
          borderTopLeftRadius: '1rem',
          borderTopRightRadius: '1rem',
          borderBottomLeftRadius: '1rem',
          borderBottomRightRadius: '1rem'
        }}
      >
        {/* Header com ícone e nome */}
        <div className="flex items-center space-x-2 md:space-x-3 mb-3 md:mb-4">
          <div
            className="text-2xl md:text-3xl transition-all duration-300 group-hover:scale-110 group-hover:rotate-3"
            style={{ color: role.color }}
          >
            {role.icon}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-base md:text-lg font-bold text-gray-900 group-hover:text-gray-700 truncate">
              {role.name}
            </h3>
            <div 
              className="text-xs md:text-sm font-medium"
              style={{ color: role.color }}
            >
              {role.tone}
            </div>
          </div>
          
          {/* Indicador de seleção */}
          {isSelected && (
            <div 
              className="w-5 h-5 md:w-6 md:h-6 rounded-full flex items-center justify-center animate-pulse"
              style={{ backgroundColor: role.color }}
            >
              <svg className="w-3 h-3 md:w-4 md:h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
          )}
        </div>

        {/* Descrição */}
        <p className="text-gray-600 text-xs md:text-sm mb-3 md:mb-4 leading-relaxed line-clamp-3">
          {role.description}
        </p>

        {/* Focus Areas */}
        <div className="mb-3 md:mb-4">
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Focus Areas
          </h4>
          <div className="flex flex-wrap gap-1 md:gap-1.5">
            {role.focus_areas.slice(0, 3).map((area, index) => (
              <span
                key={index}
                className="px-2 md:px-2.5 py-1 text-xs rounded-full font-medium transition-all duration-200 hover:scale-105"
                style={{
                  backgroundColor: `${role.color}20`,
                  color: role.color
                }}
              >
                {area.replace('_', ' ')}
              </span>
            ))}
            {role.focus_areas.length > 3 && (
              <span className="px-2 py-1 text-xs text-gray-500 bg-gray-100 rounded-full">
                +{role.focus_areas.length - 3} more
              </span>
            )}
          </div>
        </div>

        {/* Exemplos de perguntas */}
        <div className="relative group/tooltip">
          <button
            className="text-xs text-gray-500 hover:text-gray-700 transition-colors duration-200 flex items-center space-x-1"
            onClick={(e) => e.stopPropagation()}
          >
            <span>See examples</span>
            <svg className="w-3 h-3 transition-transform group-hover/tooltip:translate-x-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
          </button>
          
          {/* Tooltip melhorado */}
          <div className="absolute bottom-full left-0 right-0 mb-3 p-3 md:p-4 bg-gray-900 text-white text-xs rounded-xl opacity-0 invisible group-hover/tooltip:opacity-100 group-hover/tooltip:visible transition-all duration-300 z-10 shadow-2xl">
            <div className="font-bold mb-2 md:mb-3 text-blue-300">💡 Example questions:</div>
            <ul className="space-y-1 md:space-y-2">
              {role.example_questions.slice(0, 3).map((question, index) => (
                <li key={index} className="text-gray-300 leading-relaxed">
                  • {question}
                </li>
              ))}
            </ul>
            <div className="absolute top-full left-6 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
          </div>
        </div>

        {/* Badge de seleção */}
        {isSelected && (
          <div className="absolute top-2 md:top-3 right-2 md:right-3">
            <div 
              className="w-2 h-2 md:w-3 md:h-3 rounded-full animate-ping"
              style={{ backgroundColor: role.color }}
            ></div>
          </div>
        )}
      </div>

      {/* Efeito de brilho no hover */}
      {!disabled && (
        <div
          className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none overflow-hidden"
        >
          <div
            className="absolute inset-0"
            style={{
              background: `linear-gradient(135deg, transparent 30%, ${role.color}15 50%, transparent 70%)`,
              transform: 'translateX(-100%)',
              animation: 'shimmer 2s infinite'
            }}
          />
        </div>
      )}

      <style>{`
        @keyframes rotate {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
        
        @keyframes shimmer {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(100%);
          }
        }
      `}</style>
    </div>
  );
};

export default RoleCard;