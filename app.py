import nltk
nltk.data.path.append("C:/Users/SAI NIKHIL/AppData/Roaming/nltk_data")

import streamlit as st
import PyPDF2, docx, os, pickle, re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

nltk.download('punkt')
nltk.download('stopwords')

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Resume Screening & JD Analyzer", layout="wide")

st.markdown("""
<style>
.title{font-size:40px;font-weight:800;color:#4F8BF9}
.card{background:#0E1117;padding:18px;border-radius:12px;margin:6px}
.big{font-size:26px;font-weight:bold;color:#6CE5E8}
.tag{background:#1A2333;padding:6px 10px;border-radius:8px;margin:3px;display:inline-block}
</style>
""", unsafe_allow_html=True)

# ================= CONSTANTS =================
SYNONYMS = {
"nlp":"natural language processing",
"tfidf":"tf idf",
"ml":"machine learning",
"ai":"artificial intelligence",
"api":"rest api"
}

CORE_SKILLS = ["python","sql","machine learning","nlp","flask","api",
"data structures","algorithms","streamlit","scikit"]

SOFT_SKILLS = ["communication","team","leadership",
"problem solving","adaptability","collaboration"]

JUNK = ["tej","20233","4star","photo","push","cache","pytz20241"]

# ================= HELPERS =================

def expand(t):
    t=t.lower()
    for k,v in SYNONYMS.items():
        t=t.replace(k,v)
    return t

def filter_tokens(tokens):
    return {t for t in tokens if not any(c.isdigit() for c in t) and t not in JUNK}

def pdf_text(f):
    r=PyPDF2.PdfReader(f)
    return " ".join([p.extract_text() for p in r.pages if p.extract_text()])

def doc_text(f):
    d=docx.Document(f)
    return "\n".join([p.text for p in d.paragraphs])

def tokens(t):
    sw=set(stopwords.words('english'))
    t=re.sub(r'[^\w\s]','',t.lower())
    return set([w for w in t.split() if w not in sw and len(w)>2])

def semantic(a,b):
    v=tfidf.transform([a,b])
    return round(cosine_similarity(v[0],v[1])[0][0]*100,2)

def skill_score(text):
    s=tokens(text)
    c=sum(1 for i in CORE_SKILLS if i in s)
    return round(c/len(CORE_SKILLS)*100,2)

def soft_score(text):
    s=tokens(text)
    c=sum(1 for i in SOFT_SKILLS if i in s)
    return round(c/len(SOFT_SKILLS)*100,2)

def smart_recommend(score, core, soft, miss):
    rec=[]
    if score < 60:
        rec.append("Align resume keywords exactly with job description terms.")
    if core < 50:
        rec.append("Add dedicated Technical Skills section with Python, SQL, API, ML.")
    if soft < 40:
        rec.append("Include teamwork and communication impact statements.")
    if "api" in miss:
        rec.append("Mention REST API or deployment exposure clearly.")
    if "nlp" in miss:
        rec.append("Add NLP/TF-IDF keywords from your resume project.")
    if "sql" in miss:
        rec.append("Show SQL queries or database experience.")
    return rec[:5]

# ================= PDF REPORT =================

def make_pdf(cat,score,core,soft,match,miss):
    name="Enterprise_Resume_Report.pdf"
    c=canvas.Canvas(name,pagesize=A4)

    c.setFont("Helvetica-Bold",18)
    c.drawString(50,800,"ATS RESUME ASSESSMENT REPORT")

    c.setFont("Helvetica",11)
    c.drawString(50,775,f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    c.line(50,768,550,768)

    c.setFont("Helvetica-Bold",13)
    c.drawString(50,740,"1. Executive Summary")

    c.setFont("Helvetica",11)
    c.drawString(50,720,f"Predicted Role : {cat}")
    c.drawString(50,705,f"JD Match       : {score}%")
    c.drawString(50,690,f"Core Skills    : {core}%")
    c.drawString(50,675,f"Soft Skills    : {soft}%")

    c.setFont("Helvetica-Bold",13)
    c.drawString(50,650,"2. Skills Alignment")

    y=630
    c.setFont("Helvetica",11)
    c.drawString(50,y,"Matched Skills:")
    for w in list(match)[:12]:
        y-=16; c.drawString(70,y,"• "+w)

    y-=20
    c.drawString(50,y,"Missing Skills:")
    for w in list(miss)[:12]:
        y-=16; c.drawString(70,y,"• "+w)

    y-=30
    c.setFont("Helvetica-Bold",13)
    c.drawString(50,y,"3. Improvement Plan")

    y-=20
    c.setFont("Helvetica",11)
    for r in smart_recommend(score,core,soft,miss):
        y-=16; c.drawString(70,y,"• "+r)

    y-=30
    c.setFont("Helvetica-Bold",13)
    c.drawString(50,y,"4. Recruiter Note")

    y-=20
    c.setFont("Helvetica",11)
    note="Candidate shows strong alignment. Add exact technical keywords and quantifiable impact to improve ATS ranking."
    c.drawString(50,y,note[:90])
    c.drawString(50,y-16,note[90:])

    c.save()
    return name

# ================= LOAD MODEL =================
svc_model=pickle.load(open('clf.pkl','rb'))
tfidf=pickle.load(open('tfidf.pkl','rb'))
encoder=pickle.load(open('encoder.pkl','rb'))

# ================= UI =================

st.markdown('<div class="title">📊 Resume Screening & JD Analyzer </div>',unsafe_allow_html=True)

c1,c2=st.columns([1.1,1])

with c1:
    st.markdown('<div class="card">',unsafe_allow_html=True)
    up=st.file_uploader("Upload Resume",["pdf","docx","txt"])
    st.markdown('</div>',unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">',unsafe_allow_html=True)
    jd=st.text_area("Paste Job Description",height=180)
    st.markdown('</div>',unsafe_allow_html=True)

if up:
    ext=os.path.splitext(up.name)[-1].lower()
    txt=pdf_text(up) if ext==".pdf" else doc_text(up) if ext==".docx" else up.read().decode()

    f=tfidf.transform([txt])
    cat=encoder.inverse_transform(svc_model.predict(f))[0]

    st.markdown("## 🎯 Overview")

    m1,m2,m3=st.columns(3)

    with m1:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        st.markdown("Predicted Role")
        st.markdown(f'<div class="big">{cat}</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    if jd:
        a=expand(txt); b=expand(jd)
        score=semantic(a,b)

        core=skill_score(a)
        soft=soft_score(a)

        res=filter_tokens(tokens(a))
        js=filter_tokens(tokens(b))

        match=res.intersection(js)
        miss=js-res

        with m2:
            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.markdown("JD Match")
            st.markdown(f'<div class="big">{score}%</div>',unsafe_allow_html=True)
            st.progress(score/100)
            st.markdown('</div>',unsafe_allow_html=True)

        with m3:
            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.markdown("Core Skills")
            st.markdown(f'<div class="big">{core}%</div>',unsafe_allow_html=True)
            st.markdown("Soft Skills: "+str(soft)+"%")
            st.markdown('</div>',unsafe_allow_html=True)

        st.markdown("## 🧠 Skill Insights")

        k1,k2=st.columns(2)

        with k1:
            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.markdown("### ✅ Matched")
            for w in list(match)[:25]:
                st.markdown(f'<span class="tag">{w}</span>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        with k2:
            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.markdown("### ❌ Missing")
            for w in list(miss)[:25]:
                st.markdown(f'<span class="tag">{w}</span>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        st.markdown("## 🚀 Recommendations")

        for r in smart_recommend(score,core,soft,miss):
            st.info(r)

        pdf=make_pdf(cat,score,core,soft,match,miss)

        with open(pdf,"rb") as f:
            st.download_button("⬇ Download Professional Report",f,
            file_name="Resume Screening & JD Analyzer.pdf")

else:
    st.info("Upload resume to start enterprise analysis 🚀")
