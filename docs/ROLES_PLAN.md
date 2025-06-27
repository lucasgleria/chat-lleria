# 🎭 Custom Roles System - Gemini ChatBot

## 📋 Implementation Overview

The roles system will allow the chatbot to adapt its answers based on the user's profile (Recruiter, Developer, Student, etc.), providing more relevant information and in the appropriate tone for each audience.

### 🎯 Objectives
- **Personalization**: Answers tailored to the user's profile
- **Relevance**: More useful information for each context
- **Experience**: Improved UX with intuitive role selection
- **Scalability**: Flexible system to add new roles

## 🏗️ Proposed Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Gemini API    │
│                 │    │                 │    │                 │
│ 1. Welcome      │───►│ 1. Role Handler │───►│ 1. Role-based   │
│ 2. Role Select  │    │ 2. Prompt Gen   │    │    Prompts      │
│ 3. Chat         │    │ 3. Response Mod │    │ 2. Contextual   │
└─────────────────┘    └─────────────────┘    │   Responses     │
                                              └─────────────────┘
```

### 🔄 Data Flow
1. **User selects role** on the selection screen
2. **Frontend sends role** along with the question
3. **Backend loads** the specific role configuration
4. **System generates personalized prompt** based on the role
5. **Gemini API responds** with role context
6. **Frontend displays answer** with visual role indicator

## 🎭 Proposed Roles

### 1. **Recruiter/HR** 👔
- **Focus**: Professional experience, soft skills, cultural fit
- **Tone**: Professional, results-oriented
- **Priority Information**: 
  - Professional experience
  - Highlighted projects
  - Soft skills and teamwork
  - Relevant certifications
  - Career goals

### 2. **Developer/Technical** 💻
- **Focus**: Technical skills, tech stack, projects
- **Tone**: Technical, detailed, code-focused
- **Priority Information**:
  - Programming languages
  - Frameworks and technologies
  - Project architecture
  - Code and implementations
  - Solved technical challenges

### 3. **Student/Beginner** 🎓
- **Focus**: Academic background, learning, potential
- **Tone**: Motivational, educational, encouraging
- **Priority Information**:
  - Academic background
  - Certifications and courses
  - Academic projects
  - Growth potential
  - Learning interests

### 4. **Client/Partner** 🤝
- **Focus**: Delivery capability, completed projects, value
- **Tone**: Commercial, focused on results and benefits
- **Priority Information**:
  - Delivered projects
  - Quantifiable results
  - Practical skills
  - Delivery capability
  - Added value

## 📁 Proposed File Structure

```
Gemini-ChatBot/
├── backend/
│   ├── data/
│   │   ├── curriculo.json
│   │   ├── system_instruction.json
│   │   └── roles/
│   │       ├── recruiter.json
│   │       ├── developer.json
│   │       ├── student.json
│   │       └── client.json
│   ├── utils/
│   │   ├── role_handler.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RoleSelector.js
│   │   │   ├── RoleCard.js
│   │   │   └── RoleContext.js
│   │   └── data/
│   │       └── roles.js
│   └── ...
└── roles_plan.md
```

## 🗂️ Roles Data Structure

### JSON Schema for Roles

```json
{
  "id": "role_identifier",
  "name": "Role Name",
  "description": "Role description",
  "icon": "emoji_icon",
  "color": "#hex_color",
  "focus_areas": [
    "area1",
    "area2",
    "area3"
  ],
  "tone": "tone_description",
  "prompt_modifiers": {
    "prefix": "Prefix instruction",
    "emphasis": [
      "Item 1",
      "Item 2"
    ],
    "avoid": [
      "Item to avoid 1",
      "Item to avoid 2"
    ]
  },
  "example_questions": [
    "Example question 1",
    "Example question 2"
  ]
}
```

### Example: Recruiter Role

```json
{
  "id": "recruiter",
  "name": "Recruiter/HR",
  "description": "Specialized in recruitment and selection information",
  "icon": "👔",
  "color": "#3B82F6",
  "focus_areas": [
    "professional_experience",
    "soft_skills", 
    "highlighted_projects",
    "certifications",
    "career_goals"
  ],
  "tone": "professional",
  "prompt_modifiers": {
    "prefix": "You are talking to a recruiter. Focus on:",
    "emphasis": [
      "Quantifiable results",
      "Relevant experience",
      "Transferable skills",
      "Growth potential",
      "Teamwork"
    ],
    "avoid": [
      "Very specific technical details",
      "Advanced programming jargon",
      "Unnecessary personal information"
    ]
  },
  "example_questions": [
    "What are Lucas's main projects?",
    "How does he work in a team?",
    "What are his career goals?",
    "What kind of challenges has he faced?"
  ]
}
```

### Example: Developer Role

```json
{
  "id": "developer",
  "name": "Developer/Technical",
  "description": "Focused on technical skills and code knowledge",
  "icon": "💻",
  "color": "#10B981",
  "focus_areas": [
    "programming_languages",
    "frameworks",
    "architecture",
    "technical_projects",
    "code_challenges"
  ],
  "tone": "technical",
  "prompt_modifiers": {
    "prefix": "You are talking to a developer. Focus on:",
    "emphasis": [
      "Technical details",
      "Tech stack",
      "Project architecture",
      "Implementation challenges",
      "Best practices"
    ],
    "avoid": [
      "Very generic information",
      "Excessive focus on soft skills",
      "Non-technical details"
    ]
  },
  "example_questions": [
    "What tech stack does he use?",
    "How does he structure his projects?",
    "What technical challenges has he solved?",
    "What code patterns does he follow?"
  ]
}
```

## 🔄 Implementation Flow

### **Phase 1: Data Structure and Backend (Week 1)**

#### 1.1 Create Roles Structure
- [ ] Create folder `backend/data/roles/`
- [ ] Define JSON schema for each role
- [ ] Create configuration files for each role
- [ ] Implement schema validation

#### 1.2 Develop Role Handler
- [ ] Create `utils/role_handler.py`
- [ ] Implement function to load role configurations
- [ ] Implement role validation
- [ ] Create cache system for configurations

#### 1.3 Modify System Instructions
- [ ] Update `system_instruction.json` to support roles
- [ ] Create dynamic prompt templates
- [ ] Implement instruction selection logic
- [ ] Add fallback for default role

#### 1.4 Update API Endpoints
- [ ] Modify `/chat` endpoint to accept `role` parameter
- [ ] Implement role-based prompt generation logic
- [ ] Add role validation
- [ ] Implement error handling for invalid roles

### **Phase 2: Frontend and Interface (Week 2)**

#### 2.1 Create RoleSelector Component
- [ ] Develop `RoleSelector.js` with visual cards
- [ ] Implement role selection with visual feedback
- [ ] Add animations and transitions
- [ ] Implement mobile responsiveness

#### 2.2 Update Navigation
- [ ] Modify `App.js` to include role selection screen
- [ ] Implement flow: Welcome → Role Select → Chat
- [ ] Add persistence for selected role
- [ ] Implement back navigation to change role

#### 2.3 Integrate with Backend
- [ ] Modify `chatWindow.js` to send selected role
- [ ] Implement role context in React
- [ ] Add visual indicator for active role
- [ ] Implement role change during conversation

### **Phase 3: Personalization and Refinement (Week 3)**

#### 3.1 Develop Specialized Prompts
- [ ] Create specific prompts for each role
- [ ] Implement tone and focus variations
- [ ] Test and refine answers
- [ ] Optimize prompts based on feedback

#### 3.2 Implement Dynamic Context
- [ ] Modify conversation history to include role context
- [ ] Implement role change during conversation
- [ ] Add smooth transitions between roles
- [ ] Maintain context when changing roles

#### 3.3 Optimize UX
- [ ] Add explanatory tooltips for each role
- [ ] Implement preview of how the chatbot will respond
- [ ] Add "automatic role" option based on the first question
- [ ] Implement question suggestions by role

### **Phase 4: Testing and Documentation (Week 4)**

#### 4.1 Role-Specific Tests
- [ ] Create tests for each role
- [ ] Validate appropriate answers for each context
- [ ] Test role change during conversation
- [ ] Implement integration tests

#### 4.2 Documentation
- [ ] Update README with roles system
- [ ] Document new role configuration
- [ ] Create usage guide for developers
- [ ] Document updated API endpoints

#### 4.3 Final Refinements
- [ ] Optimize performance
- [ ] Implement cache for role configurations
- [ ] Add analytics by role
- [ ] Implement user feedback

## 🔧 Detailed Technical Implementation

### 1. **Role Handler (utils/role_handler.py)**

```python
import json
import os
from typing import Dict, Optional, List

class RoleHandler:
    def __init__(self, roles_dir: str = "data/roles"):
        self.roles_dir = roles_dir
        self.roles = self.load_roles()
        self.default_role = "recruiter"
    
    def load_roles(self) -> Dict:
        """Loads all roles from the configuration directory"""
        roles = {}
        if os.path.exists(self.roles_dir):
            for filename in os.listdir(self.roles_dir):
                if filename.endswith('.json'):
                    role_id = filename.replace('.json', '')
                    role_path = os.path.join(self.roles_dir, filename)
                    try:
                        with open(role_path, 'r', encoding='utf-8') as f:
                            roles[role_id] = json.load(f)
                    except Exception as e:
                        print(f"Error loading role {role_id}: {e}")
        return roles
    
    def get_role_config(self, role_id: str) -> Optional[Dict]:
        """Returns specific role configuration"""
        return self.roles.get(role_id, self.roles.get(self.default_role))
    
    def generate_role_prompt(self, role_id: str, base_prompt: str) -> str:
        """Generates personalized prompt based on the role"""
        role_config = self.get_role_config(role_id)
        if not role_config:
            return base_prompt
        
        modifiers = role_config.get('prompt_modifiers', {})
        
        # Build personalized prompt
        personalized_prompt = base_prompt + "\n\n"
        personalized_prompt += f"SPECIFIC CONTEXT FOR {role_config['name'].upper()}:\n"
        personalized_prompt += f"{modifiers.get('prefix', '')}\n\n"
        
        if 'emphasis' in modifiers:
            personalized_prompt += "FOCUS ON:\n"
            for item in modifiers['emphasis']:
                personalized_prompt += f"- {item}\n"
            personalized_prompt += "\n"
        
        if 'avoid' in modifiers:
            personalized_prompt += "AVOID:\n"
            for item in modifiers['avoid']:
                personalized_prompt += f"- {item}\n"
            personalized_prompt += "\n"
        
        return personalized_prompt
    
    def validate_role(self, role_id: str) -> bool:
        """Validates if the role exists"""
        return role_id in self.roles
    
    def get_all_roles(self) -> List[Dict]:
        """Returns a list of all available roles"""
        return list(self.roles.values())
    
    def get_role_examples(self, role_id: str) -> List[str]:
        """Returns example questions for the role"""
        role_config = self.get_role_config(role_id)
        return role_config.get('example_questions', []) if role_config else []
```

### 2. **Chat Endpoint Modification**

```python
# In main.py
from utils.role_handler import RoleHandler

# Initialize role handler
role_handler = RoleHandler()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()
    history = data.get("history", [])
    role = data.get("role", "recruiter")  # NEW: role parameter
    
    if not question:
        return jsonify({"answer": "Please provide your question."}), 400
    
    # Validate role
    if not role_handler.validate_role(role):
        role = "recruiter"  # Fallback to default role
    
    try:
        # Load resume
        with open("data/curriculo.json", "r", encoding="utf-8") as f:
            curriculo_data = json.load(f)
        curriculo_json_string = json.dumps(curriculo_data, indent=2, ensure_ascii=False)
        
        # Generate personalized prompt based on the role
        personalized_system_instruction = role_handler.generate_role_prompt(
            role, SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT
        )
        
        # Initialize model with personalized prompt
        chat_model = genai.GenerativeModel(
            "gemini-1.5-flash-latest",
            system_instruction=personalized_system_instruction
        )
        
        # Prepare history
        gemini_history = []
        if not history:
            gemini_history.append({
                "role": "user",
                "parts": [{"text": f"Here is the detailed résumé information in JSON format. Use this as your primary knowledge base for all responses about Lucas:\n{curriculo_json_string}"}]
            })
            gemini_history.append({"role": "user", "parts": [{"text": question}]})
        else:
            for msg in history:
                if isinstance(msg.get("parts"), list) and msg["parts"]:
                    content_text = ""
                    for part in msg["parts"]:
                        if isinstance(part, dict) and "text" in part:
                            content_text += part["text"] + " "
                    gemini_history.append({"role": msg["role"], "parts": [{"text": content_text.strip()}]})
                else:
                    gemini_history.append({"role": msg["role"], "parts": [{"text": str(msg.get("parts", ""))}]})
        
        # Send question
        chat_session = chat_model.start_chat(history=gemini_history)
        response = chat_session.send_message(question)
        answer = response.text
        
    except Exception as e:
        print(f"Unexpected error in /chat endpoint: {e}")
        answer = "An internal error occurred while processing your question. Please try again later."
        return jsonify({"answer": answer}), 500
    
    return jsonify({"answer": answer, "role": role})

# New endpoint to get available roles
@app.route("/roles", methods=["GET"])
def get_roles():
    """Returns all available roles"""
    try:
        roles = role_handler.get_all_roles()
        return jsonify({"roles": roles})
    except Exception as e:
        print(f"Error getting roles: {e}")
        return jsonify({"roles": []}), 500

# New endpoint to get example questions
@app.route("/roles/<role_id>/examples", methods=["GET"])
def get_role_examples(role_id):
    """Returns example questions for a specific role"""
    try:
        examples = role_handler.get_role_examples(role_id)
        return jsonify({"examples": examples})
    except Exception as e:
        print(f"Error getting role examples: {e}")
        return jsonify({"examples": []}), 500
```

### 3. **RoleSelector Component (Frontend)**

```javascript
// src/components/RoleSelector.js
import React, { useState, useEffect } from 'react';
import RoleCard from './RoleCard';

const RoleSelector = ({ onRoleSelect, selectedRole }) => {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    try {
      const response = await fetch('http://localhost:5000/roles');
      if (response.ok) {
        const data = await response.json();
        setRoles(data.roles);
      } else {
        throw new Error('Failed to fetch roles');
      }
    } catch (err) {
      setError('Error loading roles');
      console.error('Error fetching roles:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRoleSelect = (role) => {
    onRoleSelect(role);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-red-500 text-center">
          <p className="text-xl font-semibold mb-2">Error</p>
          <p>{error}</p>
          <button 
            onClick={fetchRoles}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">
            How can I help you today?
          </h1>
          <p className="text-lg text-gray-600">
            Select your profile so I can give you the most relevant information
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {roles.map((role) => (
            <RoleCard
              key={role.id}
              role={role}
              isSelected={selectedRole?.id === role.id}
              onClick={() => handleRoleSelect(role)}
            />
          ))}
        </div>
        
        {selectedRole && (
          <div className="mt-8 text-center">
            <button
              onClick={() => onRoleSelect(selectedRole)}
              className="px-8 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Continue with {selectedRole.name}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default RoleSelector;
```

### 4. **RoleCard Component**

```javascript
// src/components/RoleCard.js
import React from 'react';

const RoleCard = ({ role, isSelected, onClick }) => {
  return (
    <div
      className={`
        relative p-6 rounded-xl cursor-pointer transition-all duration-300 transform hover:scale-105
        ${isSelected 
          ? 'bg-white shadow-lg border-2 border-blue-500' 
          : 'bg-white shadow-md hover:shadow-lg border-2 border-transparent'
        }
      `}
      onClick={onClick}
    >
      {/* Role Icon */}
      <div className="text-center mb-4">
        <div 
          className="text-4xl mb-2"
          style={{ color: role.color }}
        >
          {role.icon}
        </div>
      </div>
      
      {/* Title */}
      <h3 className="text-xl font-semibold text-gray-800 text-center mb-2">
        {role.name}
      </h3>
      
      {/* Description */}
      <p className="text-gray-600 text-center text-sm mb-4">
        {role.description}
      </p>
      
      {/* Focus Areas */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Focus:</h4>
        <div className="flex flex-wrap gap-1">
          {role.focus_areas.slice(0, 3).map((area, index) => (
            <span
              key={index}
              className="px-2 py-1 text-xs rounded-full"
              style={{ 
                backgroundColor: `${role.color}20`,
                color: role.color 
              }}
            >
              {area.replace('_', ' ')}
            </span>
          ))}
        </div>
      </div>
      
      {/* Selection Indicator */}
      {isSelected && (
        <div className="absolute top-2 right-2">
          <div 
            className="w-6 h-6 rounded-full flex items-center justify-center"
            style={{ backgroundColor: role.color }}
          >
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </div>
        </div>
      )}
    </div>
  );
};

export default RoleCard;
```

### 5. **Role Context**

```javascript
// src/components/RoleContext.js
import React, { createContext, useContext, useState } from 'react';

const RoleContext = createContext();

export const useRole = () => {
  const context = useContext(RoleContext);
  if (!context) {
    throw new Error('useRole must be used within a RoleProvider');
  }
  return context;
};

export const RoleProvider = ({ children }) => {
  const [selectedRole, setSelectedRole] = useState(null);

  const value = {
    selectedRole,
    setSelectedRole,
  };

  return (
    <RoleContext.Provider value={value}>
      {children}
    </RoleContext.Provider>
  );
};
```

## 🎨 Interface Design

### Role Selection Screen
- **Layout**: Responsive grid of cards
- **Each Card**: Icon, title, description, theme color
- **Interaction**: Hover effects, clear visual selection
- **Responsiveness**: Adapts to mobile (1 column)

### Active Role Indicator in Chat
- **Header**: Show selected role with icon and color
- **Change Option**: Button to switch role
- **Visual Context**: Consistent colors and icons

### Example Mobile Layout
```
┌─────────────────────┐
│    How can I help   │
│    you today?       │
├─────────────────────┤
│ 👔 Recruiter/HR     │
│ Specialized in...   │
├─────────────────────┤
│ 💻 Developer        │
│ Focused on tech...  │
├─────────────────────┤
│ 🎓 Student          │
│ Academic background │
├─────────────────────┤
│ 🤝 Client/Partner   │
│ Delivery capab...   │
└─────────────────────┘
```

## 🐛 Known Issues and Solutions

### 1. **Invalid Role**
- **Problem**: User sends a role that does not exist
- **Solution**: Fallback to default role (recruiter)

### 2. **Role Change During Conversation**
- **Problem**: Context may become confusing
- **Solution**: Keep history but adapt next answers

### 3. **Performance with Multiple Roles**
- **Problem**: Loading may become slow
- **Solution**: Role configuration cache

### 4. **Mobile Responsiveness**
- **Problem**: Cards may become small
- **Solution**: Adaptive layout with horizontal scroll

## 🔄 Immediate Next Steps

### Week 1: Backend
1. **Create folder structure** `backend/data/roles/`
2. **Develop RoleHandler** with all features
3. **Create JSON files** for each role
4. **Modify `/chat` endpoint** to accept role
5. **Implement endpoints** `/roles` and `/roles/<id>/examples`

### Week 2: Frontend
1. **Create RoleSelector** with responsive design
2. **Develop RoleCard** with animations
3. **Implement RoleContext** to manage state
4. **Modify App.js** to include selection screen
5. **Update ChatWindow** to send role

### Week 3: Integration
1. **Test backend-frontend integration**
2. **Refine prompts** for each role
3. **Implement role change** during conversation
4. **Add visual indicators** for active role

### Week 4: Polish
1. **Complete tests** by role
2. **Performance optimization**
3. **Updated documentation**


## 📝 Implementation Checklist

### Backend
- [ x ] Create folder `backend/data/roles/`
- [ x ] Implement `RoleHandler` class
- [ x ] Create JSON files for each role
- [ x ] Modify `/chat` endpoint
- [ x ] Add endpoints `/roles` and `/roles/<id>/examples`
- [ x ] Implement role validation
- [ x ] Add error handling

### Frontend
- [ x ] Create `RoleSelector` component
- [ x ] Develop `RoleCard` component
- [ x ] Implement `RoleContext`
- [ x ] Modify `App.js` to include RoleSelector
- [ x ] Update `ChatWindow` to send role
- [ x ] Add visual indicator for active role
- [ x ] Implement mobile responsiveness

### Integration
- [ x ] Test backend-frontend communication
- [ x ] Validate answers by role
- [ x ] Implement role change
- [ x ] Add animations and transitions
- [ x ] Test on different devices

### Documentation
- [ x ] Update README.md
- [ x ] Document API endpoints
- [ x ] Document React components

</rewritten_file> 