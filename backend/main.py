"""
FastAPI Backend for Spare Backend
Frontend (Windows) ↔ Backend (WSL) HTTP Connection

This backend:
1. Receives user_id from frontend login
2. Triggers all 9 agents for analysis
3. Agents push results to database via MCP
4. Returns status to frontend
5. Frontend fetches results directly from database
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add agents directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Import all agents
from pattern_agent import PatternRecognitionAgent
from budget_agent import BudgetAnalysisAgent
from context_agent import ContextIntelligenceAgent
from volatility_agent import VolatilityForecasterAgent
from knowledge_agent import KnowledgeIntegrationAgent
from tax_agent import TaxComplianceAgent
from recommendation_agent import RecommendationAgent
from risk_agent import RiskAssessmentAgent
from action_agent import ActionExecutionAgent
from savings_investment_agent import SavingsInvestmentAgent
from bill_payment_agent import BillPaymentAgent
from goals_agent import FinancialGoalsAgent

# Initialize FastAPI
app = FastAPI(
    title="Agente AI - Spare Backend",
    description="Background financial analysis service for gig workers",
    version="1.0.0"
)

# CORS configuration for Windows frontend ↔ WSL backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vue default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AnalysisRequest(BaseModel):
    user_id: str

class AnalysisResponse(BaseModel):
    status: str
    message: str
    user_id: str
    analysis_started: str
    estimated_completion_minutes: int

class StatusResponse(BaseModel):
    user_id: str
    status: str
    agents_completed: int
    total_agents: int
    last_updated: str

# In-memory status tracking (for MVP)
analysis_status: Dict[str, Dict[str, Any]] = {}


class AgentOrchestrator:
    """Orchestrates all 9 agents for a user"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.agents = {
            "pattern": PatternRecognitionAgent(mcp_servers),
            "budget": BudgetAnalysisAgent(mcp_servers),
            "context": ContextIntelligenceAgent(mcp_servers),
            "volatility": VolatilityForecasterAgent(mcp_servers),
            "knowledge": KnowledgeIntegrationAgent(mcp_servers),
            "tax": TaxComplianceAgent(mcp_servers),
            "recommendation": RecommendationAgent(mcp_servers),
            "risk": RiskAssessmentAgent(mcp_servers),
            "action": ActionExecutionAgent(mcp_servers),
            "savings": SavingsInvestmentAgent(mcp_servers),
            "bills": BillPaymentAgent(mcp_servers),
            "goals": FinancialGoalsAgent(mcp_servers)
        }

    async def run_all_agents(self, user_id: str) -> Dict[str, Any]:
        """Run all 9 agents in sequence"""

        print(f"\n{'='*60}")
        print(f"Starting analysis for user {user_id}")
        print(f"{'='*60}\n")

        results = {
            "user_id": user_id,
            "analysis_started": datetime.now().isoformat(),
            "agents": {}
        }

        # Update status
        analysis_status[user_id] = {
            "status": "in_progress",
            "agents_completed": 0,
            "total_agents": 12,
            "last_updated": datetime.now().isoformat()
        }

        agent_names = [
            ("pattern", "Pattern Recognition"),
            ("context", "Context Intelligence"),
            ("volatility", "Volatility Forecaster"),
            ("budget", "Budget Analysis"),
            ("knowledge", "Knowledge Integration"),
            ("tax", "Tax & Compliance"),
            ("risk", "Risk Assessment"),
            ("recommendation", "Recommendation Engine"),
            ("action", "Action Execution"),
            ("savings", "Savings & Investment"),
            ("bills", "Bill Payment"),
            ("goals", "Financial Goals")
        ]

        for idx, (agent_key, agent_name) in enumerate(agent_names, 1):
            print(f"\n[{idx}/12] Running {agent_name} Agent...")

            try:
                result = await self.agents[agent_key].analyze_user(user_id)
                results["agents"][agent_key] = result

                # Update status
                analysis_status[user_id]["agents_completed"] = idx
                analysis_status[user_id]["last_updated"] = datetime.now().isoformat()

                print(f"+ {agent_name} completed")

            except Exception as e:
                print(f"X {agent_name} failed: {str(e)}")
                results["agents"][agent_key] = {
                    "success": False,
                    "error": str(e)
                }

            # Brief pause between agents
            await asyncio.sleep(2)

        results["analysis_completed"] = datetime.now().isoformat()

        # Update final status
        analysis_status[user_id]["status"] = "completed"
        analysis_status[user_id]["last_updated"] = datetime.now().isoformat()

        print(f"\n{'='*60}")
        print(f"Analysis complete for user {user_id}")
        print(f"{'='*60}\n")

        return results


# Global orchestrator instance
orchestrator = AgentOrchestrator()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Agente AI - Spare Backend",
        "status": "running",
        "version": "1.0.0",
        "agents": 12
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def trigger_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Trigger complete financial analysis for a user

    Frontend calls this after login with user_id
    Analysis runs in background
    Frontend fetches results directly from database
    """

    user_id = request.user_id

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    # Check if analysis already in progress
    if user_id in analysis_status and analysis_status[user_id]["status"] == "in_progress":
        raise HTTPException(
            status_code=409,
            detail=f"Analysis already in progress for user {user_id}"
        )

    # Start analysis in background
    background_tasks.add_task(orchestrator.run_all_agents, user_id)

    return AnalysisResponse(
        status="started",
        message=f"Analysis started for user {user_id}. Results will be written to database.",
        user_id=user_id,
        analysis_started=datetime.now().isoformat(),
        estimated_completion_minutes=8
    )


@app.get("/api/status/{user_id}", response_model=StatusResponse)
async def get_analysis_status(user_id: str):
    """
    Get current status of analysis for a user

    Frontend can poll this to show progress
    """

    if user_id not in analysis_status:
        raise HTTPException(
            status_code=404,
            detail=f"No analysis found for user {user_id}"
        )

    status = analysis_status[user_id]

    return StatusResponse(
        user_id=user_id,
        status=status["status"],
        agents_completed=status["agents_completed"],
        total_agents=status["total_agents"],
        last_updated=status["last_updated"]
    )


@app.get("/api/agent-logs/{user_id}")
async def get_agent_logs(user_id: str):
    """
    Get detailed agent execution logs for a user
    
    Returns all agent responses and outputs for frontend display
    """
    try:
        # Fetch agent logs from database
        import requests
        
        url = f"https://ubjrclaiqqxngfcylbfs.supabase.co/rest/v1/agent_logs"
        headers = {
            "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVianJjbGFpcXF4bmdmY3lsYmZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5NzMzOTEsImV4cCI6MjA3OTU0OTM5MX0.Kkp7BV0ZSWq0ZR6YVOzwQwX08u3NOCxClvQWknWJlbA",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVianJjbGFpcXF4bmdmY3lsYmZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5NzMzOTEsImV4cCI6MjA3OTU0OTM5MX0.Kkp7BV0ZSWq0ZR6YVOzwQwX08u3NOCxClvQWknWJlbA"
        }
        
        params = {
            "user_id": f"eq.{user_id}",
            "order": "created_at.desc",
            "limit": "20"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        logs = response.json()
        
        return {
            "user_id": user_id,
            "logs": logs,
            "total_count": len(logs)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch agent logs: {str(e)}")


@app.post("/api/analyze-sync")
async def trigger_analysis_sync(request: AnalysisRequest):
    """
    Trigger analysis and wait for completion (synchronous)

    WARNING: This will take 5-10 minutes
    Use /api/analyze (async) for production
    """

    user_id = request.user_id

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    try:
        results = await orchestrator.run_all_agents(user_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Agente AI Spare Backend",
        "agents": {
            "pattern": "ready",
            "budget": "ready",
            "context": "ready",
            "volatility": "ready",
            "knowledge": "ready",
            "tax": "ready",
            "recommendation": "ready",
            "risk": "ready",
            "action": "ready",
            "savings": "ready",
            "bills": "ready",
            "goals": "ready"
        },
        "database": "mcp_connected",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*60)
    print("Starting Agente AI Spare Backend")
    print("="*60)
    print("\nFrontend (Windows) can connect to:")
    print("  > http://localhost:8000")
    print("  > http://127.0.0.1:8000")
    print("\nAPI Endpoints:")
    print("  POST /api/analyze          - Trigger analysis (async)")
    print("  POST /api/analyze-sync     - Trigger analysis (sync)")
    print("  GET  /api/status/{user_id} - Get analysis status")
    print("  GET  /api/health           - Health check")
    print("\nDocs available at:")
    print("  > http://localhost:8000/docs")
    print("="*60 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",  # Accept connections from Windows
        port=8000,
        log_level="info"
    )
