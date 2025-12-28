-- ============================================
-- FIX: Users Table Schema for Signup
-- Run this in Supabase SQL Editor
-- ============================================

-- Step 1: Drop existing users table (WARNING: This deletes all data!)
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;
DROP TABLE IF EXISTS budgets CASCADE;
DROP TABLE IF EXISTS recommendations CASCADE;
DROP TABLE IF EXISTS savings_goals CASCADE;
DROP TABLE IF EXISTS investment_recommendations CASCADE;
DROP TABLE IF EXISTS bills CASCADE;
DROP TABLE IF EXISTS financial_goals CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Step 2: Create users table with correct schema
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) DEFAULT '',
    occupation VARCHAR(100) DEFAULT '',
    city VARCHAR(100) DEFAULT '',
    state VARCHAR(100) DEFAULT '',
    pin_code VARCHAR(10) DEFAULT '',
    date_of_birth DATE DEFAULT NULL,
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT true,
    kyc_verified BOOLEAN DEFAULT false,
    onboarding_completed BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 3: Disable RLS to allow signups
ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- Step 4: Create transactions table
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
    transaction_time TIME DEFAULT CURRENT_TIME,
    amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    transaction_type VARCHAR(10) DEFAULT 'expense' CHECK (transaction_type IN ('income', 'expense')),
    category VARCHAR(50) DEFAULT 'Other',
    subcategory VARCHAR(50) DEFAULT '',
    description TEXT DEFAULT '',
    payment_method VARCHAR(50) DEFAULT 'cash',
    merchant_name VARCHAR(100) DEFAULT '',
    location VARCHAR(100) DEFAULT '',
    source VARCHAR(50) DEFAULT '',
    account_id UUID DEFAULT NULL,
    input_method VARCHAR(20) DEFAULT 'manual',
    verified BOOLEAN DEFAULT true,
    confidence_score DECIMAL(3,2) DEFAULT 1.0,
    is_recurring BOOLEAN DEFAULT false,
    recurring_frequency VARCHAR(20) DEFAULT NULL,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;

-- Step 5: Create other required tables
CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    monthly_income_min DECIMAL(12,2) DEFAULT 0,
    monthly_income_max DECIMAL(12,2) DEFAULT 0,
    monthly_expenses_avg DECIMAL(12,2) DEFAULT 0,
    emergency_fund_target DECIMAL(12,2) DEFAULT 0,
    current_emergency_fund DECIMAL(12,2) DEFAULT 0,
    risk_tolerance VARCHAR(20) DEFAULT 'moderate',
    financial_goals JSONB DEFAULT '{}',
    income_sources JSONB DEFAULT '{}',
    debt_obligations JSONB DEFAULT '{}',
    dependents INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY;

CREATE TABLE budgets (
    budget_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    budget_type VARCHAR(20) DEFAULT 'normal',
    valid_from DATE DEFAULT CURRENT_DATE,
    valid_until DATE DEFAULT (CURRENT_DATE + INTERVAL '1 month'),
    total_income_expected DECIMAL(12,2) DEFAULT 0,
    fixed_costs JSONB DEFAULT '{}',
    variable_costs JSONB DEFAULT '{}',
    savings_target DECIMAL(12,2) DEFAULT 0,
    discretionary_budget DECIMAL(12,2) DEFAULT 0,
    category_limits JSONB DEFAULT '{}',
    confidence_score DECIMAL(3,2) DEFAULT 0.8,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE budgets DISABLE ROW LEVEL SECURITY;

CREATE TABLE recommendations (
    recommendation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    recommendation_type VARCHAR(50) DEFAULT 'general',
    priority VARCHAR(10) DEFAULT 'medium',
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    reasoning TEXT DEFAULT '',
    action_items JSONB DEFAULT '[]',
    target_amount DECIMAL(12,2) DEFAULT NULL,
    target_date DATE DEFAULT NULL,
    confidence_score DECIMAL(3,2) DEFAULT 0.8,
    success_probability DECIMAL(3,2) DEFAULT NULL,
    agent_source VARCHAR(50) DEFAULT '',
    status VARCHAR(20) DEFAULT 'pending',
    user_feedback TEXT DEFAULT NULL,
    actual_outcome JSONB DEFAULT NULL,
    delivered_at TIMESTAMPTZ DEFAULT NULL,
    actioned_at TIMESTAMPTZ DEFAULT NULL,
    completed_at TIMESTAMPTZ DEFAULT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE recommendations DISABLE ROW LEVEL SECURITY;

CREATE TABLE savings_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    goal_type VARCHAR(50) DEFAULT 'savings',
    goal_name VARCHAR(255) NOT NULL,
    target_amount DECIMAL(12,2) DEFAULT 0,
    current_amount DECIMAL(12,2) DEFAULT 0,
    monthly_contribution DECIMAL(12,2) DEFAULT 0,
    priority VARCHAR(10) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'not_started',
    reasoning TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE savings_goals DISABLE ROW LEVEL SECURITY;

CREATE TABLE investment_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    investment_type VARCHAR(50) NOT NULL,
    provider VARCHAR(100) DEFAULT '',
    recommended_amount DECIMAL(12,2) DEFAULT 0,
    frequency VARCHAR(20) DEFAULT 'monthly',
    expected_return DECIMAL(5,2) DEFAULT 0,
    risk_level VARCHAR(20) DEFAULT 'low',
    reasoning TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE investment_recommendations DISABLE ROW LEVEL SECURITY;

CREATE TABLE bills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    bill_name VARCHAR(255) NOT NULL,
    bill_type VARCHAR(50) DEFAULT 'utility',
    amount DECIMAL(12,2) DEFAULT 0,
    due_date DATE NOT NULL,
    frequency VARCHAR(20) DEFAULT 'monthly',
    priority VARCHAR(20) DEFAULT 'medium',
    auto_pay_recommended BOOLEAN DEFAULT false,
    payment_method VARCHAR(50) DEFAULT 'upi',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE bills DISABLE ROW LEVEL SECURITY;

CREATE TABLE financial_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    goal_name VARCHAR(255) NOT NULL,
    goal_type VARCHAR(50) DEFAULT 'savings',
    description TEXT DEFAULT '',
    target_amount DECIMAL(12,2) DEFAULT 0,
    current_amount DECIMAL(12,2) DEFAULT 0,
    target_date DATE DEFAULT NULL,
    priority INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'not_started',
    monthly_target DECIMAL(12,2) DEFAULT 0,
    progress_percentage DECIMAL(5,2) DEFAULT 0,
    explanation JSONB DEFAULT '{}',
    milestones JSONB DEFAULT '[]',
    action_steps JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE financial_goals DISABLE ROW LEVEL SECURITY;

-- Step 6: Verify tables created
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
