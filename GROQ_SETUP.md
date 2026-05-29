# Groq AI Integration Setup Guide

## What's New:

SkinSense AI now includes **AI-powered medical advice** using Groq's LLaMA 3 model!

## Features Added:

✅ **Intelligent Medical Advice** - AI generates personalized advice for each skin condition
✅ **What is it?** - Simple explanation of the condition
✅ **Home Care Tips** - 3 practical tips for home treatment
✅ **What to Avoid** - 2 things to avoid
✅ **When to See Doctor** - Clear guidance on when to seek medical help

## Setup Instructions:

### Step 1: Install Groq Package

```bash
cd backend
pip install groq
```

### Step 2: Verify Installation

```bash
pip list | grep groq
```

Should show: `groq  x.x.x`

### Step 3: Restart Backend

```bash
python -m uvicorn main:app --reload --port 8000
```

### Step 4: Test the API

Upload an image from the frontend and check the response includes `advice` field.

## API Response Format:

```json
{
  "disease": "Eczema",
  "confidence": 85.0,
  "advice": {
    "what_is_it": "Simple explanation...",
    "home_care": ["tip 1", "tip 2", "tip 3"],
    "avoid": ["thing 1", "thing 2"],
    "see_doctor": "When to visit..."
  },
  "status": "success"
}
```

## Groq API Details:

- **API Key:** Already configured in main.py
- **Model:** llama3-8b-8192 (Fast and accurate)
- **Rate Limits:** Free tier - 30 requests/minute
- **Response Time:** ~1-2 seconds

## Fallback Mechanism:

If Groq API fails, the backend automatically returns generic medical advice to ensure the app keeps working.

## Frontend Display:

The ResultCard component now shows:

1. **What is it?** - Light green card (#DCFCE7)
2. **Home Care Tips** - White card with checkmark icons (#0891B2)
3. **What to Avoid** - White card with X icons (#DC2626)
4. **See a Doctor If** - Warning card with red border (#DC2626)

All with smooth framer-motion animations!

## Troubleshooting:

### Error: "groq module not found"
```bash
pip install groq
```

### Error: "API key invalid"
- Check GROQ_API_KEY in main.py
- Verify the key is correct

### Error: "Rate limit exceeded"
- Wait 1 minute
- Groq free tier: 30 requests/minute

### Advice not showing in frontend
- Check browser console for errors
- Verify backend response includes `advice` field
- Check ResultCard.jsx is updated

## Testing:

1. Start backend: `python -m uvicorn main:app --reload --port 8000`
2. Start frontend: `npm run dev`
3. Upload any skin image
4. Check result card shows AI-powered advice

## Production Notes:

- Groq API is free and fast
- No sleeping issues like Hugging Face Spaces
- Reliable for production use
- Consider upgrading to paid tier for higher limits

Enjoy the AI-powered medical advice feature! 🚀🤖
