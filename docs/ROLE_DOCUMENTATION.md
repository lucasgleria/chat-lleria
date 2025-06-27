# 📚 Complete Implementation of the Roles System

## Summary
- [1. Context and Motivation](#1-context-and-motivation)
- [2. Objective of the Roles Implementation](#2-objective-of-the-roles-implementation)
- [3. Before and After: What Changed?](#3-before-and-after-what-changed)
- [4. Architecture Decisions](#4-architecture-decisions)
- [5. File and Data Structure](#5-file-and-data-structure)
- [6. Scripts, Endpoints, and Components](#6-scripts-endpoints-and-components)
- [7. Complete Roles Flow (Backend and Frontend)](#7-complete-roles-flow-backend-and-frontend)
- [8. Usage Examples and Tests](#8-usage-examples-and-tests)
- [9. References and Code Snippets](#9-references-and-code-snippets)

---

## 1. Context and Motivation

**Before roles:**
- The chatbot answered questions about the resume in a single way, without considering the user's profile.
- The system was monolithic: a single prompt logic, with no context, tone, or focus customization.
- There was no differentiation between technical, HR, client, or student questions.

**Motivation:**
- Make the chatbot smarter by adapting answers to the user's profile.
- Allow multiple usage contexts (recruiter, developer, client, student).
- Improve user experience and system usefulness.

---

## 2. Objective of the Roles Implementation

- Allow the user to choose an interaction profile (role) and have the chatbot adapt its answers according to this context.
- Modularize the logic of prompts, instructions, and examples for each profile.
- Facilitate future maintenance and expansion (new profiles, behavior adjustments, etc).

---

## 3. Before and After: What Changed?

### Before
- Single, generic prompt for all questions.
- No context differentiation.
- Coupled and inflexible code.

### After
- **Dynamic roles system**: multiple profiles, each with its own focus, tone, examples, and instructions.
- **JSON files** for each role, easily editable and expandable.
- **RoleHandler** centralizing all role logic in the backend.
- **REST endpoints** for querying roles and examples.
- **Frontend** with visual profile selection, animated cards, and persistent context.
- **Automated tests** to ensure integrity.

---

## 4. Architecture Decisions

- **Separation of responsibilities**: backend handles logic and role data, frontend handles user experience.
- **JSON as the source of truth**: each role is a JSON file, making maintenance and versioning easier.
- **RoleHandler**: dedicated class for loading, validating, caching, and generating personalized prompts.
- **RESTful Endpoints**: `/roles`, `/roles/<role_id>/examples`, and `/chat` with role support.
- **Context API in the frontend**: global management of the selected profile.
- **Responsive and accessible design**: consistent experience on any device.

---

## 5. File and Data Structure

```
backend/
  ├── main.py                  # Flask Endpoints
  ├── utils/
  │   └── role_handler.py      # RoleHandler Class
  └── data/
      ├── curriculo.json       # Base resume
      ├── system_instruction.json # System instructions
      └── roles/
          ├── recruiter.json   # Recruiter profile
          ├── developer.json   # Developer profile
          ├── client.json      # Client profile
          └── student.json     # Student profile
frontend/
  └── src/
      ├── components/
      │   ├── RoleContext.js   # Global roles context
      │   ├── RoleSelector.js  # Visual profile selection
      │   └── RoleCard.js      # Animated role card
      ├── chatWindow.js        # Chat integrated with roles
      └── index.css            # Styles and animations
```

### Example of a role file (`recruiter.json`):
```json
{
  "id": "recruiter",
  "name": "Recruiter/HR",
  "description": "Specialized in recruitment and selection information",
  "icon": "👔",
  "color": "#3B82F6",
  "focus_areas": ["experiencia_profissional", "soft_skills", "projetos_destaque"],
  "tone": "professional",
  "prompt_modifiers": {
    "prefix": "You are talking to a recruiter. Focus on:",
    "emphasis": ["Quantifiable results", "Relevant experience"],
    "avoid": ["Very specific technical details"]
  },
  "example_questions": [
    "What are Lucas's main projects?",
    "How does he work in a team?"
  ]
}
```

---

## 6. Scripts, Endpoints, and Components

### **Backend**
- **`utils/role_handler.py`**: Central class for roles (loading, validation, prompt generation, examples, cache).
- **`main.py`**:
  - Endpoint `/chat`: now receives the `role` parameter and generates a personalized prompt.
  - Endpoint `/roles`: returns all available roles.
  - Endpoint `/roles/<role_id>/examples`: returns example questions for the role.

### **Frontend**
- **`components/RoleContext.js`**: Global context for role selection and persistence.
- **`components/RoleSelector.js`**: Profile selection screen, animated cards, context integration.
- **`components/RoleCard.js`**: Visual and responsive card for each role, with example tooltips.
- **`chatWindow.js`**: Integrated chat, sends selected role to backend, displays visual context.
- **`index.css`**: Animations, responsiveness, and styles for roles.

---

## 7. Complete Roles Flow (Backend and Frontend)

### **1. Profile Selection (Frontend)**
- User chooses a profile on the selection screen (`RoleSelector`), which updates the global context (`RoleContext`).
- The selected profile is persisted in `localStorage`.

### **2. Sending a Question (Frontend → Backend)**
- When sending a message in the chat, the frontend includes the selected `role.id` in the request to `/chat`.

### **3. Personalized Prompt Generation (Backend)**
- The backend validates the received role.
- The `RoleHandler` loads the role settings and generates a personalized prompt, including prefixes, emphases, and restrictions.
- The prompt is sent to Gemini along with the resume and conversation history.

### **4. Response and Display (Backend → Frontend)**
- The backend returns Gemini's response, already adapted to the profile.
- The frontend displays the answer, highlighting the active profile.
- The user can switch profiles at any time, changing the conversation context.

---

## 8. Usage Examples and Tests

### **Example Request to `/chat`**
```json
{
  "question": "What are the main projects?",
  "history": [...],
  "role": "recruiter"
}
```

### **Example Response**
```json
{
  "answer": "Lucas worked on projects such as...",
  "role": "recruiter"
}
```
---

## 9. References and Code Snippets

### **RoleHandler (backend/utils/role_handler.py)**
```python
class RoleHandler:
    def __init__(self, roles_dir: str = None):
        ...
    def load_roles(self) -> Dict:
        ...
    def generate_role_prompt(self, role_id: str, base_prompt: str) -> str:
        ...
    def validate_role(self, role_id: str) -> bool:
        ...
    def get_all_roles(self) -> List[Dict]:
        ...
```

### **Endpoint /chat (backend/main.py)**
```python
@app.route("/chat", methods=["POST"])
def chat():
    ...
    role = data.get("role", "recruiter")
    if not role_handler.validate_role(role):
        role = "recruiter"
    personalized_system_instruction = role_handler.generate_role_prompt(role, SYSTEM_INSTRUCTION_FOR_Lucas_CHATBOT)
    ...
```

### **RoleSelector (frontend/src/components/RoleSelector.js)**
```jsx
const RoleSelector = ({ onRoleSelected, onBack }) => {
  ...
  return (
    <div className="...">
      {/* Roles Grid */}
      <div className="grid ...">
        {roles.map((role) => (
          <RoleCard ... />
        ))}
      </div>
      ...
    </div>
  );
};
```

</rewritten_file> 