"""
Test Hugging Face Space Connection
"""
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

HF_SPACE_URL = os.getenv("HF_SPACE_URL")
USE_DEMO_MODE = os.getenv("USE_DEMO_MODE", "true").lower() == "true"

print("=" * 60)
print("CONFIGURATION CHECK")
print("=" * 60)
print(f"USE_DEMO_MODE: {USE_DEMO_MODE}")
print(f"HF_SPACE_URL: {HF_SPACE_URL}")
print("=" * 60)

if USE_DEMO_MODE:
    print("\n❌ DEMO MODE IS ENABLED")
    print("Real model will NOT be used")
    print("\nTo enable real model:")
    print("1. Edit backend/.env")
    print("2. Set USE_DEMO_MODE=false")
    print("3. Restart backend")
else:
    print("\n✅ REAL MODEL MODE IS ENABLED")
    print("Attempting to connect to Hugging Face Space...")
    print(f"Space URL: {HF_SPACE_URL}")
    
    try:
        from gradio_client import Client
        print("\n⏳ Connecting to Hugging Face Space...")
        print("(This may take 30-60 seconds if Space is sleeping)")
        
        client = Client(HF_SPACE_URL)
        
        print("\n✅ SUCCESS! Connected to Hugging Face Space")
        print("Real model is ready to use!")
        print("\nNow restart your backend:")
        print("python -m uvicorn main:app --reload --port 8000")
        
    except Exception as e:
        print(f"\n❌ FAILED to connect to Hugging Face Space")
        print(f"Error: {str(e)}")
        print("\n🔧 SOLUTIONS:")
        print("1. Open this URL in browser to wake up the Space:")
        print(f"   {HF_SPACE_URL}")
        print("2. Wait 30-60 seconds for it to load")
        print("3. Run this test script again")
        print("4. If still fails, the Space might be down")
        print("\nOR switch back to demo mode:")
        print("Edit backend/.env and set USE_DEMO_MODE=true")

print("\n" + "=" * 60)
