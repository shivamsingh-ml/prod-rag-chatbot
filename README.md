# 🧠 Production-ready RAG Chatbot

Production-ready RAG Chatbot is a fully containerized, orchestrated application designed to bring **Retrieval-Augmented Generation (RAG)** into production environments with ease.

---

## 📽 Demo

https://github.com/user-attachments/assets/3044c441-0a5b-4dd8-a112-5cbe13b84365

---

## 📁 Project Structure

```text
prod-rag-chatbot/
├── backend/                        # Backend logic for RAG pipeline
│   ├── main.py                     # FastAPI endpoints for PDF upload, chat, session cleanup
│   ├── embedding_utils.py          # Handles embedding documents & uploading to Qdrant
│   ├── pdf_utils.py                # Extracts and chunks text from PDFs
│   ├── qa_utils.py                 # Builds QA chain using HuggingFace LLM + Qdrant retriever
│   ├── Dockerfile
│   ├── .env                        # Backend config (API keys, host info)
│   └── pyproject.toml              # Poetry dependencies
│
├── frontend/                       # Streamlit UI for uploading, chatting, and ending session
│   ├── app.py                      # Main Streamlit interface (chat + PDF uploader)
│   ├── Dockerfile
│   └── pyproject.toml              # Poetry dependencies
│
├── qdrant_data/                    # Persistent Qdrant volume for storing vectors
├── .gitignore
├── docker-compose.yml              # Orchestrates frontend, backend, and Qdrant containers
└── .venv/                          # Python virtual environment
```

---

### 🧱 Microservices Architecture Overview
![Architecture](assets/Architecture.drawio.svg)

### 🔄 Flow Diagram
![Flow](assets/Flow_Diagram.drawio.svg)

---

## 🧰 Tech Stack

- **FastAPI** — Async backend for document ingestion and querying
- **Streamlit** — Lightweight UI for interacting with the bot
- **Qdrant** — Vector store for efficient retrieval
- **Hugging Face (Mistral-7B)** — LLM used for final answer generation
- **LangChain** — Manages pipelines for embedding, retrieval, and QA
- **SentenceTransformers** — Used for embedding via `all-MiniLM-L6-v2`
- **PyMuPDF** — PDF parsing
- **Docker + Compose** — Containerized setup

---

## ⚙️ Setup & Installation

### 1. Clone the Repo

```bash
git clone https://github.com/shivamsingh-ml/production-rag-chatbot.git
cd production-rag-chatbot
```

### 2. Configure Environment Variables

Create a `.env` file in `backend/`:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_key
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

### 3. Start Services with Docker Compose

```bash
docker-compose up --build
```

This will launch:
- FastAPI backend at `http://localhost:8000`
- Streamlit frontend at `http://localhost:8501`
- Qdrant vector database at `http://localhost:6333`

---

## 🚀 Usage (Web Interface)

Visit the frontend at [`http://localhost:8501`](http://localhost:8501)

1. **Upload PDF** — Accepts a single PDF file.
2. **Start Session** — Embeds the document and stores it in Qdrant.
3. **Chat** — Type natural language questions to interact with the document.
4. **End Session** — Deletes the session’s Qdrant collection.

Each session is isolated via a unique `session_id`. Chat state is preserved in the app until cleared.

---

## 🧪 API Endpoints

- `POST /upload-pdf/` — Upload and process PDF
- `POST /chat` — Ask a question with `session_id`
- `POST /delete-collection/` — Delete session vector store

Example request:

```bash
curl -X POST http://localhost:8000/chat      -H "Content-Type: application/json"      -d '{"query": "Summarize the document", "session_id": "abc-123"}'
```

---

## 📦 Poetry (Backend & Frontend)

Both services use Poetry for dependency management.

To use locally (example for backend):

```bash
cd backend
poetry install
poetry run uvicorn main:app --reload
```

---


---

## 🐳 Docker Instructions

You can run the entire RAG Chatbot stack using Docker Compose. This setup includes:

- `backend` — FastAPI app for PDF upload, vector DB interaction, and QA
- `frontend` — Streamlit UI to interact with the bot
- `qdrant` — Vector database

### 🛠️ Build & Run (Recommended)

```bash
docker-compose up --build
```

- Frontend will be available at: [http://localhost:8501](http://localhost:8501)
- Backend API will run at: [http://localhost:8000](http://localhost:8000)
- Qdrant vector DB UI (if needed): [http://localhost:6333](http://localhost:6333)

### 🧼 Tear Down

```bash
docker-compose down
```

To remove named volumes and containers completely:

```bash
docker-compose down -v
```

### 🔄 Rebuild after Code Changes

```bash
docker-compose build
```


## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

