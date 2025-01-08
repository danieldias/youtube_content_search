import yt_dlp
import pandas as pd


def search_excluding(queries, exclude_keywords, max_results=50):
    """
    Search YouTube for `queries` using yt-dlp, then filter out any results
    whose titles contain one of the `exclude_keywords`.
    Returns a list of dictionaries with metadata for each matching video.
    """

    results = {} #Initializes results dictionary

    # 1. Set up yt-dlp options
    ydl_opts = {
        'quiet': True,  # Suppress detailed logs
        'ignoreerrors': True  # Skip errors if any video fails to load
    }

    # 2. Construct the special search queries string: "ytsearchN:query"
    for query in queries:
        search_string = f"ytsearch{max_results}:{query}"

        # 3. Extract info (metadata only, no downloading)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(search_string, download=False)

        # `info_dict` is a dict. Its 'entries' key holds the list of videos
        all_entries = info_dict.get('entries', [])
        if not all_entries:
            return []

        # 4. Filter out videos whose title contains any exclude_keywords
        filtered = []
        for single_video in all_entries:
            if single_video is None:
                # Sometimes an entry can be None if yt-dlp couldn’t parse it
                continue

            title = single_video.get("title", "").lower()
            if not any(kw.lower() in title for kw in exclude_keywords):
                filtered.append(single_video)

            # Store the filtered list in the results dictionary
            results[query] = filtered

    return results
