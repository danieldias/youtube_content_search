import os
import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader
import json

def extract_comments_to_json(results_folder="results", comments_folder="downloads/comments"):
    """
    Extracts comments from videos listed in all Excel files within the `results` folder.
    Saves the comments for each video in separate JSON files in the `downloads/comments` folder.
    """
    # Ensure the results folder exists
    if not os.path.exists(results_folder):
        print(f"Folder '{results_folder}' does not exist.")
        return

    # Ensure the comments folder exists
    os.makedirs(comments_folder, exist_ok=True)

    downloader = YoutubeCommentDownloader()

    # List all Excel files in the results folder
    excel_files = [f for f in os.listdir(results_folder) if f.endswith(".xlsx")]

    if not excel_files:
        print(f"No Excel files found in the '{results_folder}' folder.")
        return

    all_comments = []  # To store all comments for the final Excel

    for excel_file in excel_files:
        file_path = os.path.join(results_folder, excel_file)
        print(f"\nProcessing file: {file_path}")

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Ensure required columns exist
            if 'webpage_url' not in df.columns or 'title' not in df.columns:
                print(f"Skipping '{file_path}' as it does not contain required columns.")
                continue

            # Extract URLs and titles
            videos = df[['webpage_url', 'title']].dropna()

            if videos.empty:
                print(f"No video data found in '{file_path}'.")
                continue

            print(f"Found {len(videos)} videos in '{file_path}'. Starting comment extraction...")

            # Extract comments for each video
            for _, video in videos.iterrows():
                url = video['webpage_url']
                title = video['title']
                try:
                    video_id = url.split("v=")[-1]
                    json_file = os.path.join(comments_folder, f"{video_id}_comments.json")

                    print(f"Extracting comments for: {url}")
                    generator = downloader.get_comments_from_url(url)

                    # Save comments to JSON and store in all_comments
                    video_comments = []
                    for comment in generator:
                        # Construct the comment link
                        cid = comment.get("cid", "")
                        comment_link = f"https://www.youtube.com/watch?v={video_id}&lc={cid}" if cid else ""

                        video_comment = {
                            "COMMENT CONTENT": comment["text"],
                            "COMMENT DATE": comment.get("time", ""),
                            "COMMENT LINK": comment_link,
                            "VIDEO TITLE": title,
                            "VIDEO LINK": url
                        }
                        video_comments.append(video_comment)
                        all_comments.append(video_comment)

                    # Write to JSON file
                    with open(json_file, "w", encoding="utf-8") as f:
                        json.dump(video_comments, f, ensure_ascii=False, indent=4)

                    print(f"Comments saved to: {json_file}")

                except Exception as e:
                    print(f"Failed to extract comments for {url}: {e}")

        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")

    # Convert all comments to Excel
    if all_comments:
        consolidate_comments_to_excel(all_comments, comments_folder)

    print("\nAll files processed! Comments saved in JSON and consolidated into Excel.")

def consolidate_comments_to_excel(all_comments, comments_folder):
    """
    Converts a list of all comments to a consolidated Excel file.
    """
    try:
        comments_df = pd.DataFrame(all_comments)
        excel_file = os.path.join(comments_folder, "all_comments.xlsx")
        comments_df.to_excel(excel_file, index=False)
        print(f"All comments consolidated into: {excel_file}")
    except Exception as e:
        print(f"Failed to create consolidated Excel: {e}")

if __name__ == "__main__":
    extract_comments_to_json(results_folder="results", comments_folder="downloads/comments")
