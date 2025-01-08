import pandas as pd
import yt_dlp
from YouTubeSearchFunction import search_excluding


# Download Data
if __name__ == "__main__":
    queries = ["senna netflix serie"]
    exclude_keywords = ["teaser", "trailer"]
    max_results = 10

    # Create a directory to store results (optional: ensure the folder exists)
    import os
    os.makedirs("results", exist_ok=True)

    # Loop over each query and process results
    for query in queries:
        # Get filtered results for the current query
        filtered_results = search_excluding([query], exclude_keywords, max_results)

        # Convert the filtered list to a DataFrame
        df = pd.DataFrame(filtered_results.get(query, []))

        # Export to Excel (requires openpyxl or xlsxwriter)
        filename = f"results/{query.replace(' ', '_')}_filtered_results.xlsx"
        df.to_excel(filename, index=False)
        print(f"Saved {len(df)} filtered results to '{filename}'.")
