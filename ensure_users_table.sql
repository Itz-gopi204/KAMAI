-- ============================================
-- ENSURE: Users table exists with correct schema
-- Run this in Supabase SQL Editor FIRST
-- ============================================

-- Create users table if not exists
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(10) UNIQUE NOT NULL,
    email VARCHAR(255),
    full_name VARCHAR(255) NOT NULL,
    occupation VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    pin_code VARCHAR(10),
    date_of_birth DATE,
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT true,
    kyc_verified BOOLEAN DEFAULT false,
    onboarding_completed BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Disable RLS to allow signups
ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- Create index for faster phone lookups
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone_number);

-- ============================================
-- Create transactions table if not exists
-- ============================================
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    transaction_date DATE NOT NULL,
    transaction_time TIME,
    amount DECIMAL(12,2) NOT NULL,
    transaction_type VARCHAR(10) CHECK (transaction_type IN ('income', 'expense')),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    description TEXT,
    payment_method VARCHAR(50),
    merchant_name VARCHAR(100),
    location VARCHAR(100),
    source VARCHAR(50),
    account_id UUID,
    input_method VARCHAR(20) DEFAULT 'manual',
    verified BOOLEAN DEFAULT true,
    confidence_score DECIMAL(3,2) DEFAULT 1.0,
    is_recurring BOOLEAN DEFAULT false,
    recurring_frequency VARCHAR(20),
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;

-- ============================================
-- Verify tables created
-- ============================================
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;
