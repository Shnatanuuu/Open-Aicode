import os
from dotenv import load_dotenv

print("=== DEBUG INFO ===")
print("Current directory:", os.getcwd())
print("Files in directory:", [f for f in os.listdir('.') if not f.startswith('.')])
print("Hidden files (.env):", [f for f in os.listdir('.') if f.startswith('.env')])

# Try loading .env
result = load_dotenv()
print("load_dotenv result:", result)

# Check the API key
api_key = os.getenv('OPENAI_API_KEY')
print("API key exists:", api_key is not None)

if api_key:
    print("First 10 chars:", api_key[:10])
    print("Length:", len(api_key))
else:
    print("API key is None - check .env file content")

# Try to read .env file directly
try:
    with open('.env', 'r') as f:
        content = f.read()
        print("Raw .env content:")
        print(repr(content))  # This shows exact content including hidden characters
except FileNotFoundError:
    print(".env file not found in current directory")
except Exception as e:
    print("Error reading .env:", e)