# 📚 DocuGPT – AI PDF Reader with Chatbot

🚀 AI-powered document assistant that enables users to upload PDFs and interact with them using intelligent summarization and question answering.

---

## 📌 Overview

DocuGPT is an end-to-end AI-based web application that processes PDF documents and allows users to extract insights through a chatbot interface.

The system supports:

* Text extraction from PDFs
* Table extraction
* OCR for scanned documents
* Automatic summarization
* Semantic question answering

---

## ✨ Features

* 📄 Upload and process PDF documents
* 📝 Extract text using pdfplumber
* 📊 Extract tables from PDFs
* 🔎 OCR support using Tesseract (for scanned PDFs)
* ✂️ Clean and preprocess document text
* 🤖 Generate summaries using embedding-based approach
* 💬 Ask questions and get relevant answers
* 🔑 Keyword extraction from documents

---

## 🧠 System Workflow

```id="sht9nn"
User Upload PDF
        ↓
PDF Processing (Text + Tables + OCR)
        ↓
Text Cleaning & Preprocessing
        ↓
Sentence Embedding (SentenceTransformers)
        ↓
Cosine Similarity Computation
        ↓
Summary Generation + Question Answering
        ↓
Results Displayed to User
```

---

## 🏗️ Project Structure

```id="pwk2u1"
DocuGPT
│
├── backend/
│   └── app.py                # Flask backend
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── summary.html
│   ├── qa.html
│   ├── table.html
│   └── style.css
│
├── data/
│   └── sample.pdf
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

### 🖥️ Backend

* Python
* Flask
* Flask-CORS

### 📄 PDF Processing

* pdfplumber
* pdf2image
* pytesseract (OCR)

### 🤖 AI / NLP

* sentence-transformers
* scikit-learn (cosine similarity)
* NumPy

### 🌐 Frontend

* HTML
* CSS

---

## 🤖 AI Approach

### 🔹 Text Summarization

* Split document into sentences
* Convert sentences into embeddings
* Compute similarity with overall document
* Select top relevant sentences
* Combine into final summary

### 🔹 Question Answering

* Convert user question into embedding
* Compare with sentence embeddings
* Use cosine similarity to find best match
* Return most relevant sentences as answer

---

## 👩‍💻 My Contribution

* Independently designed and developed the complete system
* Built PDF processing pipeline (text, tables, OCR)
* Implemented embedding-based summarization
* Developed semantic question answering system
* Designed Flask backend APIs and routing
* Created frontend UI for interaction
* Integrated full workflow from document upload to AI response

---

## ▶️ How to Run

### 1️⃣ Install Dependencies

```id="lfqvyv"
pip install flask flask-cors pdfplumber pytesseract pdf2image scikit-learn sentence-transformers numpy
```

---

### 2️⃣ Install Tesseract OCR

Download from:
https://github.com/tesseract-ocr/tesseract

Set path (Windows):

```id="3z7c6q"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

### 3️⃣ Run Application

```id="7d6svk"
python backend/app.py
```

---

### 4️⃣ Open in Browser

```id="ht3q5h"
http://127.0.0.1:5000
```

---

## 📊 Output

* Extracted text from PDF
* Tables displayed from document
* Summary of document
* Answers to user questions
* Keywords from text

---

## 📌 Future Enhancements

* Improve chatbot accuracy using advanced LLMs
* Support multiple document uploads
* Add modern UI (React / Streamlit)
* Deploy on cloud platform

---

## 📄 License

This project is developed for educational and learning purposes.

---

## ⭐ Project Description

DocuGPT combines document processing with AI techniques to simulate a basic intelligent document assistant, enabling users to interact with PDFs in a smart and efficient way.
