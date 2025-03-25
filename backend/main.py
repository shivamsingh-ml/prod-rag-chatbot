from fastapi import FastAPI, File, UploadFile
from pdf_utils import extract_text_chunks
from embedding_utils import upload_documents_to_qdrant, delete_collection
from qa_utils import run_qa 
import uuid
from fastapi import FastAPI, Request


app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    documents = extract_text_chunks(content)
    
    session_id = str(uuid.uuid4())
    upload_documents_to_qdrant(documents, session_id)

    return {
        "status": "success",
        "session_id": session_id,
        "chunks_uploaded": len(documents)
    }

@app.post("/delete-collection/")
async def delete_session(request: Request):
    body = await request.json()
    session_id = body.get("session_id")
    if not session_id:
        return {"status": "error", "message": "Missing session_id"}
    success = delete_collection(session_id)
    if success:
        return {"status": "success", "message": f"Collection '{session_id}' deleted."}
    else:
        return {"status": "error", "message": f"Failed to delete collection '{session_id}'."}


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    query = body.get("query")
    session_id = body.get("session_id")
    if not query or not session_id:
        return {"status": "error", "message": "Missing query or session_id"}
    try:
        result = run_qa(query, session_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}