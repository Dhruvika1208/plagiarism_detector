# plagiarism_detector/backend/plagiarism_checker.py
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

UPLOAD_FOLDER = "./data/submissions"
REPORT_FOLDER = "./data/reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

def preprocess_text(text):
    """Clean text for similarity checking."""
    return ''.join(e for e in text.lower() if e.isalnum() or e.isspace())

def calculate_similarity(doc1, doc2):
    """Calculate cosine similarity."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

def check_plagiarism(submissions_folder):
    """Check plagiarism between submissions."""
    submissions = os.listdir(submissions_folder)
    results = []
    
    for i, file1 in enumerate(submissions):
        with open(os.path.join(submissions_folder, file1), "r") as f1:
            text1 = preprocess_text(f1.read())
        
        for j, file2 in enumerate(submissions):
            if i >= j:
                continue
            
            with open(os.path.join(submissions_folder, file2), "r") as f2:
                text2 = preprocess_text(f2.read())
            
            similarity = calculate_similarity(text1, text2)
            results.append({
                "File 1": file1,
                "File 2": file2,
                "Similarity": round(similarity * 100, 2),
                "Plagiarized": "Yes" if similarity > 0.8 else "No",
            })
    
    # Save results to CSV
    report_path = os.path.join(REPORT_FOLDER, "plagiarism_report.csv")
    pd.DataFrame(results).to_csv(report_path, index=False)
    return report_path
