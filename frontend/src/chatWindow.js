import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useRole } from './components/RoleContext';

function ChatWindow({ onBackToRoleSelect }) {
  const { selectedRole } = useRole();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Effect to scroll to the bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Effect to adjust textarea height and scroll to bottom when message changes
  useEffect(() => {
    adjustTextareaHeight();
    scrollToBottom();
  }, [message]);

  // Effect to focus the textarea when the component mounts or after sending a message
  useEffect(() => {
    if (!loading && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [loading]);

  // Function to scroll to the bottom of the chat window
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Function to adjust the textarea height based on content
  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      const lineHeight = parseFloat(getComputedStyle(textareaRef.current).lineHeight);
      const maxRows = 5;
      const maxHeight = lineHeight * maxRows;
      textareaRef.current.style.height = `${Math.min(scrollHeight, maxHeight)}px`;
    }
  };

  // Handle sending a message
  const handleSendMessage = async () => {
    if (message.trim()) {
      const userMessageText = message.trim();

      // Add the user's message to the state immediately
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(), // Use timestamp for unique ID
          sender: 'You',
          text: userMessageText,
          timestamp: new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
          })
        },
      ]);
      setMessage('');

      setLoading(true);

      try {
        const conversationHistory = messages.map(msg => ({
          role: msg.sender === 'You' ? 'user' : 'model',
          parts: [{ text: msg.text }],
        }));

        const currentRequestHistory = [...conversationHistory, { role: 'user', parts: [{ text: userMessageText }] }];

        const requestData = {
          question: userMessageText,
          history: currentRequestHistory
        };

        if (selectedRole) {
          requestData.role = selectedRole.id;
        }

        const response = await axios.post('http://localhost:5000/chat', requestData, {
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (response && response.data && response.data.answer) {
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              id: Date.now() + 1,
              sender: 'Bot',
              text: response.data.answer,
              timestamp: new Date().toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })
            },
          ]);
        } else {
          console.warn('API returned an unexpected structure or an empty answer:', response);
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              id: Date.now() + 1,
              sender: 'Bot',
              text: 'Sorry, the API returned an unexpected response. Please try again.',
              isError: true,
              timestamp: new Date().toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })
            },
          ]);
        }
      } catch (error) {
        console.error('Error sending message:', error);
        let errorMessage = 'Unable to connect to server.';

        if (error.response) {
          console.error('Server response error:', error.response.data);
          console.error('Status:', error.response.status);
          if (error.response.data && error.response.data.message) {
            errorMessage = `Server error: ${error.response.data.message}`;
          } else {
            errorMessage = `Server error (Status: ${error.response.status}).`;
          }
        } else if (error.request) {
          console.error('No response received:', error.request);
          errorMessage = 'Network error: No response received from server.';
        } else {
          console.error('Error setting up request:', error.message);
          errorMessage = `An unexpected error occurred: ${error.message}.`;
        }

        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: Date.now() + 1,
            sender: 'Bot',
            text: `Sorry, an error occurred: ${errorMessage} Please try again later.`,
            isError: true,
            timestamp: new Date().toLocaleTimeString('en-US', { 
              hour: '2-digit', 
              minute: '2-digit' 
            })
          },
        ]);
      } finally {
        setLoading(false);
      }
    }
  };

  // Handle key presses in the textarea
  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      if (!loading) {
        handleSendMessage();
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200 px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => window.location.reload()}
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-all duration-200 p-2 rounded-xl hover:bg-gray-100 transform hover:scale-105"
            >
              <img
                src="/chatbot.png"
                alt="Chatbot Icon"
                className="w-8 h-8 md:w-10 md:h-10 animate-bounceYZ transform hover:scale-110 transition-transform duration-200"
                onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/40x40/cccccc/ffffff?text=BOT"; }}
              />
              <span className="hidden sm:block text-sm font-medium">Back to Menu</span>
            </button>
          </div>
          
          {selectedRole && (
            <div className="flex items-center space-x-2 bg-gradient-to-r from-blue-50 to-indigo-50 px-4 py-3 rounded-xl border border-blue-200 shadow-sm">
              <span className="text-2xl animate-pulse">{selectedRole.icon}</span>
              <div className="hidden sm:block">
                <p className="text-sm font-medium text-blue-900">{selectedRole.name}</p>
                <p className="text-xs text-blue-700">{selectedRole.description}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main chat container */}
      <div className="flex-1 max-w-4xl mx-auto w-full px-4 py-4">
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 flex flex-col h-full overflow-hidden">
          {/* Role indicator header */}
          {selectedRole && (
            <div 
              className="px-4 py-3 border-b border-gray-200 flex items-center justify-between transition-all duration-300"
              style={{ 
                background: `linear-gradient(135deg, ${selectedRole.color}08, ${selectedRole.color}15)`,
                borderBottomColor: `${selectedRole.color}20`
              }}
            >
              <div className="flex items-center space-x-3">
                <span className="text-2xl animate-pulse">{selectedRole.icon}</span>
                <div>
                  <h3 className="font-semibold text-gray-900">{selectedRole.name}</h3>
                  <p className="text-sm text-gray-600">{selectedRole.description}</p>
                </div>
              </div>
              <button
                onClick={onBackToRoleSelect}
                className="text-gray-500 hover:text-gray-700 transition-all duration-200 p-2 rounded-lg hover:bg-gray-100 transform hover:scale-105"
                title="Switch profile"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </div>
          )}

          {/* Chat messages display area */}
          <div className="flex-1 p-4 overflow-y-auto space-y-4 scroll-smooth">
            {messages.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-4">👋</div>
                <h3 className="text-lg font-medium mb-2">Welcome to Chat!</h3>
                <p className="text-sm">Ask a question about Lucas's resume to get started.</p>
              </div>
            )}
            
            {messages.map((msg, index) => (
              <div 
                key={msg.id} 
                className={`flex ${msg.sender === 'You' ? 'justify-end' : 'justify-start'} items-start animate-fadeIn`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {msg.sender === 'Bot' && (
                  <div className="flex-shrink-0 mr-3">
                    <img
                      src="/chatbot.png"
                      alt="Bot Profile"
                      className="w-8 h-8 md:w-10 md:h-10 rounded-full border-2 border-gray-200"
                      onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/40x40/cccccc/ffffff?text=BOT"; }}
                    />
                  </div>
                )}
                
                <div className="flex flex-col max-w-[85%] md:max-w-[70%]">
                  <div
                    className={`p-3 rounded-2xl shadow-sm transition-all duration-200 ${
                      msg.sender === 'You'
                        ? 'bg-blue-500 text-white rounded-br-md'
                        : msg.isError
                        ? 'bg-red-100 text-red-800 border border-red-200'
                        : 'bg-gray-100 text-gray-800 rounded-bl-md'
                    }`}
                  >
                    <p className="text-sm font-medium mb-1">
                      {msg.sender === 'You' ? 'You' : 'Assistant'}
                    </p>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                  </div>
                  <span className="text-xs text-gray-400 mt-1 px-1">
                    {msg.timestamp}
                  </span>
                </div>
              </div>
            ))}
            
            {/* "Typing..." indicator */}
            {loading && (
              <div className="flex justify-start items-start animate-fadeIn">
                <div className="flex-shrink-0 mr-3">
                  <img
                    src="/icon2.gif"
                    alt="Bot Profile"
                    className="w-8 h-8 md:w-10 md:h-10 rounded-full border-2 border-gray-200"
                    onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/40x40/cccccc/ffffff?text=BOT"; }}
                  />
                </div>
                <div className="flex flex-col max-w-[85%] md:max-w-[70%]">
                  <div className="p-3 rounded-2xl bg-gray-100 text-gray-800 rounded-bl-md shadow-sm">
                    <p className="text-sm font-medium mb-2">Assistant</p>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Message input area */}
          <div className="p-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-end space-x-3">
              <div className="flex-1 relative">
                <textarea
                  ref={textareaRef}
                  className="w-full resize-none p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
                  rows="1"
                  placeholder="Type your message..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  style={{ minHeight: '44px' }}
                />
                <div className="absolute bottom-2 right-2 text-xs text-gray-400">
                  {message.length}/1000
                </div>
              </div>
              
              <button
                className={`px-6 py-3 rounded-xl font-medium text-white transition-all duration-200 flex items-center space-x-2 shadow-sm transform ${
                  loading || !message.trim()
                    ? 'bg-gray-400 cursor-not-allowed scale-95'
                    : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 hover:scale-105 hover:shadow-lg active:scale-95'
                }`}
                onClick={handleSendMessage}
                disabled={loading || !message.trim()}
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span className="hidden sm:inline">Sending...</span>
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                      <path d="M3.478 2.405a.75.75 0 0 0-.926.94l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.543 60.543 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.543 60.543 0 0 0 3.478 2.405Z" />
                    </svg>
                    <span className="hidden sm:inline">Send</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Custom CSS for animations */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out forwards;
        }
        
        @keyframes bounceYZ {
          0%, 100% {
            transform: translateY(0) scale(1);
          }
          50% {
            transform: translateY(-5px) scale(1.05);
          }
        }
        
        .animate-bounceYZ {
          animation: bounceYZ 2s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}

export default ChatWindow;
