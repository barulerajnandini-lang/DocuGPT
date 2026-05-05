# 📚 DocuGPT – AI PDF Reader with Chatbot

🚀 AI-powered PDF Reader with Chatbot using NLP & Embeddings

---

## 🚀 Project Overview

DocuGPT is a web-based application that allows users to upload PDF documents and interact with them intelligently.

The system can:

* Extract text and tables from PDFs
* Perform OCR on scanned PDFs
* Generate summaries
* Answer user questions based on document content

---

## 🎯 Features

* 📄 Upload PDF files
* 📝 Text extraction from PDF
* 📊 Table extraction
* 🔎 OCR support (for scanned PDFs)
* ✂️ Text cleaning & preprocessing
* 🤖 AI-based summarization
* 💬 Question Answering chatbot
* 🔑 Keyword extraction

---

## 🧠 Workflow

```
PDF Upload
   ↓
Text Extraction (pdfplumber)
   ↓
OCR (if needed)
   ↓
Text Cleaning
   ↓
Sentence Embeddings
   ↓
Cosine Similarity
   ↓
Summary + Answers
```

---

## 🏗️ Project Structure

```
DocuGPT
│
├── backend/
│   └── app.py
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

### 📄 PDF Processing

* pdfplumber
* pdf2image
* pytesseract (OCR)

### 🤖 AI / NLP

* sentence-transformers
* scikit-learn
* NumPy

### 🌐 Frontend

* HTML
* CSS

---

## 🤖 AI Logic

### 🔹 Summary

* Convert sentences into embeddings
* Calculate similarity with document
* Select top relevant sentences
* Combine into summary

### 🔹 Question Answering

* Convert question + sentences into embeddings
* Use cosine similarity
* Return most relevant sentences

---

## 👩‍💻 My Contribution (Member 2)

* Implemented PDF text extraction
* Added OCR using Tesseract
* Extracted tables from PDFs
* Cleaned and processed document text
* Built PDF processing pipeline

---

## ▶️ How to Run

### 1️⃣ Install Dependencies

```
pip install flask flask-cors pdfplumber pytesseract pdf2image scikit-learn sentence-transformers numpy
```

---

### 2️⃣ Install OCR

Download Tesseract and set path in code:

```
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

### 3️⃣ Run Project

```
python backend/app.py
```

---

### 4️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 📌 Future Improvements

* Improve chatbot accuracy
* Add multiple PDF support
* Build better UI
* Deploy project online

---

## 📄 License

This project is for educational purposes.

---

## ⭐ Project Name Meaning

DocuGPT = Document + GPT-style interaction system
