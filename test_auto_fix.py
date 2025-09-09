#!/usr/bin/env python3
"""Test file for auto-fix functionality."""

import os

def test_function():
    # Missing import: json
    data = json.dumps({"test": "data"})
    
    # Missing import: datetime
    now = datetime.now()
    
    # Missing import: requests (would need to be added to requirements)
    # response = requests.get("https://api.example.com")
    
    return data, now

if __name__ == "__main__":
    test_function()