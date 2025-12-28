import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useApp } from "@/contexts/AppContext";
import TransactionInputCard from "@/components/TransactionInputCard";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, Sparkles, TrendingUp, Shield, Zap, Lightbulb, Wallet, AlertTriangle, Receipt } from "lucide-react";
import { motion } from "framer-motion";
import db from "@/services/database";
import type { Transaction } from "@/services/database";
import PageIntro from "@/components/PageIntro";
import AIAnalysisStatus from "@/components/AIAnalysisStatus";

const Dashboard = () => {
  const { user, isAuthenticated } = useApp();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [todaySummary, setTodaySummary] = useState({ income: 0, expense: 0, count: 0 });
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([]);
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!isAuthenticated && !userId) {
      navigate("/login");
      return;
    }
    // Load data if authenticated OR if user_id exists (for testing)
    if (isAuthenticated || userId) {
      loadData();
    }
  }, [isAuthenticated, navigate]);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const summary = await db.transactions.getTodaySummary();
      setTodaySummary(summary);

      const transactions = await db.transactions.getAll({
        date_start: new Date().toISOString().split("T")[0],
        date_end: new Date().toISOString().split("T")[0],
      });
      setRecentTransactions(transactions.slice(0, 5));

      // Calculate balance from all transactions
      const allTransactions = await db.transactions.getAll();
      const total = allTransactions.reduce((sum, t) => {
        return sum + (t.transaction_type === "income" ? t.amount : -t.amount);
      }, 0);
      setBalance(total);
    } catch (error) {
      console.error("Failed to load data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  const features = [
    {
      icon: Sparkles,
      title: "AI-Powered Insights",
      description: "Get personalized financial recommendations",
      color: "from-blue-500 to-blue-600",
    },
    {
      icon: Wallet,
      title: "Dynamic Budgeting",
      description: "Feast and famine week budgets",
      color: "from-green-500 to-green-600",
    },
    {
      icon: AlertTriangle,
      title: "Risk Analysis",
      description: "Monitor your financial health",
      color: "from-red-500 to-red-600",
    },
    {
      icon: Receipt,
      title: "Tax Automation",
      description: "Auto-calculate and file ITR",
      color: "from-purple-500 to-purple-600",
    },
  ];

  return (
    <div className="space-y-8">
      {/* Header Section - Asymmetric, natural spacing */}
      <div className="space-y-1">
        <h1 className="text-[32px] font-semibold tracking-tight text-foreground">
          Good {new Date().getHours() < 12 ? "Morning" : new Date().getHours() < 18 ? "Afternoon" : "Evening"}
          {user?.name?.split(" ")[0] && `, ${user.name.split(" ")[0]}`}
          </h1>
        <p className="text-[15px] text-muted-foreground font-normal">Here's your financial overview</p>
      </div>

      <PageIntro
        title="What is this page?"
        description="This is your daily money hub. Add today's income and expenses from here and see a quick overview of how you're doing."
      />

      {/* AI Analysis Status */}
      <AIAnalysisStatus />

      {/* Transaction Input Card */}
                <div>
        <TransactionInputCard onSuccess={loadData} />
            </div>

      {/* Summary Cards - Asymmetric grid, real shadows */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-background border border-border/40 rounded-[6px] p-5 shadow-[0_1px_2px_0_rgba(0,0,0,0.05)] hover:shadow-[0_2px_4px_0_rgba(0,0,0,0.08)] transition-shadow">
          <p className="text-[13px] text-muted-foreground font-medium mb-1.5">Today's Income</p>
          <p className="text-[28px] font-semibold tracking-tight text-[#16a34a]">
            ₹{todaySummary.income.toLocaleString("en-IN")}
          </p>
                </div>
        <div className="bg-background border border-border/40 rounded-[6px] p-5 shadow-[0_1px_2px_0_rgba(0,0,0,0.05)] hover:shadow-[0_2px_4px_0_rgba(0,0,0,0.08)] transition-shadow">
          <p className="text-[13px] text-muted-foreground font-medium mb-1.5">Today's Expenses</p>
          <p className="text-[28px] font-semibold tracking-tight text-[#dc2626]">
            ₹{todaySummary.expense.toLocaleString("en-IN")}
          </p>
              </div>
        <div className="bg-background border border-border/40 rounded-[6px] p-5 shadow-[0_1px_2px_0_rgba(0,0,0,0.05)] hover:shadow-[0_2px_4px_0_rgba(0,0,0,0.08)] transition-shadow md:col-span-1">
          <p className="text-[13px] text-muted-foreground font-medium mb-1.5">Current Balance</p>
          <p className="text-[28px] font-semibold tracking-tight text-foreground">
            ₹{balance.toLocaleString("en-IN")}
          </p>
                </div>
        </div>

      {/* Recent Transactions - Section with divider */}
      {recentTransactions.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-[20px] font-semibold tracking-tight text-foreground">Recent Transactions</h2>
            <button
              onClick={() => navigate("/transactions")}
              className="text-[13px] text-muted-foreground hover:text-foreground font-medium transition-colors"
            >
              View All →
            </button>
          </div>
          <div className="bg-background border border-border/40 rounded-[6px] shadow-[0_1px_2px_0_rgba(0,0,0,0.05)] overflow-hidden">
            {recentTransactions.map((transaction, index) => (
              <div
                key={transaction.transaction_id}
                className={`flex items-center justify-between px-4 py-3.5 transition-colors hover:bg-muted/30 ${
                  index !== recentTransactions.length - 1 ? "border-b border-border/30" : ""
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-9 h-9 rounded-[5px] flex items-center justify-center text-[13px] font-semibold ${
                      transaction.transaction_type === "income"
                        ? "bg-[#dcfce7] text-[#16a34a]"
                        : "bg-[#fee2e2] text-[#dc2626]"
                    }`}
                  >
                    {transaction.transaction_type === "income" ? "+" : "−"}
                  </div>
                      <div>
                    <div className="text-[14px] font-medium text-foreground">{transaction.category || "Uncategorized"}</div>
                    <div className="text-[12px] text-muted-foreground mt-0.5">
                      {transaction.transaction_time || "N/A"} • {transaction.description || "No description"}
                    </div>
                      </div>
                    </div>
                    <div
                  className={`text-[15px] font-semibold tracking-tight ${
                    transaction.transaction_type === "income"
                      ? "text-[#16a34a]"
                      : "text-[#dc2626]"
                  }`}
                >
                  {transaction.transaction_type === "income" ? "+" : "−"}₹
                  {transaction.amount.toLocaleString("en-IN")}
                </div>
                    </div>
                ))}
              </div>
          </div>
      )}

      {/* Feature Section - Asymmetric layout */}
                      <div>
        <div className="mb-4">
          <h2 className="text-[20px] font-semibold tracking-tight text-foreground mb-1.5">What is Agente AI?</h2>
          <p className="text-[14px] text-muted-foreground leading-relaxed">
            Your personal finance coach for the gig economy. Smart insights, better savings, brighter future.
          </p>
                      </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className="bg-background border border-border/40 rounded-[6px] p-5 shadow-[0_1px_2px_0_rgba(0,0,0,0.05)] hover:shadow-[0_2px_4px_0_rgba(0,0,0,0.08)] transition-all hover:-translate-y-0.5"
              >
                <div className={`w-10 h-10 rounded-[5px] bg-gradient-to-br ${feature.color} flex items-center justify-center mb-3.5`}>
                  <Icon className="w-5 h-5 text-white" />
                    </div>
                <h3 className="text-[14px] font-semibold text-foreground mb-1.5">{feature.title}</h3>
                <p className="text-[12px] text-muted-foreground leading-relaxed">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
