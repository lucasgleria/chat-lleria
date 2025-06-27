# 🤖 Gemini ChatBot - Intelligent Chat System with Roles

An AI-powered chatbot that uses the Google Gemini API to provide personalized answers about résumés, featuring a role system for different interaction contexts.

## 🎭 **NEW: Custom Role System**

The chatbot now offers **4 personalized profiles** for different types of users:

- **🕵️‍♂️ Recruiter**: Professional and objective information
- **👨‍💻 Developer**: Focus on technical skills and projects  
- **🎓 Student**: Learning and development
- **🤝 Client**: Practical solutions and benefits

Each profile customizes the assistant's responses according to its specific needs!

## 📋 Index

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [How to Use](#how-to-use)
- [Role System](#role-system)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Deploy](#deploy)
- [Contributing](#contributing)

## 🎯 Overview

This project implements an intelligent chatbot that uses the Google Gemini API to provide contextualized answers about résumés. The system includes a role mechanism that allows customizing the interaction experience based on the user's context (recruiter, developer, client, student).

### Main Features

- 🤖 **Advanced AI**: Integration with Google Gemini 1.5 Flash
- 🎭 **Role System**: 4 different interaction profiles
- 💬 **Real-Time Chat**: Responsive and modern interface
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🎨 **Modern UI/UX**: Smooth animations and intuitive design
- 🔒 **Security**: Input validation and error handling

## ✨ Features

### Frontend
- **Multi-screen Interface**: Welcome → Question → Role Selection → Chat
- **Role Selection**: Visual cards for profile choice
- **Interactive Chat**: Modern chat interface with animations
- **Responsiveness**: Adaptive design for all devices
- **Animations**: Smooth transitions and visual feedback
- **Persistence**: Remembers the selected role

### Backend
- **RESTful API**: Well-structured endpoints
- **Gemini Integration**: Communication with Google AI
- **Role System**: Dynamic profile management
- **Validation**: Filters for out-of-scope questions
- **History**: Maintains conversation context
- **Error Handling**: Robust and informative responses

## 🛠 Technologies Used

### Frontend
- **React 19.1.0**: Main framework
- **Tailwind CSS**: Styling framework
- **Axios**: HTTP client
- **Context API**: State management

### Backend
- **Python 3.x**: Main language
- **Flask**: Web framework
- **Google Generative AI**: Gemini API
- **Pipenv**: Dependency management
- **Flask-CORS**: Cross-origin resource sharing

### Infrastructure
- **JSON**: Data storage
- **Environment Variables**: Secure configurations
- **Git**: Version control

## 📁 Project Structure

```
Gemini-ChatBot/
├── backend/
│   ├── data/
│   │   ├── roles/             # Role configurations
│   │   │   └── system_instruction.json
│   │   └── curriculo.json     # Résumé data
│   ├── utils/
│   │   └── role_handler.py    # Role manager
│   ├── main.py               # Flask server
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── data/             # Static data
│   │   ├── chatWindow.js     # Chat interface
│   │   ├── openingWindow.js  # Welcome screen
│   │   └── questionWindow.js # Question screen
│   ├── public/               # Public assets
│   └── package.json
├── docs/                     # Documentation
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites

- **Node.js** (LTS version)
- **Python 3.8+**
- **Pipenv**
- **Google Cloud Account** with Gemini API enabled

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Gemini-ChatBot.git
cd Gemini-ChatBot
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pipenv install

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Activate virtual environment
pipenv shell
```

### 3. Frontend Setup

```bash
cd frontend

# Install Node.js dependencies
npm install
```

### 4. Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to the `.env` file in the backend

## 🎮 How to Use

### Start the Project

```bash
# Terminal 1 - Backend
cd backend
pipenv run python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Usage Flow

1. **Welcome Screen**: Click "Start"
2. **Initial Question**: Answer about your goal
3. **Role Selection**: Choose your interaction profile
4. **Chat**: Ask questions about the résumé

## 🎭 Role System

The system offers 4 different interaction profiles:

### 👔 Recruiter/HR
- **Focus**: Recruitment and selection
- **Areas**: Professional experience, soft skills, projects
- **Tone**: Professional and objective
- **Examples**: "What are the main projects?", "How do you work in a team?"

### 💻 Developer
- **Focus**: Technical aspects and code
- **Areas**: Technologies, architecture, methodologies
- **Tone**: Technical and detailed
- **Examples**: "Which technologies do you master?", "How do you solve technical problems?"

### 👥 Client
- **Focus**: Results and business value
- **Areas**: Deliveries, deadlines, communication
- **Tone**: Results-oriented
- **Examples**: "How do you ensure quality?", "What is your experience with deadlines?"

### 🎓 Student
- **Focus**: Learning and development
- **Areas**: Education, academic projects, growth
- **Tone**: Motivational and educational
- **Examples**: "How did you learn programming?", "What are your goals?"

## 🔌 API Endpoints

### POST `/chat`
Sends a question and receives a chatbot response.

**Request:**
```json
{
  "question": "What is Lucas's experience?",
  "history": [...],
  "role": "recruiter"
}
```

**Response:**
```json
{
  "answer": "Lucas has experience in...",
  "role": "recruiter"
}
```

### GET `/roles`
Returns all available roles.

**Response:**
```json
{
  "roles": [
    {
      "id": "recruiter",
      "name": "Recruiter/HR",
      "description": "...",
      "icon": "👔",
      "color": "#3B82F6"
    }
  ]
}
```

### GET `/roles/{role_id}/examples`
Returns example questions for a specific role.

**Response:**
```json
{
  "examples": [
    "What are the main projects?",
    "How do you work in a team?"
  ]
}
```

## 🛠 Development

### Data Structure

#### Role Configuration (JSON)
```json
{
  "id": "recruiter",
  "name": "Recruiter/HR",
  "description": "Specialized in recruitment information",
  "icon": "👔",
  "color": "#3B82F6",
  "focus_areas": ["professional_experience", "soft_skills"],
  "tone": "professional",
  "prompt_modifiers": {
    "prefix": "You are talking to a recruiter...",
    "emphasis": ["Quantifiable results", "Relevant experience"],
    "avoid": ["Very specific technical details"]
  },
  "example_questions": ["What are the main projects?"]
}
```

### Adding New Roles

1. Create a JSON file in `backend/data/roles/`
2. Follow the schema defined above
3. The system will load it automatically

### Tests

```bash
# Frontend
cd frontend
npm test
```

## 🚀 Deploy

### Backend (Render/Heroku)

1. Set environment variables
2. Deploy via Git or CLI
3. Configure CORS for the frontend domain

### Frontend (Vercel/Netlify)

1. Connect the repository
2. Set the backend URL
3. Automatic deploy

### Environment Variables

```bash
# Backend
GEMINI_API_KEY=your_api_key
FLASK_ENV=production

# Frontend
REACT_APP_API_URL=https://your-backend.herokuapp.com
```

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards

- **Python**: PEP 8
- **JavaScript**: ESLint + Prettier
- **Commits**: Conventional Commits
- **Documentation**: JSDoc for functions

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/Gemini-ChatBot/issues)
- **Documentation**: [Wiki](https://github.com/your-username/Gemini-ChatBot/wiki)
- **Email**: your-email@example.com

## 🙏 Acknowledgements

- Google Gemini API
- React Community
- Flask Community
- Tailwind CSS

---

**Developed with ❤️ by [Your Name]** 