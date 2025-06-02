# plagiarism_detector/backend/plagiarism_checker.py

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Ensure stopwords are available
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

# Folder paths
UPLOAD_FOLDER = "./data/submissions"
REPORT_FOLDER = "./data/reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Preprocess text: lowercase, remove punctuation, remove stopwords, stem
def preprocess_text(text):
    stemmer = PorterStemmer()
    cleaned = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text.lower())
    words = cleaned.split()
    filtered = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(filtered)

# Calculate cosine similarity between two texts
def calculate_similarity(doc1, doc2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

# Main function to check plagiarism
def check_plagiarism(submissions_folder):
    submissions = [f for f in os.listdir(submissions_folder) if f.endswith(".txt")]
    results = []

    for i, file1 in enumerate(submissions):
        with open(os.path.join(submissions_folder, file1), "r", encoding='utf-8') as f1:
            text1 = preprocess_text(f1.read())

        for j in range(i + 1, len(submissions)):
            file2 = submissions[j]
            with open(os.path.join(submissions_folder, file2), "r", encoding='utf-8') as f2:
                text2 = preprocess_text(f2.read())

            similarity = calculate_similarity(text1, text2)
            if similarity > 0.3:  # Filter out very low similarity
                results.append({
                    "File 1": file1,
                    "File 2": file2,
                    "Similarity (%)": round(similarity * 100, 2),
                    "Plagiarized": "Yes" if similarity > 80 else "No",
                })

    report_path = os.path.join(REPORT_FOLDER, "plagiarism_report.csv")
    df = pd.DataFrame(results)
    df.to_csv(report_path, index=False)
    return report_path, df
