# 🧠 Document Retriever using LangGraph

A robust AI-powered system to automate document-driven workflows, built using [LangGraph](https://github.com/langchain-ai/langgraph), FastAPI, and a modern HTML frontend. This project extracts structured information (like National ID and Action) from scanned court order PDFs and performs conditional actions based on their contents.

---

## 🧭 Workflow Overview

[![LangGraph Flowchart]([https://github.com/shanalexjoseph/Document-Retriever-using-LangGraph/blob/main/assets/Flowchart.png?raw=true)](https://github.com/shanalexjoseph/Document-Retriever-using-LangGraph/blob/main/assets/Flowchart.png?raw=true](https://github.com/shanalexjoseph/Document-Retriever-using-LangGraph/blob/main/assets/Document%20retriever%20.png?raw=true))

---
## 🚀 Features

✅ OCR extraction from scanned PDFs  
✅ National ID and Action field extraction using LLM (via Hugging Face)  
✅ Validation against internal customer database  
✅ Action execution or rejection (based on business logic)  
✅ Intuitive, responsive frontend with multi-file upload  
✅ Modular architecture and Dockerized deployment  

---

## 🛠️ Tech Stack

- **LangGraph** (Agentic workflow engine)
- **FastAPI** (backend API)
- **HTML + Bootstrap 5** (frontend UI)
- **HuggingFace Transformers API** (LLM inference)
- **Python 3.11**
- **Docker** (containerized deployment)

---
## ⚙️ Getting Started (Local)

◆ Clone the repo: 
      git clone https://github.com/your-username/Document-Retriever-using-LangGraph.git
      cd Document-Retriever-using-LangGraph

◆ Create virtual environment:
      python -m venv venv
      source venv/bin/activate  # or venv\Scripts\activate on Windows

◆ Install dependencies: pip install -r requirements.txt

◆ Create a .env file with: HF_TOKEN=your_huggingface_token_here

◆ Run the app: uvicorn main:app --reload

◆ Access the frontend: Open your browser and go to: http://127.0.0.1:8000/frontend/index.html


---

## 🐳 Running with Docker
◆ Build the Docker image: docker build -t doc-retriever .

◆ Run the container: docker run -p 8000:8000 doc-retriever

◆ To access the app: Go to http://localhost:8000/frontend/index.html

---

## 📤 API Endpoints

◆ Endpoint	Method	Description

◆ /process_doc	POST	Accepts single PDF for processing

◆ /process_doc_multiple	POST	Accepts multiple PDFs

---

## 💡 Sample Output

<img width="2512" height="1347" alt="Screenshot 2025-07-22 172748" src="https://github.com/user-attachments/assets/4ba136c3-0ea7-433b-bc37-4d8f040a11d7" />
<img width="2539" height="1397" alt="Screenshot 2025-07-22 172815" src="https://github.com/user-attachments/assets/35867bd9-c4f3-462e-ab36-01c7ce66e7c0" />

---

## 🔒 Security

This app uses Hugging Face API securely via .env and dotenv. Make sure you do not commit secrets into the repo.

---

## 🧑‍💼 Use Case

◆ Designed for financial institutions or legal firms to automate the processing of judicial documents by:

◆ Digitally reading scanned orders

◆ Verifying customer IDs

◆ Executing bank-level actions like fund freezes

---

## 📂 Project Structure

```bash
.
├── Dockerfile
├── main.py               # FastAPI entrypoint
├── data/
│   ├── actions.csv
│   └── customers.csv
├── frontend/
│   └── index.html        # Modern responsive UI
├── workflow/
│   ├── __init__.py
│   ├── nodes.py          # Core LangGraph node functions
│   ├── graph_runner.py   # Orchestrates LangGraph workflow
│   ├── llm_utils.py      # LLM-related helpers
│   ├── ocr_utils.py      # OCR extraction using DocTR
│   └── state_def.py      # State object schema
└── .env                  # Hugging Face API token

