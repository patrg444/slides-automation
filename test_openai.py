#!/usr/bin/env python3
"""Test OpenAI integration"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Test OpenAI initialization
try:
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    
    # Initialize without any extra parameters
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client initialized successfully")
    
    # Test with a simple completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, OpenAI is working!' in JSON format with key 'message'"}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    print(f"✅ Test response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # Try to understand what's happening
    import traceback
    traceback.print_exc()