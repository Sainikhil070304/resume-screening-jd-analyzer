📊 Resume Screening & JD Analyzer

AI-Powered ATS Platform for Intelligent Resume Evaluation

📌 Overview

Resume Screening & JD Analyzer is an AI-based Applicant Tracking System that automates resume evaluation and job description matching.
The platform extracts text from resumes (PDF/DOCX/TXT), predicts the candidate’s job category using machine learning, compares the resume with a job description using semantic similarity, and generates a professional ATS-style report with skill gap analysis and improvement recommendations.

This tool helps:

Recruiters to shortlist candidates faster

Students to improve resumes for ATS

Organizations to standardize hiring evaluation

🚀 Features

🧠 Resume Category Prediction using TF-IDF + SVM

🎯 Semantic JD Matching with Cosine Similarity

📈 Core & Soft Skill Scoring

🔍 Matched & Missing Keyword Analysis

💡 One-Line Actionable Recommendations

📄 Professional PDF Report Generation

📂 Support for PDF / DOCX / TXT formats

🎨 Interactive Streamlit Dashboard UI

🛠 Tech Stack

Python

NLP (NLTK)

scikit-learn (TF-IDF, SVM)

Streamlit

PyPDF2 & python-docx

ReportLab (PDF generation)

Cosine Similarity

🧩 Workflow

Upload Resume

System extracts text

ML model predicts job role

Paste Job Description

System computes:

JD Match Score

Core Skill Score

Soft Skill Score

Matched / Missing skills

Generates downloadable ATS report

## 📁 Folder Structure

```
Resume-Screening-JD-Analyzer/
│
├── app.py                     # Main Streamlit application
├── clf.pkl                    # Trained SVM model
├── tfidf.pkl                  # TF-IDF vectorizer
├── encoder.pkl                # Label encoder
├── requirements.txt
├── README.md
│
├── dataset/
│   └── UpdatedResumeDataSet.csv
│
└── screenshots/
    ├── dashboard.png
    ├── match.png
    └── report.png
```


🔧 Setup Instructions
1. Clone Repository
git clone https://github.com/<your-username>/Resume-Screening-JD-Analyzer.git
cd Resume-Screening-JD-Analyzer

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run Application
streamlit run app.py

🧪 How to Use

Upload a resume (PDF/DOCX/TXT)

View predicted job category

Paste job description

Click compare

View:

Match percentage

Skill gaps

Recommendations

Download ATS report

📄 Output Report Contains

Executive Summary

Predicted Role

JD Match Score

Core & Soft Skills

Matched Skills

Missing Skills

Improvement Plan

Recruiter Note

💡 Use Cases

🔹 Recruiter shortlisting

🔹 Student resume improvement

🔹 Pre-placement preparation

🔹 HR automation

🔹 Internship filtering

🎯 Learning Outcomes

Text preprocessing with NLP

Feature extraction using TF-IDF

Classification using SVM

Semantic similarity

End-to-end ML deployment

UI development with Streamlit

PDF report automation

🚧 Future Enhancements

BERT embeddings for better semantic match

Multi-JD ranking system

Recruiter dashboard

Grammar & ATS format checker

Experience relevance scoring

Email automation

🤝 Contributing

Contributions are welcome!
Open an issue or submit a pull request for improvements.
