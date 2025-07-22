# 🧠 Document Retriever using LangGraph

A robust AI-powered system to automate document-driven workflows, built using [LangGraph](https://github.com/langchain-ai/langgraph), FastAPI, and a modern HTML frontend. This project extracts structured information (like National ID and Action) from scanned court order PDFs and performs conditional actions based on their contents.

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

