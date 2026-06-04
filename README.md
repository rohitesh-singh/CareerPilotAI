# 🚀 CareerPilotAI

### AI-Powered Career Operating System

CareerPilotAI is an AI-powered platform that helps professionals optimize resumes, analyze job fit, generate tailored resumes, track applications, and monitor job search performance through a unified dashboard.

Built using Streamlit, Groq, Supabase, and Python, the platform streamlines the job application process and provides actionable insights to improve interview outcomes.

---

## 🎯 Key Features

### 📄 Resume Optimizer
- Upload resumes in PDF format
- Analyze alignment with job descriptions
- ATS keyword gap analysis
- Match score calculation
- Strengths and missing skills identification
- Interview probability assessment
- Resume recommendations

### 📝 Resume Generator
- Generate tailored resumes for specific roles
- Human-like professional writing
- ATS-friendly formatting
- Download optimized resumes as DOCX
- Save generated resumes for future reference

### 📚 Resume Library
- Store generated resumes in Supabase
- Access historical resume versions
- Organize resumes by company and role
- Resume history management

### 💼 Application Tracker
- Save and track job applications
- Store company, role, match score, and application status
- Centralized application management

### 📊 Analytics Dashboard
- Application tracking metrics
- Average match score monitoring
- Application funnel visualization
- Status distribution analytics
- Performance insights

### 🤖 AI-Powered Analysis
- Groq LLM integration
- Resume-to-job matching
- ATS optimization recommendations
- Personalized resume generation

---

## 🏗️ Architecture

```text
┌─────────────────────┐
│      Streamlit      │
│         UI          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Service Layer     │
├─────────────────────┤
│ PDF Service         │
│ Resume Optimizer    │
│ Resume Generator    │
│ Groq Service        │
│ Supabase Service    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Supabase       │
├─────────────────────┤
│ Applications        │
│ Generated Resumes   │
│ Analytics Data      │
└─────────────────────┘
```

---

## ⚙️ Technology Stack

### Frontend
- Streamlit

### Backend
- Python

### AI
- Groq LLM

### Database
- Supabase

### Data Visualization
- Plotly

### Document Processing
- PyPDF
- python-docx

---

## 📂 Project Structure

```text
CareerPilotAI/
│
├── pages/
│   ├── Dashboard
│   ├── Resume Optimizer
│   ├── Resume Generator
│   ├── Applications
│   └── Analytics
│
├── services/
│   ├── groq_service.py
│   ├── pdf_services.py
│   ├── resume_optimizer_service.py
│   └── supabase_service.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/rohitesh-singh/CareerPilotAI.git
cd CareerPilotAI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

### Run Application

```bash
streamlit run app.py
```

---

## 📈 Future Enhancements

- Google Cloud Storage integration
- Job URL auto extraction
- Resume version comparison
- Application reminders
- AI interview preparation assistant
- Recruiter insights dashboard
- Automated job discovery
- Multi-user authentication

---

## 🎓 Learning Outcomes

This project demonstrates:

- AI-powered workflow automation
- LLM integration using Groq
- Full-stack application development
- Cloud database integration with Supabase
- Resume optimization and ATS analysis
- Analytics dashboard design
- Product thinking and workflow automation

---

## 👨‍💻 Built By

**Rohitesh Singh**

CareerPilotAI was designed and developed as an AI-powered career operating system focused on helping professionals optimize resumes, improve job application outcomes and manage their job search more effectively.