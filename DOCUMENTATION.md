# Kamai - Financial Companion for Gig Workers

## Complete Technical Documentation

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Architecture](#3-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Features](#5-features)
6. [AI Agents](#6-ai-agents)
7. [Database Schema](#7-database-schema)
8. [API Endpoints](#8-api-endpoints)
9. [Frontend Pages](#9-frontend-pages)
10. [Setup & Installation](#10-setup--installation)
11. [Data Flow](#11-data-flow)
12. [Security](#12-security)

---

## 1. Project Overview

**Kamai** is an AI-powered financial companion designed specifically for gig workers in India. The platform helps delivery partners, drivers, and freelancers manage their irregular income through intelligent budgeting, savings planning, and automated financial recommendations.

### Key Highlights
- Multi-agent AI system with 12 specialized financial agents
- Real-time financial tracking and analysis
- Personalized recommendations based on income patterns
- Support for Indian financial ecosystem (UPI, tax slabs, government schemes)

---

## 2. Problem Statement

**Hackathon Category:** S2 — Finance

### The Challenge
Gig workers in India face unique financial challenges:
- Irregular and unpredictable income
- No employer-provided benefits or savings plans
- Difficulty in budgeting with variable earnings
- Limited access to financial planning tools
- Complex tax compliance for freelancers

### Our Solution
An AI-powered platform that:
1. Tracks income and expenses automatically
2. Creates adaptive budgets based on earning patterns
3. Plans savings and investments suitable for variable income
4. Automates bill payment decisions
5. Sets financial goals with clear explanations and milestones

---

## 3. Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│                     Port: 5173 (Vite Dev)                       │
├─────────────────────────────────────────────────────────────────┤
│  Pages: Dashboard, Transactions, Budget, Goals, Savings, etc.  │
│  Services: database.ts (Supabase SDK)                           │
│  State: React Hooks + LocalStorage                              │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP (REST API)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│                        Port: 8000                               │
├─────────────────────────────────────────────────────────────────┤
│  Endpoints: /api/analyze, /api/status, /api/health             │
│  Orchestrator: Manages 12 AI Agents                             │
│  Runtime: AutoGen + Azure OpenAI                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │ REST API
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (Supabase)                          │
│                PostgreSQL + Real-time Sync                      │
├─────────────────────────────────────────────────────────────────┤
│  Tables: users, transactions, budgets, recommendations,        │
│          savings_goals, bills, financial_goals, etc.            │
│  Security: Row Level Security (RLS) Policies                    │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATOR                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Pattern    │  │   Context    │  │  Volatility  │          │
│  │    Agent     │  │    Agent     │  │    Agent     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Budget     │  │  Knowledge   │  │     Tax      │          │
│  │    Agent     │  │    Agent     │  │    Agent     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Risk      │  │Recommendation│  │   Action     │          │
│  │    Agent     │  │    Agent     │  │    Agent     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Savings    │  │    Bills     │  │    Goals     │          │
│  │    Agent     │  │    Agent     │  │    Agent     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Technology Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI Framework |
| TypeScript | Type Safety |
| Vite | Build Tool & Dev Server |
| Tailwind CSS | Styling |
| shadcn/ui | Component Library |
| Framer Motion | Animations |
| React Router | Navigation |
| Supabase JS | Database Client |
| Recharts | Data Visualization |
| date-fns | Date Handling |

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Runtime |
| FastAPI | Web Framework |
| Uvicorn | ASGI Server |
| AutoGen | Multi-Agent Framework |
| Azure OpenAI | LLM Provider |
| Pydantic | Data Validation |
| python-dotenv | Environment Config |

### Database
| Technology | Purpose |
|------------|---------|
| Supabase | Backend-as-a-Service |
| PostgreSQL | Relational Database |
| Row Level Security | Data Protection |

### AI/ML
| Technology | Purpose |
|------------|---------|
| Azure OpenAI GPT-4 | Language Model |
| AutoGen Framework | Agent Orchestration |
| Custom Prompts | Financial Analysis |

---

## 5. Features

### 5.1 Income & Expense Tracking
- Manual transaction entry with categories
- Support for multiple income sources (Swiggy, Zomato, Uber, etc.)
- Expense categorization (rent, fuel, food, utilities)
- Daily, weekly, monthly summaries
- Search and filter transactions

### 5.2 Budget Optimization System
- Three budget modes: Feast, Famine, Normal
- Adaptive budgets based on income volatility
- Category-wise spending limits
- Real-time budget tracking
- Overspending alerts

### 5.3 Savings & Investment Planning
- Emergency fund calculator (6 months expenses)
- Investment recommendations:
  - Post Office RD (7.5% p.a.)
  - PPF (7.1% p.a.)
  - SIP in Index Funds (10-12% p.a.)
  - NPS for retirement
- Risk-based suggestions (low/moderate/high)
- Monthly contribution targets

### 5.4 Automated Bill Payment Decisions
- Bill detection from transaction history
- Priority classification:
  - Critical: EMIs, Rent
  - High: Utilities
  - Medium: Subscriptions
  - Low: Optional services
- Payment schedule aligned with income days
- Auto-pay recommendations
- Late fee risk calculation

### 5.5 Financial Goal-Based Planning
- Goal types:
  - Emergency Fund
  - Asset Purchase (bike, phone)
  - Education
  - Healthcare
  - Retirement
  - Business expansion
- Detailed explanations for each goal:
  - Why it matters
  - How target was calculated
  - Steps to achieve
  - Impact when achieved
- Milestones with rewards
- Progress tracking
- Obstacle identification and contingency plans

---

## 6. AI Agents

### Agent Details

| # | Agent Name | Purpose | Output Table |
|---|------------|---------|--------------|
| 1 | Pattern Recognition | Identifies income patterns and trends | income_patterns |
| 2 | Context Intelligence | Understands user context and life situation | user_profiles |
| 3 | Volatility Forecaster | Predicts income fluctuations | income_forecasts |
| 4 | Budget Analysis | Creates adaptive budgets | budgets |
| 5 | Knowledge Integration | Integrates financial knowledge | recommendations |
| 6 | Tax & Compliance | Handles tax calculations and filing | tax_records |
| 7 | Risk Assessment | Evaluates financial risks | risk_assessments |
| 8 | Recommendation Engine | Generates personalized advice | recommendations |
| 9 | Action Execution | Creates actionable financial tasks | executed_actions |
| 10 | Savings & Investment | Plans savings and investments | savings_goals, investment_recommendations |
| 11 | Bill Payment | Automates bill decisions | bills |
| 12 | Financial Goals | Creates goal-based plans | financial_goals |

### Agent Workflow
1. User triggers analysis via `/api/analyze`
2. Orchestrator runs agents sequentially
3. Each agent:
   - Reads relevant data from database
   - Analyzes using Azure OpenAI
   - Outputs structured JSON
   - Writes results to database
4. Frontend fetches updated data in real-time

---

## 7. Database Schema

### Core Tables

#### users
```sql
- user_id: UUID (Primary Key)
- phone_number: VARCHAR(10)
- email: VARCHAR
- full_name: VARCHAR
- occupation: VARCHAR
- city, state, pin_code: VARCHAR
- preferred_language: VARCHAR
- is_active: BOOLEAN
- kyc_verified: BOOLEAN
- created_at: TIMESTAMP
```

#### transactions
```sql
- transaction_id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- transaction_date: DATE
- amount: DECIMAL
- transaction_type: ENUM ('income', 'expense')
- category: VARCHAR
- description: TEXT
- payment_method: VARCHAR
- is_recurring: BOOLEAN
- created_at: TIMESTAMP
```

#### budgets
```sql
- budget_id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- budget_type: ENUM ('feast', 'famine', 'normal')
- valid_from, valid_until: DATE
- total_income_expected: DECIMAL
- fixed_costs: JSONB
- variable_costs: JSONB
- savings_target: DECIMAL
- is_active: BOOLEAN
```

#### savings_goals
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- goal_type: VARCHAR
- goal_name: VARCHAR
- target_amount: DECIMAL
- current_amount: DECIMAL
- monthly_contribution: DECIMAL
- priority: ENUM ('high', 'medium', 'low')
- status: ENUM ('not_started', 'in_progress', 'completed')
- reasoning: TEXT
```

#### investment_recommendations
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- investment_type: VARCHAR
- provider: VARCHAR
- recommended_amount: DECIMAL
- frequency: VARCHAR
- expected_return: DECIMAL
- risk_level: ENUM ('low', 'moderate', 'high')
- reasoning: TEXT
```

#### bills
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- bill_name: VARCHAR
- bill_type: VARCHAR
- amount: DECIMAL
- due_date: DATE
- frequency: VARCHAR
- priority: ENUM ('critical', 'high', 'medium', 'low')
- auto_pay_recommended: BOOLEAN
- status: ENUM ('pending', 'paid', 'overdue', 'scheduled')
```

#### financial_goals
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- goal_name: VARCHAR
- goal_type: VARCHAR
- description: TEXT
- target_amount: DECIMAL
- current_amount: DECIMAL
- target_date: DATE
- priority: INTEGER
- status: ENUM ('not_started', 'in_progress', 'completed', 'paused')
- monthly_target: DECIMAL
- progress_percentage: DECIMAL
- explanation: JSONB
- milestones: JSONB
- action_steps: JSONB
```

---

## 8. API Endpoints

### Backend API (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check, returns service info |
| GET | `/api/health` | Detailed health check with agent status |
| POST | `/api/analyze` | Trigger async analysis for user |
| POST | `/api/analyze-sync` | Trigger sync analysis (blocking) |
| GET | `/api/status/{user_id}` | Get analysis progress |
| GET | `/api/agent-logs/{user_id}` | Get agent execution logs |

### Request/Response Examples

#### POST /api/analyze
```json
// Request
{
  "user_id": "153735c8-b1e3-4fc6-aa4e-7deb6454990b"
}

// Response
{
  "status": "started",
  "message": "Analysis started for user...",
  "user_id": "153735c8-b1e3-4fc6-aa4e-7deb6454990b",
  "analysis_started": "2025-01-15T10:30:00",
  "estimated_completion_minutes": 8
}
```

#### GET /api/status/{user_id}
```json
{
  "user_id": "153735c8-b1e3-4fc6-aa4e-7deb6454990b",
  "status": "in_progress",
  "agents_completed": 7,
  "total_agents": 12,
  "last_updated": "2025-01-15T10:35:00"
}
```

---

## 9. Frontend Pages

| Page | Route | Description |
|------|-------|-------------|
| Landing | `/` | Marketing page with features |
| Login | `/login` | Phone + password login |
| Signup | `/signup` | New user registration |
| Dashboard | `/dashboard` | Main overview with stats |
| Transactions | `/transactions` | Income/expense management |
| Budget | `/budget` | Budget creation and tracking |
| Goals | `/goals` | Financial goal management |
| Savings | `/savings` | Savings and investments |
| Actions | `/actions` | Automated financial actions |
| Tips | `/tips` | AI recommendations |
| Tax | `/tax` | Tax records and compliance |
| Risk | `/risk` | Risk assessment dashboard |
| Profile | `/profile` | User profile management |
| Benefits | `/benefits` | Government schemes |

---

## 10. Setup & Installation

### Prerequisites
- Node.js 18+
- Python 3.11+
- Supabase account
- Azure OpenAI access

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env file with your credentials:
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_ENDPOINT

# Start server
python main.py
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
# Edit .env file:
# - VITE_SUPABASE_URL
# - VITE_SUPABASE_ANON_KEY
# - VITE_API_BASE_URL

# Start dev server
npm run dev
```

### Database Setup

1. Create Supabase project
2. Run SQL migrations for all tables
3. Enable Row Level Security
4. Configure RLS policies

---

## 11. Data Flow

### User Registration Flow
```
User enters details → Frontend validates →
Supabase creates user → user_id stored in localStorage →
Redirect to dashboard
```

### Analysis Flow
```
User logs in → Frontend calls POST /api/analyze →
Backend starts 12 agents sequentially →
Each agent reads data, analyzes with GPT-4, writes results →
Frontend fetches updated data from Supabase →
Dashboard displays insights
```

### Real-time Updates
```
Agent writes to Supabase →
Supabase real-time broadcasts change →
Frontend receives update →
UI re-renders with new data
```

---

## 12. Security

### Authentication
- Phone number + password based auth
- Session tokens stored in localStorage
- Token validation on each request

### Database Security
- Row Level Security (RLS) enabled
- Users can only access their own data
- Anon key has limited permissions

### API Security
- CORS configured for allowed origins
- Input validation with Pydantic
- Error handling without sensitive info exposure

### Sensitive Data
- API keys stored in environment variables
- .env files excluded from version control
- Supabase service key never exposed to frontend

---

## Project Structure

```
Kamai-main/
├── backend/
│   ├── agents/
│   │   ├── pattern_agent.py
│   │   ├── budget_agent.py
│   │   ├── context_agent.py
│   │   ├── volatility_agent.py
│   │   ├── knowledge_agent.py
│   │   ├── tax_agent.py
│   │   ├── recommendation_agent.py
│   │   ├── risk_agent.py
│   │   ├── action_agent.py
│   │   ├── savings_investment_agent.py
│   │   ├── bill_payment_agent.py
│   │   ├── goals_agent.py
│   │   └── financial_agent.py
│   ├── main.py
│   ├── autogen_runtime.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── database.ts
│   │   ├── lib/
│   │   │   └── supabase.ts
│   │   └── App.tsx
│   ├── package.json
│   └── .env
│
├── supabase_new_tables.sql
├── DOCUMENTATION.md
└── PROGRESS_REPORT.md
```

---

## Conclusion

Kamai represents a comprehensive solution for the financial challenges faced by India's growing gig economy workforce. By leveraging multi-agent AI architecture and real-time data processing, the platform provides personalized, actionable financial guidance that adapts to the unique income patterns of gig workers.

---

*Documentation Version: 1.0*
*Last Updated: December 2025*
*Hackathon: S2 — Finance*
