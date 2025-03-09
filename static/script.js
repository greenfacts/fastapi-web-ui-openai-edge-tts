async function generateSpeech() {
    const text = document.getElementById("text").value;
    const voice = document.getElementById("voice").value;

    const formData = new FormData();
    formData.append("text", text);
    formData.append("voice", voice);

    try {
        const response = await fetch("/generate_speech", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`); // Display error from FastAPI
            return;
        }

        const data = await response.json();
        const audioUrl = data.audio_url;

        const audioPlayer = document.getElementById("audio-player");
        const audio = document.getElementById("audio");
        const downloadLink = document.getElementById("download-link");

        audio.src = audioUrl;
        downloadLink.href = audioUrl; // Set the download link

        audioPlayer.style.display = "block"; // Show the audio player
        audio.load(); // Load the audio
        audio.play();

    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while generating speech.");
    }
}