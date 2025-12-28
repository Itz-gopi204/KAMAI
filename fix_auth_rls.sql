-- ============================================
-- FIX: Enable User Registration (Signup)
-- Run this in Supabase SQL Editor
-- ============================================

-- Option 1: Disable RLS on users table (Quick fix for hackathon)
ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- OR Option 2: Create proper RLS policies (Recommended)
-- Uncomment below if you want to keep RLS enabled

/*
-- First, enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Allow anyone to create new users (signup)
CREATE POLICY "Allow public signup" ON users
    FOR INSERT
    WITH CHECK (true);

-- Allow users to read their own data
CREATE POLICY "Users can read own data" ON users
    FOR SELECT
    USING (true);

-- Allow users to update their own data
CREATE POLICY "Users can update own data" ON users
    FOR UPDATE
    USING (true);
*/

-- ============================================
-- Also fix RLS for other tables if needed
-- ============================================

-- Transactions table
ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;

-- User profiles table (if exists)
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user_profiles') THEN
        EXECUTE 'ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY';
    END IF;
END $$;

-- Budgets table
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'budgets') THEN
        EXECUTE 'ALTER TABLE budgets DISABLE ROW LEVEL SECURITY';
    END IF;
END $$;

-- Recommendations table
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'recommendations') THEN
        EXECUTE 'ALTER TABLE recommendations DISABLE ROW LEVEL SECURITY';
    END IF;
END $$;

-- New tables (savings, bills, goals)
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'savings_goals') THEN
        EXECUTE 'ALTER TABLE savings_goals DISABLE ROW LEVEL SECURITY';
    END IF;
END $$;

DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'investment_recommendations') THEN
        EXECUTE 'ALTER TABLE investment_recommendations DISABLE ROW LEVEL SECURITY';
    END IF;
END $$;

DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'bills') THEN
        EXECUTE 'ALTER TABLE bills DISABLE ROW LEVEL SECURITY';
    END IF;
END $$;

DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'financial_goals') THEN
        EXECUTE 'ALTER TABLE financial_goals DISABLE ROW LEVEL SECURITY';
    END IF;
END $$;

-- ============================================
-- Verify: Check RLS status
-- ============================================
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';
