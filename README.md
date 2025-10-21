# 🚘 Driving License Reader API

A simple FastAPI-based project that extracts details from a scanned **Driving License** image using **OCR (pytesseract)** and **regex**.

---

## 🚀 Features

- Upload an image of a driving license (`.jpg`, `.jpeg`, `.png`)
- Automatically extracts:
  - License holder’s **Name**
  - License holder’s **Age**
  - License **Number**
  - License **Validity**
- Built with **FastAPI**, **Pillow**, and **Tesseract OCR**

---

## 🧩 Setup Instructions

### 1️⃣ Clone the repository
```
git clone https://github.com/AnayP99/driving-license-reader.git
cd driving-license-reader
```

### 2️⃣ Create a virtual environment
```
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate   # On macOS/Linux
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Install Tesseract OCR
Windows: Download and install from
👉 https://tesseract-ocr.github.io/tessdoc/Downloads.html
(Add Tesseract to PATH during installation)

Linux/macOS:
```
sudo apt install tesseract-ocr
```

### 5️⃣ Run the API
```
uvicorn main:app --reload
```

### 6️⃣ Test the API
```
Open your browser at:
👉 http://127.0.0.1:8000/docs

Use the /upload endpoint to upload your Driving License image.
```