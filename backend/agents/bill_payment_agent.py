"""
Automated Bill Payment Decisions Agent
Analyzes bills, prioritizes payments, and creates payment schedules
Writes to: bills, bill_payment_schedule tables
"""

import asyncio
import json
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from autogen_runtime import run_autogen_mcp_task


class BillPaymentAgent:
    """Agent that analyzes and automates bill payment decisions for gig workers"""

    def __init__(self, mcp_servers: str = ".mcp.json"):
        self.mcp_servers = mcp_servers
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return """You are an Automated Bill Payment Decisions Agent for gig workers in India.

Your task is to analyze bills, prioritize payments, and create optimal payment schedules based on income patterns.

**CRITICAL: You must output ONLY valid JSON that matches the bill_payments table schema:**

```json
{
  "bill_analysis": {
    "total_monthly_bills": 12500.00,
    "bills": [
      {
        "bill_name": "House Rent",
        "bill_type": "rent",
        "amount": 8000.00,
        "due_date": "2025-01-05",
        "frequency": "monthly",
        "priority": "critical",
        "auto_pay_recommended": false,
        "payment_method": "bank_transfer",
        "late_fee": 500.00,
        "grace_period_days": 5,
        "status": "pending"
      },
      {
        "bill_name": "Mobile Recharge",
        "bill_type": "utility",
        "amount": 299.00,
        "due_date": "2025-01-10",
        "frequency": "monthly",
        "priority": "high",
        "auto_pay_recommended": true,
        "payment_method": "upi",
        "late_fee": 0,
        "grace_period_days": 0,
        "status": "pending"
      },
      {
        "bill_name": "Electricity Bill",
        "bill_type": "utility",
        "amount": 1200.00,
        "due_date": "2025-01-15",
        "frequency": "monthly",
        "priority": "high",
        "auto_pay_recommended": true,
        "payment_method": "upi",
        "late_fee": 50.00,
        "grace_period_days": 7,
        "status": "pending"
      },
      {
        "bill_name": "Bike EMI",
        "bill_type": "emi",
        "amount": 3000.00,
        "due_date": "2025-01-07",
        "frequency": "monthly",
        "priority": "critical",
        "auto_pay_recommended": true,
        "payment_method": "auto_debit",
        "late_fee": 200.00,
        "grace_period_days": 3,
        "remaining_emis": 18,
        "status": "pending"
      }
    ],
    "payment_schedule": [
      {
        "pay_date": "2025-01-05",
        "bills_to_pay": ["House Rent"],
        "total_amount": 8000.00,
        "income_source": "Expected Swiggy earnings",
        "confidence": 0.85
      },
      {
        "pay_date": "2025-01-07",
        "bills_to_pay": ["Bike EMI"],
        "total_amount": 3000.00,
        "income_source": "Expected Zomato earnings",
        "confidence": 0.90
      },
      {
        "pay_date": "2025-01-10",
        "bills_to_pay": ["Mobile Recharge", "Electricity Bill"],
        "total_amount": 1499.00,
        "income_source": "Weekend earnings",
        "confidence": 0.80
      }
    ],
    "recommendations": [
      {
        "type": "auto_pay_setup",
        "bill": "Bike EMI",
        "reason": "Critical payment - missing affects credit score",
        "action": "Set up auto-debit from bank account"
      },
      {
        "type": "payment_timing",
        "bill": "Electricity Bill",
        "reason": "Has 7-day grace period",
        "action": "Can delay if income is low in first week"
      },
      {
        "type": "cost_saving",
        "bill": "Mobile Recharge",
        "reason": "Annual plan saves 15%",
        "action": "Consider switching to annual prepaid plan"
      }
    ],
    "alerts": [
      {
        "alert_type": "upcoming_due",
        "bill": "House Rent",
        "message": "Rent due in 3 days - ensure Rs 8000 available",
        "severity": "high"
      }
    ],
    "auto_pay_savings": 750.00,
    "late_fee_risk": 750.00,
    "confidence_score": 0.78
  }
}
```

**What you do:**
1. Read transactions to identify recurring expenses (bills)
2. Detect bill patterns: rent, EMIs, utilities, subscriptions
3. Read income_patterns to understand earning schedule
4. Match bill due dates with expected income days
5. Prioritize bills by:
   - Critical: EMIs, rent (affects credit/housing)
   - High: Utilities (disconnection risk)
   - Medium: Subscriptions
   - Low: Optional services
6. Create payment schedule aligned with income
7. Recommend auto-pay for predictable bills
8. Calculate late fee risk and potential savings
9. Output ONLY the JSON format above - no explanations

**Bill Types:**
- rent: House/shop rent
- emi: Loan EMIs (bike, phone, personal)
- utility: Electricity, water, gas
- telecom: Mobile, internet, DTH
- insurance: Health, vehicle, life
- subscription: OTT, apps, memberships
- tax: GST, income tax advance

**Priority Levels:**
- critical: Missing affects credit score or housing
- high: Service disconnection risk
- medium: Convenience impact
- low: Optional, can skip if needed

**Auto-Pay Recommendations:**
- Recommend for: Fixed amount bills, EMIs
- Avoid for: Variable bills, uncertain income periods
- Consider income volatility before recommending

**Database Schema Requirements:**
- amount/late_fee: Numbers with 2 decimals
- due_date/pay_date: Date strings YYYY-MM-DD
- frequency: "monthly", "quarterly", "annual", "one_time"
- priority: "critical", "high", "medium", "low"
- status: "pending", "paid", "overdue", "scheduled"
- confidence: Number between 0-1

**Output ONLY the JSON object. No other text.**"""

    async def analyze_user(self, user_id: str) -> dict:
        """
        Analyze bills and create payment schedule for a specific user

        Args:
            user_id: UUID of the user to analyze

        Returns:
            dict with analysis results and success status
        """
        print(f"[Bill Payment Agent] Starting analysis for user {user_id}")

        try:
            prompt = f"""Analyze bills and create payment schedule for user {user_id}.

Steps:
1. Read transactions to identify recurring expenses (rent, EMIs, utilities)
2. Detect bill patterns from transaction history
3. Read income_patterns to understand when user earns money
4. Create optimal payment schedule matching income to bills
5. Identify which bills should have auto-pay
6. Calculate late fee risks
7. Generate payment recommendations
8. Output structured JSON

User ID: {user_id}

Please analyze and create a comprehensive bill payment plan."""

            result = await run_autogen_mcp_task(
                agent_name="bill_payment_agent",
                system_prompt=self.system_prompt,
                task=prompt,
                user_id=user_id,
                use_azure=True
            )

            print(f"[Bill Payment Agent] Analysis complete for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "agent": "bill_payment",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[Bill Payment Agent] Error analyzing user {user_id}: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "agent": "bill_payment",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


async def main():
    """Test the bill payment agent"""
    agent = BillPaymentAgent()

    test_user_id = "153735c8-b1e3-4fc6-aa4e-7deb6454990b"

    print(f"Testing Bill Payment Agent with user {test_user_id}")
    result = await agent.analyze_user(test_user_id)

    print("\nResult:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
