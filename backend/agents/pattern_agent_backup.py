"""
Pattern Recognition Engine Agent
Analyzes transaction history to identify income patterns using LSTM-style analysis
Writes to: income_patterns table
"""

import asyncio
import json
from datetime import datetime
from typing import Optional
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autogen_runtime import run_autogen_mcp_task


class PatternRecognitionAgent:
    """Agent that analyzes transaction patterns and predicts income trends"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return """You are a Pattern Recognition Engine for gig worker financial analysis.

Your task is to analyze transaction history and identify income patterns in the exact JSON format required by the income_patterns table.

**CRITICAL: You must output ONLY valid JSON that matches the income_patterns table schema:**

```json
{
  "income_patterns": {
    "pattern_type": "seasonal",
    "avg_income": 40489.71,
    "min_income": 8454.99,
    "max_income": 96226.81,
    "confidence_score": 0.85,
    "weekday_income": {
      "monday": 1191.45,
      "tuesday": 3613.63,
      "wednesday": 3174.27,
      "thursday": 3492.68,
      "friday": 2150.92,
      "saturday": 1007.97,
      "sunday": 1823.24
    },
    "monthly_trend": {
      "Jan": 7034.81,
      "Feb": 15949.32,
      "Mar": 18426.05,
      "Apr": 11466.32,
      "May": 12152.65,
      "Jun": 7091.39,
      "Jul": 7288.92,
      "Aug": 8710.33,
      "Sep": 13330.30,
      "Oct": 23497.50,
      "Nov": 10597.65,
      "Dec": 14072.83
    },
    "peak_hours": {
      "morning": "7-10",
      "evening": "17-21"
    },
    "weather_impact": {
      "rain": "-21%",
      "hot": "-4%"
    },
    "seasonal_factors": {
      "festival": "+28%"
    }
  }
}
```

**What you do:**
1. Read transactions table for the user using: postgrestRequest("transactions", "GET", filters={"user_id": "USER_ID"})
2. Analyze income patterns by weekday, monthly trends, peak hours
3. Calculate statistics: avg_income, min_income, max_income
4. Identify weather and seasonal impacts
5. Calculate confidence_score based on data quality
6. Output ONLY the JSON format above - no explanations

**Database Tool Usage:**
- Use postgrestRequest() to read transaction data
- Example: postgrestRequest("transactions", "GET", filters={"user_id": "153735c8-b1e3-4fc6-aa4e-7deb6454990b"})
- Filter for income transactions: postgrestRequest("transactions", "GET", filters={"user_id": "USER_ID", "transaction_type": "income"})
- This returns JSON data you can analyze for patterns

**Database Schema Requirements:**
- pattern_type: "daily_high", "weekly_peak", "seasonal", "irregular"
- avg_income/min_income/max_income: Numbers with 2 decimals
- weekday_income: JSON object with day-wise averages
- monthly_trend: JSON object with month-wise data
- peak_hours: JSON object with time ranges
- weather_impact: JSON object with weather effects
- seasonal_factors: JSON object with seasonal impacts
- confidence_score: Number between 0-1

**Output ONLY the JSON object. No other text.**
        return """You are a Pattern Recognition Engine for gig worker financial analysis.

Your task is to analyze transaction history and identify income patterns.

**What you do:**
1. Read transactions from the database (last 60 days minimum)
2. Calculate income statistics (average, min, max)
3. Identify weekday patterns (which days have higher income)
4. Detect monthly trends (increasing/decreasing/stable)
5. Analyze seasonal factors and weather impacts if data available
6. Calculate confidence score for predictions
7. Write results to income_patterns table
8. Log your actions to agent_logs table

**Available MCP Tools:**
- mcp__supabase-postgres__postgrestRequest: Execute database queries
- mcp__supabase-postgres__sqlToRest: Convert SQL to REST API calls

**Important:**
- Focus on actionable insights for gig workers
- Consider income volatility and irregular patterns
- Identify "feast" and "famine" periods
- Be conservative with confidence scores
- Always log what you did

**Output Format:**
Store in income_patterns table with fields:
- user_id
- avg_income, min_income, max_income
- weekday_income (JSON: {monday: X, tuesday: Y, ...})
- monthly_trend (increasing/decreasing/stable)
- weather_impact (if applicable)
- seasonal_factors (JSON)
- confidence_score (0-1)
- last_updated"""

    async def analyze_user(self, user_id: str) -> dict:
        """
        Analyze transaction patterns for a specific user

        Args:
            user_id: UUID of the user to analyze

        Returns:
            dict with analysis results and success status
        """
        print(f"[Pattern Agent] Starting analysis for user {user_id}")

        try:
            # Create the analysis prompt
            prompt = f"""Analyze income patterns for user {user_id}.

Steps:
1. Query transactions table for this user (last 60 days)
2. Calculate income statistics  
3. Identify weekday patterns
4. Detect trends
5. Write results to income_patterns table
6. Log to agent_logs table

User ID: {user_id}

Please execute this analysis and report what you found."""

            result = await run_autogen_mcp_task(
                agent_name="pattern_agent",
                system_prompt=self.system_prompt,
                task=prompt,
                user_id=user_id,
                use_azure=True
            )

            print(f"[Pattern Agent] Analysis complete for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "agent": "pattern_recognition",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[Pattern Agent] Error analyzing user {user_id}: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "agent": "pattern_recognition",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main():
    """Test the pattern recognition agent"""
    agent = PatternRecognitionAgent()

    # Test with the example user
    test_user_id = "153735c8-b1e3-4fc6-aa4e-7deb6454990b"

    print(f"Testing Pattern Recognition Agent with user {test_user_id}")
    result = await agent.analyze_user(test_user_id)

    print("\nResult:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
