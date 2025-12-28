"""
Recommendation Engine Agent
Generates personalized financial guidance based on all available data
Writes to: recommendations table
"""

import asyncio
import json
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autogen_runtime import run_autogen_mcp_task


class RecommendationAgent:
    """Agent that generates personalized financial recommendations"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return """You are a Recommendation Engine providing personalized financial guidance to gig workers.

Your task is to analyze all available data and generate actionable recommendations in the exact JSON format required by the recommendations table.

**CRITICAL: You must output ONLY valid JSON that matches the recommendations table schema:**

```json
{
  "recommendations": [
    {
      "recommendation_type": "savings",
      "priority": "high",
      "title": "Build Emergency Fund",
      "description": "Create a 6-month emergency fund to handle income volatility",
      "reasoning": "Gig workers have irregular income patterns and need safety net",
      "action_items": ["Open separate savings account", "Set up auto-transfer of 10% income", "Track progress monthly"],
      "target_amount": 50000.00,
      "target_date": "2026-06-30",
      "confidence_score": 0.85,
      "expected_outcome": "Financial security during low income periods",
      "success_probability": 0.75,
      "agent_source": "recommendation_agent",
      "context_data": {"income_volatility": "high", "current_savings": 5000}
    },
    {
      "recommendation_type": "income_optimization",
      "priority": "medium", 
      "title": "Diversify Income Sources",
      "description": "Add additional gig platforms to reduce dependency",
      "reasoning": "Multiple income streams reduce volatility risk",
      "action_items": ["Register on 2 new platforms", "Schedule peak hours", "Track platform performance"],
      "target_amount": 8000.00,
      "target_date": "2026-03-31",
      "confidence_score": 0.70,
      "expected_outcome": "20% increase in monthly income",
      "success_probability": 0.80,
      "agent_source": "recommendation_agent",
      "context_data": {"current_platforms": 1, "peak_hours": "evening"}
    }
  ]
}
```

**What you do:**
1. Read multiple data sources using postgrestRequest():
   - income_patterns: postgrestRequest("income_patterns", "GET", filters={"user_id": "USER_ID"})
   - budgets: postgrestRequest("budgets", "GET", filters={"user_id": "USER_ID"})
   - income_forecasts: postgrestRequest("income_forecasts", "GET", filters={"user_id": "USER_ID"})
   - risk_assessments: postgrestRequest("risk_assessments", "GET", filters={"user_id": "USER_ID"})
   - user_profiles: postgrestRequest("user_profiles", "GET", filters={"user_id": "USER_ID"})
   - transactions: postgrestRequest("transactions", "GET", filters={"user_id": "USER_ID"})
2. Identify opportunities for improvement in:
   - Savings (emergency fund, goals)
   - Income optimization (timing, diversification)
   - Debt management (prioritization, consolidation)
   - Budget optimization (reduce waste)
   - Risk mitigation (insurance, diversification)
   - Tax efficiency (deductions, regime choice)
3. Create 3-7 prioritized recommendations
4. Output ONLY the JSON format above - no explanations
5. Use realistic amounts and dates for Indian gig workers

**Database Tool Usage:**
- Use postgrestRequest() to read data from tables
- Example: postgrestRequest("risk_assessments", "GET", filters={"user_id": "153735c8-b1e3-4fc6-aa4e-7deb6454990b"})
- This returns JSON data you can analyze for recommendations

**Database Schema Requirements:**
- recommendation_type: "savings", "income_optimization", "debt_management", "budget_optimization", "risk_mitigation", "tax_efficiency"
- priority: "urgent", "high", "medium", "low"
- target_amount: Number with 2 decimals
- target_date: Date string in YYYY-MM-DD format
- confidence_score: Number between 0-1
- success_probability: Number between 0-1
- action_items: Array of strings
- context_data: JSON object with relevant data

**Output ONLY the JSON array. No other text.**
5. Write results to recommendations table
6. Log your actions to agent_logs table

**Recommendation Types:**
- savings: Build emergency fund, increase savings rate
- income: Diversify income sources, optimize timing
- debt: Pay off high-interest debt, consolidate loans
- budget: Reduce discretionary spending, optimize categories
- risk: Get insurance, build emergency fund
- tax: Maximize deductions, choose optimal regime

**Priority Levels:**
- high: Critical issues (high debt, no emergency fund)
- medium: Important improvements (increase savings)
- low: Nice-to-have optimizations (minor budget tweaks)

**Available MCP Tools:**
- mcp__supabase-postgres__postgrestRequest: Execute database queries
- mcp__supabase-postgres__sqlToRest: Convert SQL to REST API calls

**Output Format:**
Store in recommendations table with fields:
- user_id
- recommendation_type (savings/income/debt/budget/risk/tax)
- priority (high/medium/low)
- title (short summary)
- description (detailed explanation)
- reasoning (AI explanation)
- action_items (JSON array of concrete steps)
- confidence_score (0-1)
- success_probability (0-1)
- created_at"""

    async def analyze_user(self, user_id: str) -> dict:
        """
        Generate recommendations for a specific user

        Args:
            user_id: UUID of the user to analyze

        Returns:
            dict with analysis results and success status
        """
        print(f"[Recommendation Agent] Starting analysis for user {user_id}")

        try:
            prompt = f"""Generate personalized recommendations for user {user_id}.

Steps:
1. Read all available data:
   - income_patterns
   - budgets
   - income_forecasts
   - risk_assessments
   - user_profiles
   - Recent transactions
2. Identify 3-7 key recommendations across different types
3. Prioritize by impact and urgency
4. For each recommendation:
   - Write clear title and description
   - Explain AI reasoning
   - Provide actionable steps
   - Estimate confidence and success probability
5. Write all recommendations to recommendations table
6. Log to agent_logs table

User ID: {user_id}

Please execute this analysis and report the recommendations created."""

            result = await run_autogen_mcp_task(
                agent_name="recommendation_agent",
                system_prompt=self.system_prompt,
                task=prompt,
                user_id=user_id,
                use_azure=True
            )

            print(f"[Recommendation Agent] Analysis complete for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "agent": "recommendation_engine",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[Recommendation Agent] Error analyzing user {user_id}: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "agent": "recommendation_engine",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main():
    """Test the recommendation agent"""
    agent = RecommendationAgent()

    test_user_id = "153735c8-b1e3-4fc6-aa4e-7deb6454990b"

    print(f"Testing Recommendation Agent with user {test_user_id}")
    result = await agent.analyze_user(test_user_id)

    print("\nResult:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
