import logging  # Import the logging module
import os
import re  # Import the regular expression module
from typing import Optional

import httpx
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

OPENAI_EDGE_TTS_URL = os.getenv(
    "OPENAI_EDGE_TTS_URL", "http://openai-edge-tts:5050"
)  # Use the Docker service name
API_KEY = "your_api_key_here"  # Default API Key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSRequest(BaseModel):
    model: str = "tts-1"
    input: str
    voice: str = "alloy"


def clean_text(text: str) -> str:
    """Removes special characters from the input text."""
    # Keep only alphanumeric characters, spaces, periods, commas, question marks, and exclamation points.
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s.,?!]", "", text)
    return cleaned_text.strip()  # Remove leading/trailing whitespace


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main UI."""
    return templates.TemplateResponse(
        "index.html", {"request": request, "api_key": API_KEY}
    )


@app.post("/set_api_key")
async def set_api_key(api_key: str = Form(...)):
    """Sets the API key."""
    global API_KEY
    API_KEY = api_key
    return {"message": "API Key set successfully"}


@app.post("/generate_speech")
async def generate_speech(
    request: Request, text: str = Form(...), voice: str = Form(...)
):
    """Generates speech using the OpenAI-edge-tts service."""

    # Clean the input text
    cleaned_text = clean_text(text)

    tts_request_data = TTSRequest(input=cleaned_text, voice=voice).dict()

    try:
        async with httpx.AsyncClient() as client:
            url = f"{OPENAI_EDGE_TTS_URL}/v1/audio/speech"
            logger.info(f"Sending request to URL: {url}")
            response = await client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}",
                },
                json=tts_request_data,
                timeout=60,  # Adjust timeout as needed
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            # Save the audio to a temporary file.  Important: Use a unique filename
            temp_file_path = f"static/speech_{hash(cleaned_text + voice)}.mp3"
            with open(temp_file_path, "wb") as f:
                f.write(response.content)

            # Return the path to the audio file so the frontend can display a link
            return {"audio_url": f"/static/{os.path.basename(temp_file_path)}"}

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e.response.status_code} - {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Request error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error connecting to TTS service: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
