# Backend Troubleshooting Guide

## Issue: Cannot connect to Hugging Face Space

### Problem:
```
Could not get Gradio config from: https://itsluckysharma01-skin-diseases-detection-of-30-classes.hf.space
```

### Possible Causes:

1. **Hugging Face Space is sleeping**
   - Free Hugging Face Spaces go to sleep after inactivity
   - Takes 30-60 seconds to wake up

2. **Space is down or unavailable**
   - The space owner may have taken it offline
   - Hugging Face may be experiencing issues

3. **Network/Firewall issues**
   - Your network may be blocking Hugging Face
   - Firewall or antivirus blocking the connection

### Solutions:

#### Solution 1: Wake up the Space manually

1. Open browser and visit:
   ```
   https://huggingface.co/spaces/itsluckysharma01/Skin_Diseases_Detection_of_30_Classes
   ```

2. Wait for the space to load (30-60 seconds)

3. Once it's running, restart your backend:
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

#### Solution 2: Use the /wake endpoint

1. Start the backend
2. Open browser: `http://localhost:8000/wake`
3. Wait for response
4. Try uploading image again

#### Solution 3: Check Space Status

Visit the space URL in browser:
```
https://huggingface.co/spaces/itsluckysharma01/Skin_Diseases_Detection_of_30_Classes
```

If you see:
- ✅ "Running" - Space is active, try again
- ⏸️ "Sleeping" - Click to wake it up
- ❌ "Error" - Space may be down

#### Solution 4: Alternative - Use Different Model

If the space is permanently down, you can:

1. Find another skin disease detection model on Hugging Face
2. Update `SPACE_URLS` in `main.py`
3. Or deploy your own model

### Testing:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test wake endpoint
curl http://localhost:8000/wake

# Test root endpoint
curl http://localhost:8000/
```

### Common Errors:

**Error:** `503 Service Unavailable`
- **Cause:** Cannot connect to Hugging Face
- **Fix:** Wake up the space manually

**Error:** `500 Internal Server Error`
- **Cause:** Prediction failed
- **Fix:** Check image format and size

**Error:** `400 Bad Request`
- **Cause:** Invalid file type or size
- **Fix:** Upload valid image (JPG/PNG, <10MB)

### Need Help?

1. Check Hugging Face status: https://status.huggingface.co/
2. Visit the space page to see if it's running
3. Try a different image
4. Restart backend server
