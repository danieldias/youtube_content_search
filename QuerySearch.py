import pandas as pd
import yt_dlp
from YouTubeSearchFunction import search_excluding


#Download Data
if __name__ == "__main__":
    query = "senna netflix series"
    exclude_keywords = ["teaser", "trailer"]
    max_results = 50

    # Get filtered results
    filtered_results = search_excluding(query, exclude_keywords, max_results)

    # Convert the filtered list to a DataFrame
    df = pd.DataFrame(filtered_results)

    # Export to Excel (requires openpyxl or xlsxwriter)
    df.to_excel(f"results/{query}_filtered_results.xlsx", index=False)
    print(f"Saved {len(df)} filtered results to 'yt_dlp_filtered_results.xlsx'.")