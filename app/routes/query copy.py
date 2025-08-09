from fastapi import APIRouter
from app.services import parser, chunker, embedder, retriever, llm_reasoner
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def handle_query(q: QueryRequest):
    parsed = llm_reasoner.parse_query(q.query)
    matches = retriever.retrieve_chunks(parsed)
    final_answer = llm_reasoner.answer_query_with_clauses(q.query, matches)
    return {
        "query": q.query,
        "answer": final_answer,
        "clauses": matches
    }
