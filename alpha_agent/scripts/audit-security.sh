#!/bin/bash

echo "Running backend security audit..."
pip install bandit
bandit -r backend/

echo "Running frontend security audit..."
npm audit --prefix frontend/
