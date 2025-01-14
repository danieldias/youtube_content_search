import pandas as pd
import re

# File paths
comments_file = "downloads/comments/all_comments.xlsx"  # Excel file with comments
themes_file = "downloads/comments/themes_keywords.xlsx"  # Excel file with themes and keywords

# Load the comments
comments_df = pd.read_excel(comments_file)

# Load the themes and keywords
themes_df = pd.read_excel(themes_file)

# Create the dictionary dynamically
themes = themes_df.groupby('Theme')['Keyword'].apply(list).to_dict()

# Add a column for each theme in the comments DataFrame
for theme, keywords in themes.items():
    # Combine keywords into a regex pattern
    pattern = '|'.join(re.escape(keyword) for keyword in keywords)
    # Check if any keyword matches in the comments
    comments_df[theme] = comments_df['COMMENT CONTENT'].str.contains(pattern, case=False, na=False)

# Calculate percentages for each theme
theme_percentages = {
    theme: (comments_df[theme].sum() / len(comments_df)) * 100 for theme in themes
}

# Print percentages
for theme, percentage in theme_percentages.items():
    print(f"The theme '{theme}' is mentioned in {percentage:.2f}% of the comments.")

# Save results to a new Excel file
output_file = "comments_with_themes.xlsx"
comments_df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}.")
