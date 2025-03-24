# plagiarism_detector/app.py
import streamlit as st
from backend.auth import login, logout
from backend.plagiarism_checker import check_plagiarism
import os
import pandas as pd

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None

# Show login page if not authenticated
if not st.session_state["authenticated"]:
    login()
else:
    if st.session_state["role"] == "Student":
        st.title("Welcome, Student!")
        uploaded_file = st.file_uploader("Upload your assignment", type=["txt"])
        if uploaded_file is not None:
            with open(f"./data/submissions/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded successfully!")

        st.sidebar.button("Logout", on_click=logout)

    elif st.session_state["role"] == "Teacher":
        st.title("Welcome, Teacher!")
        if st.button("Check Plagiarism"):
            report_path = check_plagiarism("./data/submissions")
            st.success(f"Plagiarism report generated at: {report_path}")
        
        if os.path.exists("./data/reports/plagiarism_report.csv"):
            df = pd.read_csv("./data/reports/plagiarism_report.csv")
            st.write("### Plagiarism Report")
            st.dataframe(df)
        
        st.sidebar.button("Logout", on_click=logout)
