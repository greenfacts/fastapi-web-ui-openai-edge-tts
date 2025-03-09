from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
import os
from typing import Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

OPENAI_EDGE_TTS_URL = os.getenv("OPENAI_EDGE_TTS_URL", "http://localhost:5050") # Default URL, allow env override
API_KEY = ""  # Initially empty, to be set via the UI

# Data model for the request body
class TTSRequest(BaseModel):
    model: str = "tts-1"
    input: str
    voice: str = "alloy"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main UI."""
    return templates.TemplateResponse("index.html", {"request": request, "api_key": API_KEY})


@app.post("/set_api_key")
async def set_api_key(api_key: str = Form(...)):
    """Sets the API key."""
    global API_KEY
    API_KEY = api_key
    return {"message": "API Key set successfully"}



@app.post("/generate_speech")
async def generate_speech(request: Request, text: str = Form(...), voice: str = Form(...)):
    """Generates speech using the OpenAI-edge-tts service."""
    if not API_KEY:
        raise HTTPException(status_code=400, detail="API Key is not set.  Please set it on the main page.")

    tts_request_data = TTSRequest(input=text, voice=voice).dict()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OPENAI_EDGE_TTS_URL}/v1/audio/speech",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
                json=tts_request_data,
                timeout=60  # Adjust timeout as needed
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            # Save the audio to a temporary file.  Important: Use a unique filename
            temp_file_path = f"static/speech_{hash(text + voice)}.mp3"
            with open(temp_file_path, "wb") as f:
                f.write(response.content)

            # Return the path to the audio file so the frontend can display a link
            return {"audio_url": f"/static/{os.path.basename(temp_file_path)}"}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to TTS service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")