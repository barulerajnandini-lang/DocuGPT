from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import pdfplumber
import re
import numpy as np
import pytesseract

from pdf2image import convert_from_path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity





from sentence_transformers import SentenceTransformer

# ======================
# WINDOWS OCR PATH
# ======================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ======================
# INITIALIZE APP
# ======================

app = Flask(__name__)
CORS(app)

# ======================
# GLOBAL VARIABLES
# ======================

document_text = ""
tables_data = []

# ======================
# LOAD LLM MODEL
# ======================

model = SentenceTransformer('all-MiniLM-L6-v2')

# ======================
# SIMPLE SENTENCE SPLITTER (REPLACES NLTK)
# ======================

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if len(s.split()) > 6]

# ======================
# CLEAN TEXT FOR SUMMARY
# ======================

def clean_text_for_summary(text):

    sentences = split_sentences(text)

    clean_sentences = []

    for sentence in sentences:

        sentence = sentence.strip()

        if sentence.lower().startswith("table"):
            continue

        if len(sentence.split()) < 6:
            continue

        if re.match(r'^[0-9\s\.\%\(\)]+$', sentence):
            continue

        clean_sentences.append(sentence)

    return clean_sentences

# ======================
# LOAD PDF TEXT
# ======================

def load_pdf(file):

    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass

    # OCR fallback
    if text.strip() == "":
        images = convert_from_path(file)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text

# ======================
# EXTRACT TABLES
# ======================

def extract_tables(file):

    tables = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_tables()
            if extracted:
                tables.extend(extracted)

    return tables

# ======================
# LLM-BASED SUMMARY
# ======================

def short_summary(text, n=6):

    if text.strip() == "":
        return "No content available."

    # Clean text
    text = re.sub(r'\s+', ' ', text)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Remove duplicates + filter
    clean_sentences = []
    seen = set()

    for s in sentences:
        s_clean = s.strip().lower()

        if len(s.split()) < 8:
            continue

        if "factor cause effect" in s_clean:
            continue

        if s_clean in seen:
            continue

        seen.add(s_clean)
        clean_sentences.append(s.strip())

    if len(clean_sentences) == 0:
        return "No meaningful content."

    # Convert to embeddings
    embeddings = model.encode(clean_sentences)

    # Document embedding
    doc_embedding = np.mean(embeddings, axis=0)

    # Similarity scores
    scores = cosine_similarity([doc_embedding], embeddings)[0]

    # Get top sentences
    top_indices = scores.argsort()[-n:][::-1]

    selected = [clean_sentences[i] for i in top_indices]

    # Sort them in original order (IMPORTANT for flow)
    ordered = sorted(selected, key=lambda x: sentences.index(x))

    # Join into ONE paragraph
    summary = " ".join(ordered)

    return summary
# ======================
# KEYWORDS
# ======================

def extract_keywords(text):

    words = re.findall(r'\b[a-zA-Z]{6,}\b', text.lower())

    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) + 1

    return sorted(freq, key=freq.get, reverse=True)[:10]

# ======================
# CLEAN DOCUMENT TEXT
# ======================

def clean_document_text(text):

    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text

# ======================
# LLM QA SYSTEM
# ======================
def answer_question(question):

    global document_text

    if document_text.strip() == "":
        return "Upload a document first."

    if len(question.split()) < 2:
        return "Ask a proper question."

    # Clean document
    cleaned_text = re.sub(r'\s+', ' ', document_text)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)

    # Filter valid sentences
    valid_sentences = []
    seen = set()

    for s in sentences:
        s_clean = s.strip().lower()

        if len(s.split()) < 8:
            continue

        if "factor cause effect" in s_clean:
            continue

        if s_clean in seen:
            continue

        seen.add(s_clean)
        valid_sentences.append(s.strip())

    if len(valid_sentences) == 0:
        return "No useful content found."

    # Embeddings
    sentence_embeddings = model.encode(valid_sentences)
    question_embedding = model.encode([question])

    similarity_scores = cosine_similarity(
        question_embedding,
        sentence_embeddings
    )[0]

    # Threshold
    if max(similarity_scores) < 0.45:
        return "Please ask a question related to the document."

    # Get top 5 relevant sentences
    top_indices = similarity_scores.argsort()[-5:][::-1]

    selected_sentences = [valid_sentences[i] for i in top_indices]

    # Remove duplicate meaning sentences again
    final_sentences = []
    seen = set()

    for s in selected_sentences:
        s_clean = s.lower()
        if s_clean not in seen:
            seen.add(s_clean)
            final_sentences.append(s)

    # Join into ONE paragraph
    final_answer = " ".join(final_sentences)

    return final_answer

# ======================
# ROUTES
# ======================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload_page")
def upload_page():
    return render_template("upload.html")

@app.route("/summary_page")
def summary_page():

    global document_text, tables_data

    if document_text == "":
        return "Upload PDF first."

    return render_template(
        "summary.html",
        summary=short_summary(document_text),
        keywords=extract_keywords(document_text),
        tables=tables_data
    )

@app.route("/qa_page")
def qa_page():
    return render_template("qa.html")

@app.route("/table_page")
def table_page():

    global tables_data

    if not tables_data:
        return "No tables found."

    return render_template("table.html", tables=tables_data)

# ======================
# UPLOAD
# ======================

@app.route("/upload", methods=["POST"])
def upload():

    global document_text, tables_data

    file = request.files.get("file")

    if not file:
        return "No file uploaded."

    document_text = load_pdf(file)

    file.seek(0)

    tables_data = extract_tables(file)

    return render_template(
        "summary.html",
        summary=short_summary(document_text),
        keywords=extract_keywords(document_text),
        tables=tables_data
    )

# ======================
# ASK
# ======================

@app.route("/ask", methods=["POST"])
def ask():

    question = request.json.get("question")

    answer = answer_question(question)

    return jsonify({"answer": answer})

# ======================
# RUN
# ======================

if __name__ == "__main__":
    app.run(debug=True)
