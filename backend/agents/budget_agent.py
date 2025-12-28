"""
Budget Analysis Engine Agent
Calculates feast/famine budgets based on income patterns
Writes to: budgets table
"""

import asyncio
import json
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autogen_runtime import run_autogen_mcp_task


class BudgetAnalysisAgent:
    """Agent that creates feast/famine week budgets for gig workers"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return """You are a Budget Analysis Engine for gig worker financial planning.

Your task is to create realistic feast/famine budgets based on income volatility and write them to the budgets table in the exact JSON format required.

**CRITICAL: You must output ONLY valid JSON that matches the budgets table schema:**

```json
{
  "budgets": [
    {
      "budget_type": "feast_week",
      "valid_from": "2025-12-28",
      "valid_until": "2025-12-31", 
      "total_income_expected": 45000.00,
      "fixed_costs": {"rent": 12000, "emi": 5000},
      "variable_costs": {"food": 3000, "fuel": 2000, "utilities": 1500},
      "savings_target": 15000.00,
      "discretionary_budget": 6000.00,
      "category_limits": {"food": 3500, "fuel": 2500, "entertainment": 2000},
      "confidence_score": 0.85
    },
    {
      "budget_type": "famine_week", 
      "valid_from": "2025-12-28",
      "valid_until": "2025-12-31",
      "total_income_expected": 15000.00,
      "fixed_costs": {"rent": 12000, "emi": 5000},
      "variable_costs": {"food": 2000, "fuel": 1000, "utilities": 1000},
      "savings_target": 0.00,
      "discretionary_budget": 0.00,
      "category_limits": {"food": 2500, "fuel": 1500, "entertainment": 0},
      "confidence_score": 0.75
    }
  ]
}
```

**What you do:**
1. Read income_patterns table for the user using: postgrestRequest("income_patterns", "GET", filters={"user_id": "USER_ID"})
2. Read user_profiles for fixed costs using: postgrestRequest("user_profiles", "GET", filters={"user_id": "USER_ID"})
3. Read transactions for spending analysis using: postgrestRequest("transactions", "GET", filters={"user_id": "USER_ID"})
4. Calculate feast_week, famine_week, and monthly budgets
5. Output ONLY the JSON format above - no explanations
6. Use realistic amounts based on Indian gig worker context
7. Ensure all required fields are present

**Database Tool Usage:**
- Use postgrestRequest() to read data from tables
- Example: postgrestRequest("income_patterns", "GET", filters={"user_id": "153735c8-b1e3-4fc6-aa4e-7deb6454990b"})
- This returns JSON data you can analyze for budget calculations

**Budget Categories:**
- Fixed costs: Rent, EMIs, subscriptions (from user_profile)
- Variable costs: Food, transportation, utilities  
- Discretionary: Entertainment, dining out
- Savings: Emergency fund, goals

**Feast/Famine Budgeting:**
- Feast week: When income > average, allocate more to savings/debt
- Famine week: When income < average, focus on essentials only
- Monthly: Balanced budget assuming average income

**Database Schema Requirements:**
- budget_type: "feast_week", "famine_week", or "monthly"
- valid_from/valid_until: Date strings in YYYY-MM-DD format
- total_income_expected: Number with 2 decimals
- fixed_costs/variable_costs/category_limits: JSON objects
- savings_target/discretionary_budget: Numbers with 2 decimals
- confidence_score: Number between 0-1

**Output ONLY the JSON array. No other text.**
- Debt repayment: Credit cards, loans

**Available MCP Tools:**
- mcp__supabase-postgres__postgrestRequest: Execute database queries
- mcp__supabase-postgres__sqlToRest: Convert SQL to REST API calls

**Output Format:**
Store in budgets table with fields:
- user_id
- budget_type (feast_week/famine_week/monthly)
- total_income_expected
- fixed_costs (JSON)
- variable_costs (JSON)
- savings_target
- discretionary_budget
- category_limits (JSON)
- created_at"""

    async def analyze_user(self, user_id: str) -> dict:
        """
        Create budget plans for a specific user

        Args:
            user_id: UUID of the user to analyze

        Returns:
            dict with analysis results and success status
        """
        print(f"[Budget Agent] Starting analysis for user {user_id}")

        try:
            prompt = f"""Create feast/famine budgets for user {user_id}.

Steps:
1. Read income_patterns for user {user_id}
2. Read user_profiles for fixed costs
3. Create three budgets:
   - feast_week (high income period)
   - famine_week (low income period)
   - monthly (averaged)
4. Write all three budgets to budgets table
5. Log to agent_logs table

User ID: {user_id}

Please execute this analysis and report the budgets created."""

            result = await run_autogen_mcp_task(
                agent_name="budget_agent",
                system_prompt=self.system_prompt,
                task=prompt,
                user_id=user_id,
                use_azure=True
            )

            print(f"[Budget Agent] Analysis complete for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "agent": "budget_analysis",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[Budget Agent] Error analyzing user {user_id}: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "agent": "budget_analysis",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main():
    """Test the budget analysis agent"""
    agent = BudgetAnalysisAgent()

    test_user_id = "153735c8-b1e3-4fc6-aa4e-7deb6454990b"

    print(f"Testing Budget Analysis Agent with user {test_user_id}")
    result = await agent.analyze_user(test_user_id)

    print("\nResult:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
