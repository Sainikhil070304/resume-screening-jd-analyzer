import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split

# 1. Sample data (replace with your real dataset)
data = {
    'Resume': [
        "Experienced lawyer with background in litigation and corporate law",
        "Developed machine learning models in Python and scikit-learn",
        "Certified network engineer with CCNA and firewall experience"
    ],
    'Category': ['Advocate', 'Data Scientist', 'Network Engineer']
}

df = pd.DataFrame(data)

# 2. Encode target labels
le = LabelEncoder()
y = le.fit_transform(df['Category'])

# 3. TF-IDF vectorization
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df['Resume'])

# 4. Train classifier
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = OneVsRestClassifier(SVC(probability=True))
clf.fit(X_train, y_train)

# 5. Save files
pickle.dump(clf, open("clf.pkl", "wb"))
pickle.dump(tfidf, open("tfidf.pkl", "wb"))
pickle.dump(le, open("encoder.pkl", "wb"))

print("✅ Model training complete. Files saved: clf.pkl, tfidf.pkl, encoder.pkl")
