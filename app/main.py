from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import query, uploads

app = FastAPI()

# Enable CORS (adjust allow_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers
app.include_router(query.router)
app.include_router(uploads.router)
