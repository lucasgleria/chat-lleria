// Fallback data for roles in case the backend is not available
// Contains only essential UI data - detailed configuration is loaded from backend
export const fallbackRoles = [
  {
    "id": "recruiter",
    "name": "Recruiter/HR",
    "description": "Specialized in recruitment and selection information",
    "icon": "👔",
    "color": "#3B82F6"
  },
  {
    "id": "developer",
    "name": "Developer/Technical",
    "description": "Focused on technical skills and code knowledge",
    "icon": "💻",
    "color": "#10B981"
  },
  {
    "id": "student",
    "name": "Student/Beginner",
    "description": "Focused on academic background and growth potential",
    "icon": "🎓",
    "color": "#F59E0B"
  },
  {
    "id": "client",
    "name": "Client/Partner",
    "description": "Focused on delivery capability and added value",
    "icon": "🤝",
    "color": "#8B5CF6"
  }
];

// Function to get role by ID
export const getRoleById = (id) => {
  return fallbackRoles.find(role => role.id === id);
};

// Function to get example questions by role (returns empty array for fallback)
export const getRoleExamples = (roleId) => {
  return [];
}; 