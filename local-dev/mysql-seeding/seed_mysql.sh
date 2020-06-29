#!/bin/sh

echo "Preparing users table..."
python seed_users.py
echo "Preparing transactions table..."
python seed_transactions.py