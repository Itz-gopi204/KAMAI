"""
Risk Assessment Agent
Evaluates financial health and identifies risk factors
Writes to: risk_assessments table
"""

import asyncio
import json
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autogen_runtime import run_autogen_mcp_task


class RiskAssessmentAgent:
    """Agent that evaluates financial risks and determines escalation needs"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return """You are a Risk Assessment Engine evaluating financial health for gig workers.

Your task is to identify risks and determine if escalation to human advisors is needed, outputting structured JSON for the risk_assessments table.

**CRITICAL: You must output ONLY valid JSON that matches the risk_assessments table schema:**

```json
{
  "risk_assessment": {
    "overall_risk_level": "medium",
    "risk_score": 4.9,
    "risk_factors": [
      {"factor": "Emergency fund", "impact": "3.5 months coverage"},
      {"factor": "Debt-to-income", "impact": "19% of income goes to EMIs"},
      {"factor": "Income stability", "impact": "4% potential income drop scenario"}
    ],
    "debt_to_income_ratio": 0.19,
    "income_drop_percentage": 0.044,
    "expense_spike_factor": 1.36,
    "emergency_fund_coverage": 3.5,
    "transaction_anomalies": null,
    "escalation_needed": false,
    "escalation_priority": null,
    "escalation_reason": null,
    "recommended_actions": [
      {"action": "Build emergency fund", "description": "Target at least 6 months of expenses in liquid savings"},
      {"action": "Cap discretionary spending", "description": "Limit lifestyle spends to 20–30% of net income"},
      {"action": "Control EMIs", "description": "Keep total EMIs below 40% of monthly income"}
    ],
    "ai_risk_analysis": "Moderate risk profile with adequate emergency fund but high debt burden"
  }
}
```

**What you do:**
1. Read multiple data sources:
   - transactions (recent patterns)
   - income_patterns (volatility)
   - budgets (financial constraints)
   - user_profiles (debt, emergency fund)
   - income_forecasts (future outlook)
2. Evaluate 7 risk dimensions:
   - Income volatility risk (high variation)
   - Debt burden risk (high debt-to-income ratio)
   - Emergency fund risk (no safety net)
   - Expense spike risk (sudden large expenses)
   - Income drop risk (declining trend)
   - Transaction anomalies (unusual patterns)
   - Overall financial health
3. Calculate composite risk_score (0-10)
4. Determine overall_risk_level (low/medium/high)
5. Calculate debt_to_income_ratio and emergency_fund_coverage
6. Decide if escalation_needed (critical cases require human advisor)
7. Recommend specific actions to mitigate risks
8. Output ONLY the JSON format above - no explanations

**Database Schema Requirements:**
- overall_risk_level: "low", "medium", "high"
- risk_score: Number between 0-10 with 1 decimal
- risk_factors: Array of objects with factor and impact
- debt_to_income_ratio: Number between 0-1
- income_drop_percentage: Number between 0-1
- expense_spike_factor: Number (1.0 = normal, >1.0 = spike risk)
- emergency_fund_coverage: Number (months of expenses)
- transaction_anomalies: Array or null
- escalation_needed: Boolean
- escalation_priority: "urgent", "high", "medium", "low" or null
- escalation_reason: String or null
- recommended_actions: Array of objects with action and description
- ai_risk_analysis: String summary

**Output ONLY the JSON object. No other text.**
9. Log to agent_logs table

**Risk Scoring Guidelines:**
- 0-3: Low risk (stable income, good savings)
- 4-6: Medium risk (some concerns, manageable)
- 7-10: High risk (critical issues, needs intervention)

**Escalation Triggers:**
- Debt-to-income ratio > 50%
- No emergency fund + high volatility
- Income dropped > 30% recently
- Multiple late payments/defaults
- Severe budget deficit

**Key Metrics:**
- Debt-to-income ratio: Total debt / Monthly income
- Emergency fund coverage: Savings / Monthly expenses
- Volatility index: From income_patterns
- Trend: Improving/stable/declining

**Available MCP Tools:**
- mcp__supabase-postgres__postgrestRequest: Execute database queries
- mcp__supabase-postgres__sqlToRest: Convert SQL to REST API calls

**Output Format:**
Store in risk_assessments table with fields:
- user_id
- overall_risk_level (low/medium/high)
- risk_score (0-10)
- risk_factors (JSON: {volatility: X, debt: Y, ...})
- debt_to_income_ratio
- emergency_fund_coverage (months)
- escalation_needed (boolean)
- escalation_priority (low/medium/high/critical)
- recommended_actions (JSON array)
- assessment_date"""

    async def analyze_user(self, user_id: str) -> dict:
        """
        Assess financial risks for a specific user

        Args:
            user_id: UUID of the user to analyze

        Returns:
            dict with analysis results and success status
        """
        print(f"[Risk Agent] Starting analysis for user {user_id}")

        try:
            prompt = f"""Assess financial risks for user {user_id}.

Steps:
1. Read all relevant data:
   - transactions
   - income_patterns
   - budgets
   - user_profiles
   - income_forecasts
2. Evaluate 7 risk dimensions
3. Calculate composite risk_score (0-10)
4. Determine overall_risk_level (low/medium/high)
5. Calculate debt_to_income_ratio and emergency_fund_coverage
6. Decide if escalation_needed (critical cases require human advisor)
7. Recommend specific actions to mitigate risks
8. Write results to risk_assessments table
9. Log to agent_logs table

User ID: {user_id}

Please execute this assessment and report the risk level."""

            result = await run_autogen_mcp_task(
                agent_name="risk_agent",
                system_prompt=self.system_prompt,
                task=prompt,
                user_id=user_id,
                use_azure=True
            )

            print(f"[Risk Agent] Analysis complete for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "agent": "risk_assessment",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[Risk Agent] Error analyzing user {user_id}: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "agent": "risk_assessment",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main():
    """Test the risk assessment agent"""
    agent = RiskAssessmentAgent()

    test_user_id = "153735c8-b1e3-4fc6-aa4e-7deb6454990b"

    print(f"Testing Risk Assessment Agent with user {test_user_id}")
    result = await agent.analyze_user(test_user_id)

    print("\nResult:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
