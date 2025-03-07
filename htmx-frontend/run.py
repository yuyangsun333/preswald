#!/usr/bin/env python3
"""
Simple script to run the FastHTML app and connect it to Preswald.
"""

import os
import sys

import uvicorn


# Ensure the current directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting FastHTML app with Preswald integration...")
    print("Access the app at http://localhost:8000")
    print("Connecting to Preswald backend at ws://localhost:8501/ws")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
