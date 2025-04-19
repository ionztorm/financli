#!/bin/bash

echo "🔍 Running unit tests..."

python3 -m unittest discover -s . -p "test_*.py"
