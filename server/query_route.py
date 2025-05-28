from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.responses import StreamingResponse

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str


@router.post("/query")
def handle_query(request: PromptRequest):
    try:
        from query import query_main, intent_classifier
        intent = intent_classifier(request.prompt)
        return query_main(request.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search_index")
def search_index(request: PromptRequest):
    try:
        from policy_services.pdf_faiss import search_faiss
        scores, results = search_faiss(request.prompt, top_k=5)
        if not results:
            return {"message": "No relevant documents found."}
        return {
            "scores": scores[0].tolist(),
            "results": [{"filename": r['filename'], "chunk_id": r['chunk_id'], "text": r['text']} for r in results]
        }
    except Exception as e:
        return {"error": str(e)}