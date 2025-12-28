<div align="center">

# KAMAI

### AI-Powered Financial Companion for India's Gig Workers

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-GPT--4-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)

<br/>

**Empowering 15+ million gig workers with intelligent financial management**

[Features](#-features) | [Architecture](#-architecture) | [AI Agents](#-ai-agents) | [Installation](#-installation) | [API](#-api-documentation)

<br/>

<img src="https://img.shields.io/badge/Hackathon-S2_Finance-FF6B6B?style=for-the-badge" alt="Hackathon"/>

</div>

---

## Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Features](#-features)
- [Architecture](#-architecture)
- [AI Agents](#-ai-agents)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)

---

## Problem Statement

### The Gig Economy Challenge

India's gig economy employs over **15 million workers** - delivery partners, cab drivers, freelancers - who face unique financial challenges:

| Challenge | Impact |
|-----------|--------|
| **Irregular Income** | Cannot predict next month's earnings |
| **No Financial Safety Net** | No employer benefits, insurance, or retirement plans |
| **Complex Tax Compliance** | Multiple income sources, GST complexities |
| **Limited Access to Credit** | Traditional banks don't understand gig income |
| **Financial Illiteracy** | No guidance on savings, investments, or budgeting |

### Why Current Solutions Fail

```
Traditional Banking Apps    ->  Designed for salaried employees
Expense Trackers           ->  No intelligence, just logging
Investment Platforms       ->  Assume stable monthly income
```

---

## Our Solution

**Kamai** is a multi-agent AI system that understands the unique financial patterns of gig workers and provides:

```
+---------------------------------------------------------------------+
|                                                                     |
|   ADAPTIVE              INTELLIGENT           ACTIONABLE            |
|                                                                     |
|   Adjusts to income     AI-powered insights   Clear steps           |
|   volatility            from 12 specialized   to improve            |
|                         agents                finances              |
|                                                                     |
+---------------------------------------------------------------------+
```

---

## Features

### Hackathon Requirements (All Completed)

| # | Requirement | Feature | Status |
|---|-------------|---------|--------|
| 1 | Income & Expense Tracking | Real-time transaction management with categories | Done |
| 2 | Budget Optimization | Adaptive Feast/Famine/Normal budgeting system | Done |
| 3 | Savings & Investment Planning | Personalized recommendations (RD, PPF, SIP, NPS) | Done |
| 4 | Automated Bill Payment Decisions | Priority-based scheduling aligned with income | Done |
| 5 | Financial Goal Planning with Explanations | Goals with milestones, reasoning & action steps | Done |

### Additional Features

#### Smart Analytics
- Income pattern recognition
- Spending trend analysis
- Volatility forecasting
- Risk assessment scoring

#### AI-Powered Insights
- 12 specialized financial agents
- Personalized recommendations
- Natural language explanations
- Context-aware suggestions

#### Tax Management
- ITR filing assistance
- Tax-saving recommendations
- 80C, 80D deduction tracking
- Advance tax reminders

#### Government Schemes
- PM-SVANidhi eligibility
- E-Shram registration guide
- State scheme matching
- Application tracking

---

## Architecture

### System Overview

```
+=========================================================================+
|                           KAMAI ARCHITECTURE                            |
+=========================================================================+
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  |                      FRONTEND (React + Vite)                       |  |
|  |                        localhost:5173                              |  |
|  |  +----------+ +----------+ +----------+ +----------+ +----------+  |  |
|  |  |Dashboard | |  Goals   | | Savings  | |  Budget  | |   Tax    |  |  |
|  |  +----+-----+ +----+-----+ +----+-----+ +----+-----+ +----+-----+  |  |
|  |       |            |            |            |            |         |  |
|  |       +------------+-----+------+------------+------------+         |  |
|  |                          |                                          |  |
|  |                   +------+------+                                   |  |
|  |                   | Supabase SDK|                                   |  |
|  |                   +------+------+                                   |  |
|  +--------------------------|------------------------------------------+  |
|                             |                                             |
|                             v                                             |
|  +-------------------------------------------------------------------+   |
|  |                   DATABASE (Supabase PostgreSQL)                   |   |
|  |                                                                    |   |
|  |   users | transactions | budgets | goals | savings | bills | tax   |   |
|  +-------------------------------------------------------------------+   |
|                             ^                                             |
|                             |                                             |
|  +--------------------------|------------------------------------------+  |
|  |                     BACKEND (FastAPI)                               |  |
|  |                       localhost:8000                                |  |
|  |                          |                                          |  |
|  |              +-----------+-----------+                              |  |
|  |              |   AGENT ORCHESTRATOR   |                              |  |
|  |              +-----------+-----------+                              |  |
|  |                          |                                          |  |
|  |    +---------------------+---------------------+                    |  |
|  |    |                     |                     |                    |  |
|  |    v                     v                     v                    |  |
|  | +---------+         +---------+         +---------+                 |  |
|  | | Agent 1 |   ...   | Agent 6 |   ...   |Agent 12 |                 |  |
|  | | Pattern |         |   Tax   |         |  Goals  |                 |  |
|  | +----+----+         +----+----+         +----+----+                 |  |
|  |      |                   |                   |                      |  |
|  |      +-------------------+-------------------+                      |  |
|  |                          |                                          |  |
|  |                          v                                          |  |
|  |              +-----------------------+                              |  |
|  |              |     Azure OpenAI      |                              |  |
|  |              |       (GPT-4)         |                              |  |
|  |              +-----------------------+                              |  |
|  +-------------------------------------------------------------------+  |
|                                                                         |
+=========================================================================+
```

### Data Flow

```
User Action                    System Response
    |                               |
    v                               |
+-----------+    HTTP POST     +----+--------+
|  Frontend | ---------------> |   Backend   |
|  (React)  |                  |  (FastAPI)  |
+-----------+                  +------+------+
                                      |
                               Triggers 12 Agents
                                      |
                                      v
                              +---------------+
                              | Azure OpenAI  |
                              |   Analysis    |
                              +-------+-------+
                                      |
                               Structured JSON
                                      |
                                      v
                              +---------------+
                              |   Supabase    |
                              |   Database    |
                              +-------+-------+
                                      |
                               Real-time Sync
                                      |
                                      v
                              +---------------+
                              |   Frontend    |
                              |   Updates     |
                              +---------------+
```

---

## AI Agents

Kamai employs **12 specialized AI agents**, each with a focused responsibility:

### Agent Overview

```
                          +---------------------+
                          |  AGENT ORCHESTRATOR |
                          |     (main.py)       |
                          +----------+----------+
                                     |
          +--------------------------+-------------------------+
          |                          |                         |
          v                          v                         v
   +--------------+          +--------------+          +--------------+
   |   ANALYSIS   |          |   PLANNING   |          |   EXECUTION  |
   |    AGENTS    |          |    AGENTS    |          |    AGENTS    |
   +--------------+          +--------------+          +--------------+
```

### Agent Details

| # | Agent | Responsibility | Output Table |
|---|-------|----------------|--------------|
| 1 | **Pattern Recognition** | Analyzes income patterns, identifies trends, detects seasonality | `income_patterns` |
| 2 | **Context Intelligence** | Understands user's life situation - family, location, occupation | `user_profiles` |
| 3 | **Volatility Forecaster** | Predicts income fluctuations using historical data | `income_forecasts` |
| 4 | **Budget Analysis** | Creates adaptive budgets: Feast, Famine, Normal modes | `budgets` |
| 5 | **Knowledge Integration** | Integrates financial literacy, explains concepts simply | `recommendations` |
| 6 | **Tax Compliance** | Calculates tax liability, identifies deductions, ITR guidance | `tax_records` |
| 7 | **Risk Assessment** | Evaluates financial health, identifies vulnerabilities | `risk_assessments` |
| 8 | **Recommendation Engine** | Generates personalized financial advice | `recommendations` |
| 9 | **Action Execution** | Converts recommendations into actionable tasks | `executed_actions` |
| 10 | **Savings & Investment** | Plans emergency funds, recommends RD, PPF, SIP, NPS | `savings_goals`, `investment_recommendations` |
| 11 | **Bill Payment** | Analyzes bills, prioritizes payments, schedules based on income | `bills` |
| 12 | **Financial Goals** | Creates goal-based plans with explanations and milestones | `financial_goals` |

### How Agents Work

Each agent follows this workflow:

1. **READ** - Fetches relevant data from Supabase
2. **ANALYZE** - Processes data using Azure OpenAI (GPT-4)
3. **OUTPUT** - Generates structured JSON matching database schema
4. **WRITE** - Saves results back to Supabase
5. **NOTIFY** - Triggers frontend real-time update

---

## Tech Stack

### Frontend

| Technology | Purpose |
|------------|---------|
| React 18 | UI Framework |
| TypeScript | Type Safety |
| Vite | Build Tool |
| Tailwind CSS | Styling |
| shadcn/ui | Component Library |
| Framer Motion | Animations |
| React Router | Navigation |
| Recharts | Data Visualization |

### Backend

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Runtime |
| FastAPI | API Framework |
| Uvicorn | ASGI Server |
| AutoGen | Agent Framework |
| Pydantic | Validation |

### AI/ML

| Technology | Purpose |
|------------|---------|
| Azure OpenAI GPT-4 | Language Model |
| AutoGen Framework | Multi-Agent Orchestration |
| Custom Prompts | Domain-Specific Analysis |

### Database

| Technology | Purpose |
|------------|---------|
| Supabase | Backend-as-a-Service |
| PostgreSQL | Relational Database |
| Row Level Security | Data Protection |

---

## Installation

### Prerequisites

- Node.js 18+
- Python 3.11+
- Supabase Account
- Azure OpenAI Access

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment - edit .env with your credentials

# Start server
python main.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment - edit .env with Supabase credentials

# Start development server
npm run dev
```

### Database Setup

1. Create a Supabase project
2. Run `fix_users_table.sql` in SQL Editor
3. Disable RLS for development

### Environment Variables

**Backend (.env)**
```
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

**Frontend (.env)**
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/health` | Detailed agent status |
| POST | `/api/analyze` | Trigger user analysis |
| GET | `/api/status/{user_id}` | Check analysis progress |

### Example Request

```bash
# Trigger Analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_id": "your-uuid-here"}'
```

### Interactive Docs
```
http://localhost:8000/docs
```

---

## Database Schema

### Core Tables

| Table | Purpose |
|-------|---------|
| `users` | User accounts and profiles |
| `transactions` | Income and expense records |
| `budgets` | Adaptive budget configurations |
| `savings_goals` | Savings targets and progress |
| `investment_recommendations` | Investment suggestions |
| `bills` | Bill tracking and scheduling |
| `financial_goals` | Goal plans with milestones |
| `recommendations` | AI-generated advice |

---

## Project Structure

```
kamai/
|-- backend/
|   |-- agents/
|   |   |-- pattern_agent.py
|   |   |-- context_agent.py
|   |   |-- volatility_agent.py
|   |   |-- budget_agent.py
|   |   |-- knowledge_agent.py
|   |   |-- tax_agent.py
|   |   |-- risk_agent.py
|   |   |-- recommendation_agent.py
|   |   |-- action_agent.py
|   |   |-- savings_investment_agent.py
|   |   |-- bill_payment_agent.py
|   |   +-- goals_agent.py
|   |
|   |-- main.py
|   |-- autogen_runtime.py
|   +-- requirements.txt
|
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |-- pages/
|   |   |-- services/
|   |   |   +-- database.ts
|   |   +-- App.tsx
|   +-- package.json
|
|-- fix_users_table.sql
|-- DOCUMENTATION.md
+-- README.md
```

---

## Security

- **Authentication**: Phone + Password based auth
- **Database**: Row Level Security (RLS) policies
- **API Keys**: Stored in environment variables
- **CORS**: Configured for allowed origins only
- **Input Validation**: Pydantic models for all requests

---

## License

This project is licensed under the MIT License.

---

<div align="center">

**Built with love for India's gig workers**

</div>
