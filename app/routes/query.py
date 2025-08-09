from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.services import parser, chunker, embedder, retriever, llm_reasoner

router = APIRouter()

# Request model
class HackRxRequest(BaseModel):
    documents: str
    questions: List[str]

# Response model
class HackRxResponse(BaseModel):
    answers: List[str]

# Dummy API key (replace with secure config)
API_KEY = "asdfghjkl"

@router.post("api/v1/hackrx/run", response_model=HackRxResponse)
def run_hackrx(
    request: HackRxRequest,
    authorization: Optional[str] = Header(None)
):
    # Authorization check
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid"
        )
    token = authorization.split("Bearer ")[-1].strip()
    if token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )

    # Step 1: Process the document
    # Here you would actually download & parse the document
    document_content = parser.parse_document(request.documents)
    chunks = chunker.chunk_document(document_content)
    embeddings = embedder.embed_chunks(chunks)

    # Step 2: Retrieve and answer each question
    answers = []
    for question in request.questions:
        parsed_q = llm_reasoner.parse_query(question)
        matches = retriever.retrieve_chunks(parsed_q)
        answer = llm_reasoner.answer_query_with_clauses(question, matches)
        answers.append(answer)

    # Step 3: Return the structured response
    return HackRxResponse(answers=answers)