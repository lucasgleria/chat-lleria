import React, { useState } from 'react';
import './App.css';
import ChatWindow from './chatWindow';
import OpeningWindow from './openingWindow';
import QuestionWindow from './questionWindow';
import RoleSelector from './components/RoleSelector';
import { RoleProvider } from './components/RoleContext';

function App() {
  // We'll use 'currentScreen' to manage which component is rendered.
  // Possible values: 'welcome', 'question1', 'roleSelect', 'chat'
  const [currentScreen, setCurrentScreen] = useState('welcome');

  // Function to navigate from the Welcome screen to the Question 1 screen
  const handleStartQuestion = () => {
    setCurrentScreen('question1');
  };

  // Function to navigate from the Question 1 screen to the Role Selection screen
  const handleAnswerSelected = () => {
    setCurrentScreen('roleSelect');
  };

  // Function to navigate from Role Selection to Chat
  const handleRoleSelected = () => {
    setCurrentScreen('chat');
  };

  // Function to go back from Role Selection to Question
  const handleBackToQuestion = () => {
    setCurrentScreen('question1');
  };

  // Function to go back from Chat to Role Selection
  const handleBackToRoleSelect = () => {
    setCurrentScreen('roleSelect');
  };

  return (
    <RoleProvider>
      <div className="App min-h-screen flex items-center justify-center bg-gray-100">
        {currentScreen === 'welcome' && (
          // Render the OpeningWindow (Welcome screen)
          // Pass handleStartQuestion to it, so its button can change the screen
          <OpeningWindow onStartQuestion={handleStartQuestion} />
        )}

        {currentScreen === 'question1' && (
          // Render the QuestionWindow (Question 1 screen)
          // Pass handleAnswerSelected to it, so its buttons can change the screen
          <QuestionWindow onAnswerSelected={handleAnswerSelected} />
        )}

        {currentScreen === 'roleSelect' && (
          // Render the RoleSelector screen
          <RoleSelector 
            onRoleSelected={handleRoleSelected}
            onBack={handleBackToQuestion}
          />
        )}

        {currentScreen === 'chat' && (
          // Render the ChatWindow when currentScreen is 'chat'
          <ChatWindow onBackToRoleSelect={handleBackToRoleSelect} />
        )}
      </div>
    </RoleProvider>
  );
}

export default App;