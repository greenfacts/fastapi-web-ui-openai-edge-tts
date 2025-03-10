# Natural Language Text-to-Speech (TTS) with FastAPI UI

This project provides a user-friendly interface for converting text to natural-sounding speech using the [`edge-tts`](https://github.com/travisvn/openai-edge-tts) library. It leverages a FastAPI application with a simple web UI to streamline the process, making it easy to generate audio from text.

**Key Features:**

* **Natural-Sounding Speech:** Utilizes `edge-tts`, which leverages Microsoft Edge's online text-to-speech service, delivering high-quality, natural-sounding audio.
* **FastAPI Web UI:** Includes a simple and intuitive web interface for easy interaction.
    * Provides an input text box for entering the text to be converted.
    * Automatically cleans the input text before processing.
    * Submits the processed text to the local Edge-TTS API.
    * **Audio Playback:** Allows immediate playback of the generated audio within the browser.
    * **MP3 Download:** Provides the ability to download the generated audio as an MP3 file.
* **Local OpenAI-Compatible API:** Exposes an OpenAI-compatible API endpoint (`/v1/audio/speech`) for seamless integration with tools designed for the OpenAI TTS API.
* **Edge-TTS Integration:** Directly integrates with `edge-tts` for fast and efficient text-to-speech conversion.
* **Free and Local:** As `edge-tts` uses Microsoft Edge's online service, this project is completely free to use and runs locally.
* **Docker Compose:** Uses Docker Compose to easily deploy the edge-tts API and the fastAPI service.

**How it Works:**

1.  The user enters text into the input box on the FastAPI web UI.
2.  The application cleans the input text.
3.  The text is sent to the local Edge-TTS API (emulating the OpenAI TTS endpoint).
4.  `edge-tts` processes the text and generates audio.
5.  The generated audio is returned to the user, allowing for immediate playback within the browser.
6.  A download link is provided to save the audio as an MP3 file.
7.  Docker compose is used to launch the edge-tts API and fastAPI service.

**Benefits:**

* Provides a convenient and accessible way to generate high-quality speech from text.
* Eliminates the need for external cloud-based TTS services, offering a privacy-focused and cost-effective solution.
* The OpenAI-compatible API allows for easy integration with existing workflows.
* The fastAPI UI with playback and download features makes it very easy to use with no prior programming knowledge.  

To run:  
```sh
uvicorn main:app --reload
```

OR  

To build and run using Docker Compose:
```sh
docker-compose up --build
```

Open the URL: http://127.0.0.1:8000/  

![Screenshot](static/screenshot.png)
