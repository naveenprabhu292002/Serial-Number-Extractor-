from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os
import re
import io
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── Configuration ─────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="Serial Number Extractor", version="1.0.0")


# ─── Main Endpoint ─────────────────────────────────────────────────────────────
@app.post("/extract-serial")
async def extract_serial(file: UploadFile = File(...)):
    """
    POST an image → returns the BW serial number found on the device label.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Look at this device label image. "
        "Find the Serial Number field (labeled 'Serial #:' or 'Serial Number'). "
        "The serial number always starts with 'BW'. "
        "Return ONLY the serial number string, nothing else. "
        "If you cannot find it, return 'NOT_FOUND'."
    )

    response = model.generate_content([prompt, image])
    raw_text = response.text.strip()

    match = re.search(r"BW\S+", raw_text, re.IGNORECASE)
    if match:
        serial_number = match.group(0).rstrip(".,;:")
        return JSONResponse(content={
            "serial_number": serial_number,
            "status": "success"
        })

    return JSONResponse(
        status_code=404,
        content={
            "serial_number": None,
            "status": "not_found",
            "raw_response": raw_text
        }
    )


# ─── Health Check ──────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}
