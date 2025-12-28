-- ============================================================================
-- NEW TABLES FOR HACKATHON REQUIREMENTS
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/YOUR_PROJECT/sql
-- ============================================================================

-- ============================================================================
-- 1. SAVINGS GOALS TABLE
-- For: Savings & Investment Agent
-- ============================================================================
CREATE TABLE IF NOT EXISTS savings_goals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
  goal_type TEXT NOT NULL DEFAULT 'savings',
  goal_name TEXT NOT NULL,
  target_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
  current_amount DECIMAL(12,2) DEFAULT 0,
  monthly_contribution DECIMAL(12,2) DEFAULT 0,
  priority TEXT DEFAULT 'medium' CHECK (priority IN ('high', 'medium', 'low')),
  status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed', 'paused')),
  reasoning TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_savings_goals_user_id ON savings_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_savings_goals_status ON savings_goals(status);

-- ============================================================================
-- 2. INVESTMENT RECOMMENDATIONS TABLE
-- For: Savings & Investment Agent
-- ============================================================================
CREATE TABLE IF NOT EXISTS investment_recommendations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
  investment_type TEXT NOT NULL,
  provider TEXT,
  recommended_amount DECIMAL(12,2) DEFAULT 0,
  frequency TEXT DEFAULT 'monthly',
  expected_return DECIMAL(5,2) DEFAULT 0,
  risk_level TEXT DEFAULT 'low' CHECK (risk_level IN ('low', 'moderate', 'high')),
  min_lock_in_months INTEGER DEFAULT 0,
  reasoning TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_investment_recommendations_user_id ON investment_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_investment_recommendations_risk ON investment_recommendations(risk_level);

-- ============================================================================
-- 3. BILLS TABLE
-- For: Bill Payment Agent
-- ============================================================================
CREATE TABLE IF NOT EXISTS bills (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
  bill_name TEXT NOT NULL,
  bill_type TEXT DEFAULT 'utility' CHECK (bill_type IN ('rent', 'emi', 'utility', 'telecom', 'insurance', 'subscription', 'tax', 'other')),
  amount DECIMAL(12,2) NOT NULL DEFAULT 0,
  due_date DATE,
  frequency TEXT DEFAULT 'monthly' CHECK (frequency IN ('daily', 'weekly', 'monthly', 'quarterly', 'annual', 'one_time')),
  priority TEXT DEFAULT 'medium' CHECK (priority IN ('critical', 'high', 'medium', 'low')),
  auto_pay_recommended BOOLEAN DEFAULT false,
  auto_pay_enabled BOOLEAN DEFAULT false,
  payment_method TEXT DEFAULT 'upi',
  late_fee DECIMAL(10,2) DEFAULT 0,
  grace_period_days INTEGER DEFAULT 0,
  remaining_emis INTEGER,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'overdue', 'scheduled', 'cancelled')),
  last_paid_date DATE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_bills_user_id ON bills(user_id);
CREATE INDEX IF NOT EXISTS idx_bills_due_date ON bills(due_date);
CREATE INDEX IF NOT EXISTS idx_bills_status ON bills(status);

-- ============================================================================
-- 4. BILL PAYMENT SCHEDULE TABLE
-- For: Bill Payment Agent - Payment planning
-- ============================================================================
CREATE TABLE IF NOT EXISTS bill_payment_schedule (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
  bill_id UUID REFERENCES bills(id) ON DELETE CASCADE,
  pay_date DATE NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  income_source TEXT,
  confidence DECIMAL(3,2) DEFAULT 0.5,
  status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'paid', 'missed', 'rescheduled')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_bill_payment_schedule_user_id ON bill_payment_schedule(user_id);
CREATE INDEX IF NOT EXISTS idx_bill_payment_schedule_pay_date ON bill_payment_schedule(pay_date);

-- ============================================================================
-- 5. FINANCIAL GOALS TABLE
-- For: Goals Agent - Goal-based planning with explanations
-- ============================================================================
CREATE TABLE IF NOT EXISTS financial_goals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
  goal_name TEXT NOT NULL,
  goal_type TEXT DEFAULT 'savings' CHECK (goal_type IN ('emergency_fund', 'asset_purchase', 'education', 'healthcare', 'retirement', 'lifestyle', 'business', 'debt_repayment', 'savings', 'other')),
  description TEXT,
  target_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
  current_amount DECIMAL(12,2) DEFAULT 0,
  target_date DATE,
  priority INTEGER DEFAULT 1 CHECK (priority >= 1 AND priority <= 5),
  status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed', 'paused')),
  monthly_target DECIMAL(12,2) DEFAULT 0,
  progress_percentage DECIMAL(5,2) DEFAULT 0,
  explanation JSONB DEFAULT '{}',
  milestones JSONB DEFAULT '[]',
  action_steps JSONB DEFAULT '[]',
  potential_obstacles JSONB DEFAULT '[]',
  contingency_plan TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_financial_goals_user_id ON financial_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_financial_goals_status ON financial_goals(status);
CREATE INDEX IF NOT EXISTS idx_financial_goals_priority ON financial_goals(priority);

-- ============================================================================
-- 6. GOAL MILESTONES TABLE (Optional - for detailed milestone tracking)
-- ============================================================================
CREATE TABLE IF NOT EXISTS goal_milestones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  goal_id UUID REFERENCES financial_goals(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
  milestone_name TEXT NOT NULL,
  target_amount DECIMAL(12,2) DEFAULT 0,
  target_date DATE,
  status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
  reward TEXT,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_goal_milestones_goal_id ON goal_milestones(goal_id);

-- ============================================================================
-- ENABLE ROW LEVEL SECURITY (RLS) FOR ALL NEW TABLES
-- ============================================================================

-- Enable RLS
ALTER TABLE savings_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE investment_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE bills ENABLE ROW LEVEL SECURITY;
ALTER TABLE bill_payment_schedule ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE goal_milestones ENABLE ROW LEVEL SECURITY;

-- Create policies for savings_goals
CREATE POLICY "Users can view own savings_goals" ON savings_goals FOR SELECT USING (auth.uid()::text = user_id::text OR true);
CREATE POLICY "Users can insert own savings_goals" ON savings_goals FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update own savings_goals" ON savings_goals FOR UPDATE USING (true);
CREATE POLICY "Users can delete own savings_goals" ON savings_goals FOR DELETE USING (true);

-- Create policies for investment_recommendations
CREATE POLICY "Users can view own investment_recommendations" ON investment_recommendations FOR SELECT USING (true);
CREATE POLICY "Users can insert own investment_recommendations" ON investment_recommendations FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update own investment_recommendations" ON investment_recommendations FOR UPDATE USING (true);
CREATE POLICY "Users can delete own investment_recommendations" ON investment_recommendations FOR DELETE USING (true);

-- Create policies for bills
CREATE POLICY "Users can view own bills" ON bills FOR SELECT USING (true);
CREATE POLICY "Users can insert own bills" ON bills FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update own bills" ON bills FOR UPDATE USING (true);
CREATE POLICY "Users can delete own bills" ON bills FOR DELETE USING (true);

-- Create policies for bill_payment_schedule
CREATE POLICY "Users can view own bill_payment_schedule" ON bill_payment_schedule FOR SELECT USING (true);
CREATE POLICY "Users can insert own bill_payment_schedule" ON bill_payment_schedule FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update own bill_payment_schedule" ON bill_payment_schedule FOR UPDATE USING (true);
CREATE POLICY "Users can delete own bill_payment_schedule" ON bill_payment_schedule FOR DELETE USING (true);

-- Create policies for financial_goals
CREATE POLICY "Users can view own financial_goals" ON financial_goals FOR SELECT USING (true);
CREATE POLICY "Users can insert own financial_goals" ON financial_goals FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update own financial_goals" ON financial_goals FOR UPDATE USING (true);
CREATE POLICY "Users can delete own financial_goals" ON financial_goals FOR DELETE USING (true);

-- Create policies for goal_milestones
CREATE POLICY "Users can view own goal_milestones" ON goal_milestones FOR SELECT USING (true);
CREATE POLICY "Users can insert own goal_milestones" ON goal_milestones FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update own goal_milestones" ON goal_milestones FOR UPDATE USING (true);
CREATE POLICY "Users can delete own goal_milestones" ON goal_milestones FOR DELETE USING (true);

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================
SELECT 'All new tables created successfully!' as status;
