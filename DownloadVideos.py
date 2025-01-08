import os
import pandas as pd
import yt_dlp

def download_audio_from_excel(results_folder="results", downloads_folder="downloads/audio"):
    """
    Downloads audio from videos listed in all Excel files within the `results` folder.
    Saves the audio files in the specified `downloads/audio` folder.
    Assumes each Excel file contains a column named 'webpage_url' with video URLs.
    """
    # Ensure the results folder exists
    if not os.path.exists(results_folder):
        print(f"Folder '{results_folder}' does not exist.")
        return

    # Ensure the downloads/audio folder exists
    os.makedirs(downloads_folder, exist_ok=True)

    # List all Excel files in the results folder
    excel_files = [f for f in os.listdir(results_folder) if f.endswith(".xlsx")]

    if not excel_files:
        print(f"No Excel files found in the '{results_folder}' folder.")
        return

    # yt-dlp options for audio-only downloads
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best available audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',  # Save the audio as MP3
            'preferredquality': '192',  # Set audio quality to 192kbps
        }],
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),  # Save audio in downloads/audio
        'quiet': False,  # Show download progress
        'ignoreerrors': True  # Continue on download errors
    }

    # Process each Excel file
    for excel_file in excel_files:
        file_path = os.path.join(results_folder, excel_file)
        print(f"\nProcessing file: {file_path}")

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Ensure 'webpage_url' column exists
            if 'webpage_url' not in df.columns:
                print(f"Skipping '{file_path}' as it does not contain a 'webpage_url' column.")
                continue

            # Extract URLs
            video_urls = df['webpage_url'].dropna().tolist()
            if not video_urls:
                print(f"No video URLs found in '{file_path}'.")
                continue

            print(f"Found {len(video_urls)} videos in '{file_path}'. Starting downloads...")

            # Download each video as audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for url in video_urls:
                    print(f"Downloading audio from: {url}")
                    try:
                        ydl.download([url])
                    except Exception as e:
                        print(f"Failed to download {url}: {e}")

        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")

    print("\nAll files processed! Audio saved in the 'downloads/audio' folder.")

if __name__ == "__main__":
    download_audio_from_excel(results_folder="results", downloads_folder="downloads/audio")
