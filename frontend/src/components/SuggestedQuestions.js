// import React from 'react';

// function SuggestedQuestions({ suggestions, onSuggestionClick }) {
//   if (!suggestions || suggestions.length === 0) return null;

//   return (
//     <div className="flex flex-wrap gap-2 justify-center">
//       {suggestions.slice(0, 4).map((suggestion, idx) => (
//         <button
//           key={idx}
//           type="button"
//           className="px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-sm border border-gray-200 hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-200"
//           style={{ fontWeight: 400, opacity: 0.85 }}
//           onClick={() => onSuggestionClick(suggestion)}
//         >
//           {suggestion}
//         </button>
//       ))}
//     </div>
//   );
// }

// export default SuggestedQuestions; 

// SuggestedQuestions.js

// SuggestedQuestions.js
import React from 'react';

const SuggestedQuestions = ({ suggestions, onSuggestionClick }) => {
  // Add null check to prevent errors
  if (!suggestions || suggestions.length === 0) return null;
  
  return (
    <div className="flex flex-wrap gap-1 sm:gap-2 justify-center">
      {suggestions.slice(0, 4).map((suggestion, index) => (
        <button
          key={index}
          type="button"
          onClick={() => onSuggestionClick(suggestion)}
          className="text-xs px-2 py-1 sm:px-3 sm:py-1.5 rounded-full bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-colors duration-200 truncate max-w-[150px] sm:max-w-[200px] min-h-[36px] sm:min-h-[40px] flex items-center justify-center active:scale-95 transition-transform duration-100"
          style={{ fontWeight: 400, opacity: 0.85 }}
          title={suggestion}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
};

export default SuggestedQuestions;