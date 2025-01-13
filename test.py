import os
import whisper

# Load the Whisper model
model = whisper.load_model("medium")

# Define the input folder and output folder
input_folder = "downloads/audio"
output_folder = "downloads/transcriptions"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate over all audio files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".mp3") or filename.endswith(".wav") or filename.endswith(".m4a"):
        audio_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

        print(f"Processing: {filename}")

        # Transcribe the audio file using Whisper's transcribe method
        result = model.transcribe(audio_path)

        # Save the transcription to a text file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"Saved transcription to: {output_path}")

print("Transcription completed for all files.")
