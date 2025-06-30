import React from 'react';

function SuggestedQuestions({ suggestions, onSuggestionClick }) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 justify-center">
      {suggestions.slice(0, 4).map((suggestion, idx) => (
        <button
          key={idx}
          type="button"
          className="px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-sm border border-gray-200 hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-200"
          style={{ fontWeight: 400, opacity: 0.85 }}
          onClick={() => onSuggestionClick(suggestion)}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
}

export default SuggestedQuestions; 