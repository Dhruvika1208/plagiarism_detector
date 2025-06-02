from backend.plagiarism_checker import check_plagiarism

# Call the plagiarism check function
report_path, df = check_plagiarism("./data/submissions")

# Show results
print("Plagiarism Report Saved At:", report_path)
print(df)
