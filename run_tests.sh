#!/bin/bash

echo "🔍 Running unit tests..."

PYTHONPATH=core python3 -m unittest discover -s core -p "test_*.py"
PYTHONPATH=core python3 -m unittest discover -s features -p "test_*.py"
