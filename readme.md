# CareerLM 🚀

**Your AI-Powered Career Assistant**

CareerLM is a comprehensive career development platform that helps job seekers optimize their resumes, analyze skill gaps, prepare for interviews, and accelerate their career growth. Built with modern AI technology and an intuitive interface, CareerLM provides everything you need to succeed in today's competitive job market.

## ✨ Features

### 📄 Resume Optimizer

- **ATS Score Analysis**: Get a detailed ATS compatibility score with component breakdowns
- **Gap Identification**: Discover missing keywords and qualifications
- **Alignment Suggestions**: Receive AI-powered recommendations to improve your resume
- **Real-time Analysis**: Upload your resume and job description for instant feedback

### 🎯 Skill Gap Analyzer

- **Career Path Analysis**: Identify top career matches based on your skills
- **Skills Mapping**: See matched and missing skills for each career path
- **Match Probability**: Get probability scores for different career options
- **Detailed Insights**: Comprehensive analysis of your strengths and areas for improvement

### 🎤 Mock Interview

- AI-powered interview practice tailored to your target role
- Get feedback on your responses
- Build confidence before the real interview

### ✉️ Cold Email Generator

- Create compelling outreach emails
- Personalized templates for networking
- Increase your response rates

### 📚 Study Planner

- Structured learning paths for missing skills
- Curated study materials and resources
- Project recommendations to build your portfolio
- Video tutorials and courses

### 📊 Dashboard

- Track your career development progress
- Quick access to all tools
- View resume analysis status
- Session persistence across page reloads

### 👤 User Management

- Secure authentication with Supabase
- Personal profile and settings
- Resume history tracking
- Version management for multiple resume uploads

## 🏗️ Project Structure

```
CareerLM/
├── frontend-react/          # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── Navbar.js           # Navigation bar with profile dropdown
│   │   │   ├── Sidebar.js          # Dashboard sidebar navigation
│   │   │   ├── ResumeUpload.js     # Resume upload interface
│   │   │   ├── ResumeOptimizer.js  # Resume optimization display
│   │   │   ├── SkillGapAnalyzer.js # Career and skill analysis
│   │   │   ├── StudyPlanner.js     # Learning materials display
│   │   │   ├── MockInterview.js    # Interview practice
│   │   │   ├── ColdEmailGenerator.js
│   │   │   ├── History.js          # Resume version history
│   │   │   └── ATSScore.js         # ATS score visualization
│   │   ├── pages/           # Page components
│   │   │   ├── Home.js             # Landing page
│   │   │   ├── Dashboard.js        # Main dashboard
│   │   │   └── Auth.js             # Login/Signup
│   │   ├── context/         # React Context
│   │   │   └── UserContext.js      # User session management
│   │   └── api/
│   │       └── supabaseClient.js   # Supabase configuration
│   └── package.json
│
└── backend-fastapi/         # FastAPI backend server
    ├── app/
    │   ├── main.py          # FastAPI application entry
    │   ├── api/
    │   │   └── v1/
    │   │       ├── routes_resume.py  # Resume analysis endpoints
    │   │       └── routes_user.py    # User history endpoints
    │   └── services/
    │       ├── ats_checker.py        # ATS scoring logic
    │       └── resume_optimizer.py   # Resume optimization
    ├── supabase_client.py   # Supabase Python client
    └── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **Ollama** (for local LLM inference)
- **Supabase Account** (for authentication and database)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/avogadronuggies/CareerLM.git
cd CareerLM
```

#### 2. Set Up Backend

```bash
cd backend-fastapi

# Install dependencies
pip install -r requirements.txt

# Configure Supabase
# Create a .env file or update supabase_client.py with your credentials:
# - SUPABASE_URL
# - SUPABASE_KEY

# Start the FastAPI server
python -m uvicorn app.main:app --reload
```

The backend will run on `http://localhost:8000`

#### 3. Set Up Frontend

```bash
cd frontend-react

# Install dependencies
npm install

# Configure Supabase
# Update src/api/supabaseClient.js with your Supabase credentials

# Start the React development server
npm start
```

The frontend will run on `http://localhost:3000`

#### 4. Install and Configure Ollama

```bash
# Install Ollama from https://ollama.ai

# Pull the required model
ollama pull llama3

# The backend will automatically start Ollama if needed
```

### Database Setup

CareerLM uses Supabase PostgreSQL database with the following tables:

1. **resumes** - Stores user resume information
2. **resume_versions** - Tracks multiple versions of resume analysis
3. **auth.users** - User authentication (managed by Supabase Auth)

The backend automatically creates versions when you analyze resumes, storing complete analysis in JSONB format.

## 🔌 API Endpoints

### Resume Analysis

- **POST** `/api/v1/resume/optimize`

  - Upload resume and job description
  - Returns ATS score, gaps, and alignment suggestions
  - Automatically saves to resume_versions table

- **POST** `/api/v1/resume/skill-gap-analysis`

  - Analyze career paths and skill gaps
  - Returns top career matches with probability scores

- **POST** `/api/v1/resume/generate-study-materials`
  - Generate personalized learning materials
  - Returns courses, tutorials, and project recommendations

### User Management

- **GET** `/api/v1/user/history`

  - Get user's resume analysis history
  - Returns all versions with metadata

- **GET** `/api/v1/user/history/{version_id}`

  - Get specific resume version details

- **DELETE** `/api/v1/user/history/{version_id}`

  - Delete a resume version

- **GET** `/api/v1/user/profile`
  - Get current user profile information

## 🎨 UI Features

### Modern Design

- Clean, professional interface with gradient accents
- Responsive design for desktop, tablet, and mobile
- Smooth animations and transitions
- SVG icons throughout (no emojis for professional look)

### User Experience

- **Persistent Data**: Resume analysis persists across page reloads using localStorage
- **Active State Highlighting**: Selected sidebar panel is highlighted
- **Navigation**: Smooth scrolling and proper routing across all pages
- **Profile Dropdown**: Quick access to Dashboard, History, and Sign Out
- **Empty States**: Helpful messages when no data is available

## 🛠️ Tech Stack

### Frontend

- **React** 18 - UI framework
- **React Router** - Client-side routing
- **Context API** - State management
- **Supabase Client** - Authentication and database
- **CSS3** - Styling with gradients and animations

### Backend

- **FastAPI** - Modern Python web framework
- **Supabase** - Authentication and PostgreSQL database
- **Ollama** - Local LLM inference
- **PDFPlumber** - PDF parsing
- **Python-DOCX** - DOCX parsing

### Infrastructure

- **Supabase Auth** - JWT-based authentication
- **PostgreSQL** - Relational database with JSONB support
- **Row Level Security** - Database-level access control

## 📝 Development Notes

- Backend and frontend are fully decoupled for independent development
- All sensitive data is protected with Row Level Security (RLS)
- Resume data persists in localStorage for better UX
- Complete analysis stored in JSONB format for flexibility
- Version history automatically tracked for each resume upload
- `.gitignore` configured for Node, Python, VSCode, and Docker

## 🔒 Security

- JWT-based authentication via Supabase
- Row Level Security ensures users only access their own data
- Secure password hashing
- HTTPS recommended for production
- Environment variables for sensitive credentials

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Authors

- **avogadronuggies** - _Initial work_ - [GitHub](https://github.com/avogadronuggies)

## 🙏 Acknowledgments

- Ollama for local LLM inference
- Supabase for backend infrastructure
- React community for excellent tools and libraries
- All contributors and users of CareerLM

---

**Built with ❤️ to help job seekers succeed in their career journey**
