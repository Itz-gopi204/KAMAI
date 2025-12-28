"""
Income Volatility Forecaster Agent
Predicts 30-day income scenarios (pessimistic, realistic, optimistic)
Writes to: income_forecasts table
"""

import asyncio
import json
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autogen_runtime import run_autogen_mcp_task


class VolatilityForecasterAgent:
    """Agent that forecasts income volatility and creates 30-day predictions"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return """You are an Income Volatility Forecaster for gig workers.

Your task is to predict 30-day income scenarios and calculate volatility metrics, outputting structured JSON for the income_forecasts table.

**CRITICAL: You must output ONLY valid JSON that matches the income_forecasts table schema:**

```json
{
  "income_forecast": {
    "forecast_period_days": 30,
    "pessimistic_scenario": {
      "expected_income": 35000.00,
      "confidence": 0.15,
      "daily_average": 1166.67,
      "risk_factors": ["Seasonal decline", "Weather impact", "Market saturation"]
    },
    "realistic_scenario": {
      "expected_income": 45000.00,
      "confidence": 0.65,
      "daily_average": 1500.00,
      "risk_factors": ["Normal market conditions"]
    },
    "optimistic_scenario": {
      "expected_income": 55000.00,
      "confidence": 0.20,
      "daily_average": 1833.33,
      "risk_factors": ["Festival season", "Increased demand"]
    },
    "volatility_score": 0.42,
    "volatility_category": "moderate",
    "trend_direction": "stable",
    "seasonal_adjustment": 1.1,
    "market_conditions": "normal",
    "forecast_confidence": 0.68,
    "recommendation": "Maintain 3-month emergency fund due to moderate volatility"
  }
}
```

**What you do:**
1. Read income_patterns and transactions data
2. Analyze historical volatility patterns
3. Calculate 3 scenarios: pessimistic, realistic, optimistic
4. Determine volatility_score (0-1) and category
5. Identify trend_direction and seasonal_adjustment
6. Generate confidence scores for each scenario
7. Provide actionable recommendation
8. Output ONLY the JSON format above - no explanations

**Database Schema Requirements:**
- forecast_period_days: Number (30, 60, 90)
- pessimistic/realistic/optimistic_scenario: Objects with expected_income, confidence, daily_average, risk_factors
- volatility_score: Number between 0-1
- volatility_category: "low", "moderate", "high"
- trend_direction: "increasing", "stable", "decreasing"
- seasonal_adjustment: Number (multiplier)
- market_conditions: "favorable", "normal", "challenging"
- forecast_confidence: Number between 0-1
- recommendation: String

**Output ONLY the JSON object. No other text.**
1. Read income_patterns for historical trends
2. Read transactions to understand income volatility
3. Consider contextual factors from income_patterns
4. Create three 30-day forecast scenarios:
   - Pessimistic (worst case - 10th percentile)
   - Realistic (expected case - median)
   - Optimistic (best case - 90th percentile)
5. Calculate volatility index (0-1, higher = more volatile)
6. Determine forecast confidence based on data quality
7. Provide AI reasoning for the forecast
8. Write results to income_forecasts table
9. Log your actions to agent_logs table

**Volatility Considerations:**
- Historical income variance
- Seasonal patterns
- Recent trend direction
- External factors (weather, festivals)
- Gig work type (delivery, driving, freelance)

**Scenario Guidelines:**
- Pessimistic: Assume 2-3 bad weeks in the month
- Realistic: Based on moving average trend
- Optimistic: Assume 2-3 good weeks in the month
- Range should reflect actual historical volatility

**Available MCP Tools:**
- mcp__supabase-postgres__postgrestRequest: Execute database queries
- mcp__supabase-postgres__sqlToRest: Convert SQL to REST API calls

**Output Format:**
Store in income_forecasts table with fields:
- user_id
- forecast_month
- pessimistic_scenario (JSON: {week1: X, week2: Y, ...})
- realistic_scenario (JSON)
- optimistic_scenario (JSON)
- forecast_range_min, forecast_range_max
- volatility_index (0-1)
- forecast_confidence (0-1)
- ai_reasoning (text explanation)
- created_at"""

    async def analyze_user(self, user_id: str) -> dict:
        """
        Create 30-day income forecast for a specific user

        Args:
            user_id: UUID of the user to analyze

        Returns:
            dict with analysis results and success status
        """
        print(f"[Volatility Agent] Starting analysis for user {user_id}")

        try:
            prompt = f"""Create 30-day income forecast for user {user_id}.

Steps:
1. Read income_patterns and transactions for user {user_id}
2. Calculate historical volatility
3. Create three scenarios (pessimistic, realistic, optimistic)
4. Calculate volatility_index and forecast_confidence
5. Write detailed reasoning for your forecast
6. Write results to income_forecasts table
7. Log to agent_logs table

User ID: {user_id}

Please execute this analysis and report your forecasts."""

            result = await run_autogen_mcp_task(
                agent_name="volatility_agent",
                system_prompt=self.system_prompt,
                task=prompt,
                user_id=user_id,
                use_azure=True
            )

            print(f"[Volatility Agent] Analysis complete for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "agent": "volatility_forecaster",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[Volatility Agent] Error analyzing user {user_id}: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "agent": "volatility_forecaster",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main():
    """Test the volatility forecaster agent"""
    agent = VolatilityForecasterAgent()

    test_user_id = "153735c8-b1e3-4fc6-aa4e-7deb6454990b"

    print(f"Testing Volatility Forecaster Agent with user {test_user_id}")
    result = await agent.analyze_user(test_user_id)

    print("\nResult:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
