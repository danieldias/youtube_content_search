import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.exceptions import ConvergenceWarning
import warnings
import numpy as np

# Suppress warnings related to KMeans convergence
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# Define the transcription folder
transcription_folder = "downloads/transcriptions"

# Read all text files in the folder
texts = []
file_names = []
for filename in os.listdir(transcription_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(transcription_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            texts.append(file.read())
        file_names.append(filename)

# Check if there are any files to process
if not texts:
    print("No text files found in the transcription folder.")
    exit()

# Vectorize the texts using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(texts)

# Extract feature names (keywords)
feature_names = vectorizer.get_feature_names_out()

# Compute the average TF-IDF score for each feature across all documents
average_tfidf = np.mean(tfidf_matrix.toarray(), axis=0)

# Combine feature names with their corresponding average TF-IDF scores
keywords_with_scores = list(zip(feature_names, average_tfidf))

# Sort keywords by their TF-IDF scores in descending order
sorted_keywords = sorted(keywords_with_scores, key=lambda x: x[1], reverse=True)

# Print the top 20 keywords
print("Top 20 Keywords:")
for keyword, score in sorted_keywords[:20]:
    print(f"{keyword}: {score:.4f}")

# Optional: Save the keywords and their scores to a file
output_keywords_path = os.path.join(transcription_folder, "keywords.txt")
with open(output_keywords_path, "w", encoding="utf-8") as output_file:
    for keyword, score in sorted_keywords:
        output_file.write(f"{keyword}: {score:.4f}\n")

print(f"Keywords saved to {output_keywords_path}.")
