# 🩺 SkinSense AI - Backend

FastAPI-based backend for SkinSense AI skin disease detection application.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here

# Download model files (see below)

# Start server
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## 📦 Tech Stack

- **FastAPI** - Web framework
- **PyTorch** - Deep learning
- **Transformers** - Model loading
- **Groq AI** - Medical advice generation
- **Pillow** - Image processing
- **Uvicorn** - ASGI server

## 🧠 AI Models

### 1. Local PyTorch Model (EfficientNetB3)
- **Purpose:** Skin disease classification
- **Classes:** 31 diseases
- **Size:** 347MB

### 2. Groq AI (Llama 3.1 8B Instant)
- **Purpose:** Medical advice generation
- **API:** Groq Cloud

## 📥 Download Model Files

Model files are NOT included in git (too large). Download them:

```python
from huggingface_hub import hf_hub_download
import shutil

files = ['config.json', 'preprocessor_config.json', 'pytorch_model.bin']
for f in files:
    print(f'Downloading {f}...')
    path = hf_hub_download(
        repo_id='Asad-Aziz/Skin-Disease-Detection',
        filename=f,
        repo_type='space'
    )
    shutil.copy(path, f'./{f}')
    print(f'Done: {f}')
```

Or download manually from:
https://huggingface.co/Asad-Aziz/Skin-Disease-Detection

Required files:
- `config.json` (3KB)
- `preprocessor_config.json` (3KB)
- `pytorch_model.bin` (347MB)

## ⚙️ Configuration

Create `.env` file:

```env
# Groq API (Required)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=800

# Model Configuration
MODEL_PATH=./
MAX_FILE_SIZE_MB=10

# Server Configuration
HOST=127.0.0.1
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Get Groq API Key

1. Visit https://console.groq.com
2. Sign up / Login
3. Go to API Keys
4. Create new key
5. Copy to `.env` file

## 📡 API Endpoints

### Health Check
```http
GET /health
```

### Predict Disease
```http
POST /predict
Content-Type: multipart/form-data

Body: file=<image_file>
```

**Response:**
```json
{
  "disease": "Acne",
  "confidence": 87.5,
  "advice": {
    "what_is_it": "...",
    "causes": [...],
    "who_gets_it": "...",
    "home_care": [...],
    "first_aid_medicines": [...],
    "avoid": [...],
    "see_doctor": "..."
  },
  "status": "success",
  "mode": "local_model"
}
```

### API Documentation
```http
GET /docs
```
Interactive Swagger UI documentation.

## 🎯 Features

- ✅ Local PyTorch model inference
- ✅ 31 disease classification
- ✅ AI-powered medical advice
- ✅ File validation (type, size)
- ✅ CORS enabled
- ✅ Error handling
- ✅ Fallback to demo mode

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Configuration (not in git)
├── .env.example         # Template
├── config.json          # Model config (download)
├── preprocessor_config.json  # Preprocessor (download)
└── pytorch_model.bin    # Model weights (download)
```

## 🔒 Security

- ✅ Environment variables for secrets
- ✅ CORS protection
- ✅ File type validation
- ✅ File size limits
- ✅ No data storage
- ✅ Input sanitization

## 🐛 Troubleshooting

### Model not loading?
```bash
# Check files exist
ls -la *.json *.bin

# Should see:
# config.json
# preprocessor_config.json
# pytorch_model.bin
```

### Groq API error?
```bash
# Check API key in .env
cat .env | grep GROQ_API_KEY

# Test API key at console.groq.com
```

### Port already in use?
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

## 🔗 Frontend Repository

This backend works with the SkinSense AI frontend:
https://github.com/alisaqibh1/skinsense-ai-frontend

## 📊 Performance

- **Response Time:** 3-5 seconds
- **Model Inference:** 2-3 seconds
- **AI Advice:** 1-2 seconds
- **Max File Size:** 10MB
- **Supported Formats:** JPG, PNG, JPEG

## ⚠️ Important Notes

- Model files must be downloaded separately
- Groq API key required
- Python 3.8+ required
- 10GB disk space for model

## 📄 License

Educational purposes only.

## 🤝 Contributing

Contributions welcome! Please open an issue first.

---

**Made with ❤️ using FastAPI + PyTorch**
