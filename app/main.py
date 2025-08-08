from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import query, uploads
import os

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(query.router)
app.include_router(uploads.router)

# Path to the frontend folder
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

# Serve static assets (CSS/JS/images)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# HTML Routes
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/about", response_class=HTMLResponse)
async def serve_about():
    return FileResponse(os.path.join(frontend_path, "about.html"))

@app.get("/services", response_class=HTMLResponse)
async def serve_services():
    return FileResponse(os.path.join(frontend_path, "services.html"))

@app.get("/contact", response_class=HTMLResponse)
async def serve_contact():
    return FileResponse(os.path.join(frontend_path, "contact.html"))
