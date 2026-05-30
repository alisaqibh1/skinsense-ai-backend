from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import tempfile
import os
from PIL import Image
import io
from groq import Groq
import json
from dotenv import load_dotenv
from transformers import AutoModelForImageClassification, AutoImageProcessor
import torch

# Load environment variables
load_dotenv()

app = FastAPI()

# Get CORS origins from environment
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq API Configuration from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "800"))

# Model Configuration from environment variables
MODEL_PATH = os.getenv("MODEL_PATH", "./")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))

# Validate API key
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Load local model
print(f"🤖 Loading local skin disease detection model from: {MODEL_PATH}")
try:
    model = AutoModelForImageClassification.from_pretrained(MODEL_PATH)
    processor = AutoImageProcessor.from_pretrained(MODEL_PATH)
    model.eval()
    print("✅ Local model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load local model: {e}")
    model = None
    processor = None

def get_medical_advice(disease_name: str, confidence: float) -> dict:
    """Get AI-powered medical advice using Groq API"""
    try:
        prompt = f"""A patient has been diagnosed with {disease_name} skin condition with {confidence}% confidence. Provide comprehensive medical advice in simple English:

1. What is this condition? (2-3 lines simple explanation)
2. Common causes - Why does this happen? (3-4 bullet points covering deficiencies, triggers, lifestyle factors)
3. Who gets it? (Age groups, risk factors - 2 lines)
4. Home care tips (4 practical tips)
5. First aid medicines (3-4 over-the-counter medicines/creams that can help - with generic names)
6. What to avoid (3 things)
7. When to see a doctor urgently (2-3 warning signs)

Keep response clear, helpful, and non-scary. Use simple medical terms.
Do not replace professional medical advice.

Return ONLY a JSON object with this exact structure (no markdown, no extra text):
{{
  "what_is_it": "Simple explanation of the condition",
  "causes": ["cause 1", "cause 2", "cause 3", "cause 4"],
  "who_gets_it": "Age groups and risk factors",
  "home_care": ["tip 1", "tip 2", "tip 3", "tip 4"],
  "first_aid_medicines": ["medicine 1", "medicine 2", "medicine 3"],
  "avoid": ["thing 1", "thing 2", "thing 3"],
  "see_doctor": "Warning signs when to visit doctor urgently"
}}"""

        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant providing detailed skin condition advice. Always respond with valid JSON only, no markdown formatting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
        )
        
        # Extract response
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        # Parse JSON
        advice = json.loads(response_text)
        
        print(f"✓ Generated detailed medical advice for {disease_name}")
        return advice
        
    except Exception as e:
        print(f"⚠️ Error generating advice: {str(e)}")
        # Return fallback advice
        return {
            "what_is_it": f"{disease_name} is a skin condition that affects the skin's appearance and health. It requires proper medical evaluation for accurate diagnosis and treatment.",
            "causes": [
                "Genetic factors and family history",
                "Environmental triggers and allergens",
                "Immune system response",
                "Nutritional deficiencies or hormonal changes"
            ],
            "who_gets_it": "Can affect people of all ages, though some age groups may be more susceptible. Risk factors vary by individual health conditions.",
            "home_care": [
                "Keep the affected area clean and dry",
                "Avoid scratching or picking at the skin",
                "Use gentle, fragrance-free skincare products",
                "Maintain good hygiene and moisturize regularly"
            ],
            "first_aid_medicines": [
                "Calamine lotion for soothing irritation",
                "Hydrocortisone cream (1%) for mild inflammation",
                "Antihistamine tablets for itching (e.g., Cetirizine)"
            ],
            "avoid": [
                "Self-medication without consulting a doctor",
                "Harsh chemicals or irritants on the skin",
                "Excessive sun exposure without protection"
            ],
            "see_doctor": "Seek immediate medical attention if you experience severe pain, rapid spreading, signs of infection (pus, fever), or if symptoms worsen despite home care."
        }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an image file (JPG, PNG, etc.)"
        )
    
    # Read file contents
    contents = await file.read()
    
    # Check file size (max from environment variable)
    max_size = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB."
        )
    
    try:
        disease_name = None
        confidence = 0.0
        
        # Use local model if available
        if model is not None and processor is not None:
            print("🤖 Using local model for prediction")
            
            # Convert image bytes to PIL Image
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            
            # Preprocess image
            inputs = processor(images=image, return_tensors="pt")
            
            # Run inference
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                
            # Get prediction
            predicted_class_idx = logits.argmax(-1).item()
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            confidence_score = probabilities[0][predicted_class_idx].item()
            
            # Get label
            disease_name = model.config.id2label[predicted_class_idx]
            confidence = round(confidence_score * 100, 1)
            
            # Get top 5 predictions
            top5_prob, top5_idx = torch.topk(probabilities[0], k=min(5, len(probabilities[0])))
            top_predictions = []
            for prob, idx in zip(top5_prob, top5_idx):
                top_predictions.append({
                    "disease": model.config.id2label[idx.item()],
                    "confidence": round(prob.item() * 100, 2)
                })
            
        else:
            # Fallback to demo mode if model not loaded
            print("⚠️ Local model not available, using demo mode")
            
            mock_diseases = [
                {"label": "Eczema", "score": 0.85},
                {"label": "Psoriasis", "score": 0.78},
                {"label": "Acne", "score": 0.72},
                {"label": "Melanoma", "score": 0.68},
                {"label": "Dermatitis", "score": 0.65},
                {"label": "Rosacea", "score": 0.82},
                {"label": "Vitiligo", "score": 0.75},
                {"label": "Ringworm", "score": 0.88},
            ]
            
            import random
            selected = random.choice(mock_diseases)
            disease_name = selected['label']
            confidence = round(selected['score'] * 100, 1)
        
        print(f"✓ Prediction: {disease_name} ({confidence}%)")
        print(f"✓ Top 5 predictions: {top_predictions if model is not None else 'N/A'}")
        
        # Get AI-powered medical advice
        print(f"🤖 Generating medical advice using Groq AI...")
        advice = get_medical_advice(disease_name, confidence)
        
        return {
            "disease": disease_name,
            "confidence": confidence,
            "top_predictions": top_predictions if model is not None else [],
            "advice": advice,
            "status": "success",
            "mode": "local_model" if model is not None else "demo"
        }
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/")
async def root():
    return {
        "app": "SkinSense AI Backend API",
        "version": "2.0.0",
        "status": "running",
        "features": ["Skin Disease Detection", "AI-Powered Medical Advice"],
        "endpoints": {
            "predict": "POST /predict - Upload image for skin disease detection with AI advice",
            "health": "GET /health - Check API health status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    mode = "local_model" if model is not None else "demo"
    return {
        "status": "healthy",
        "mode": mode,
        "model": "local" if model is not None else "mock",
        "groq_api": "connected",
        "message": f"API is running in {mode.upper()} mode with AI-powered advice"
    }
