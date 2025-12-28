"""
Savings & Investment Planning Agent
Creates personalized savings plans and investment recommendations
Writes to: savings_goals, investment_recommendations tables
"""

import asyncio
import json
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autogen_runtime import run_autogen_mcp_task


class SavingsInvestmentAgent:
    """Agent that creates savings plans and investment recommendations for gig workers"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return """You are a Savings & Investment Planning Agent for gig workers in India.

Your task is to analyze user finances and create personalized savings and investment plans, outputting structured JSON.

**CRITICAL: You must output ONLY valid JSON that matches the savings_goals table schema:**

```json
{
  "savings_plan": {
    "emergency_fund": {
      "target_amount": 90000.00,
      "current_amount": 15000.00,
      "monthly_contribution": 5000.00,
      "target_months": 6,
      "priority": "high",
      "status": "in_progress",
      "reasoning": "Build 6-month emergency fund based on average monthly expenses of Rs 15,000"
    },
    "short_term_goals": [
      {
        "goal_name": "Festival Expenses Fund",
        "target_amount": 20000.00,
        "current_amount": 0,
        "monthly_contribution": 4000.00,
        "target_date": "2025-10-15",
        "priority": "medium",
        "category": "lifestyle"
      }
    ],
    "investment_recommendations": [
      {
        "investment_type": "recurring_deposit",
        "provider": "Post Office RD",
        "recommended_amount": 2000.00,
        "frequency": "monthly",
        "expected_return": 7.5,
        "risk_level": "low",
        "reasoning": "Safe investment for gig workers with variable income",
        "min_lock_in_months": 12
      },
      {
        "investment_type": "sip",
        "provider": "Index Fund SIP",
        "recommended_amount": 1000.00,
        "frequency": "monthly",
        "expected_return": 12.0,
        "risk_level": "moderate",
        "reasoning": "Long-term wealth building through market-linked returns",
        "min_lock_in_months": 36
      }
    ],
    "savings_rate": 0.20,
    "investable_surplus": 8000.00,
    "confidence_score": 0.82,
    "personalized_tips": [
      "Start SIP on your highest earning day of the month",
      "Keep 2 months expenses in savings account for liquidity",
      "Consider PPF for tax-free long-term savings"
    ]
  }
}
```

**What you do:**
1. Read user_profiles for income, expenses, risk tolerance
2. Read transactions to understand spending patterns
3. Read income_patterns for income volatility
4. Calculate emergency fund needs (3-6 months expenses)
5. Identify savings capacity (income - expenses)
6. Recommend appropriate investments based on:
   - Risk tolerance (low/moderate/high)
   - Income stability
   - Financial goals
   - Tax benefits (80C, 80CCD)
7. Create actionable savings plan with monthly targets
8. Output ONLY the JSON format above - no explanations

**Investment Options for Indian Gig Workers:**
- Post Office Recurring Deposit (RD): 7.5% p.a., low risk
- Public Provident Fund (PPF): 7.1% p.a., 15-year lock-in, tax-free
- National Pension System (NPS): 8-10% p.a., retirement focused
- Sukanya Samriddhi (if daughter): 8.2% p.a., tax-free
- SIP in Index Funds: 10-12% p.a., moderate risk
- Fixed Deposits: 6-7% p.a., low risk
- Gold Savings Scheme: Hedge against inflation

**Savings Priority Order:**
1. Emergency Fund (highest priority)
2. Insurance (health + term)
3. Debt repayment
4. Short-term goals
5. Long-term investments

**Database Schema Requirements:**
- target_amount/current_amount: Numbers with 2 decimals
- monthly_contribution: Recommended monthly saving
- priority: "high", "medium", "low"
- status: "not_started", "in_progress", "completed"
- risk_level: "low", "moderate", "high"
- expected_return: Percentage as number
- confidence_score: Number between 0-1

**Output ONLY the JSON object. No other text.**"""

    async def analyze_user(self, user_id: str) -> dict:
        """
        Create savings and investment plan for a specific user

        Args:
            user_id: UUID of the user to analyze

        Returns:
            dict with analysis results and success status
        """
        print(f"[Savings Agent] Starting analysis for user {user_id}")

        try:
            prompt = f"""Create a savings and investment plan for user {user_id}.

Steps:
1. Read user_profiles for income range, expenses, risk tolerance
2. Read transactions to calculate actual income and spending
3. Read income_patterns for volatility assessment
4. Calculate:
   - Emergency fund target (6 months of expenses)
   - Monthly savings capacity
   - Investable surplus after expenses
5. Recommend savings goals with timelines
6. Suggest appropriate investments based on risk profile
7. Create personalized tips for this gig worker
8. Output structured JSON

User ID: {user_id}

Please analyze and provide a complete savings and investment plan."""

            result = await run_autogen_mcp_task(
                agent_name="savings_investment_agent",
                system_prompt=self.system_prompt,
                task=prompt,
                user_id=user_id,
                use_azure=True
            )

            print(f"[Savings Agent] Analysis complete for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "agent": "savings_investment",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[Savings Agent] Error analyzing user {user_id}: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "agent": "savings_investment",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main():
    """Test the savings investment agent"""
    agent = SavingsInvestmentAgent()

    test_user_id = "153735c8-b1e3-4fc6-aa4e-7deb6454990b"

    print(f"Testing Savings & Investment Agent with user {test_user_id}")
    result = await agent.analyze_user(test_user_id)

    print("\nResult:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
