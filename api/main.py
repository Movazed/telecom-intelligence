from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import usage, ml_predict

# 1. Initialize the App
app = FastAPI(title="Telecom Network Intelligence API")

# 2. CORS Configuration (Crucial for Phase 5 React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows React (localhost:5173) to talk to the API
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# 3. Include Distributed Routers
# This tells FastAPI to look inside your routes folder for the endpoints
app.include_router(usage.router, prefix="/usage", tags=["Analytics"])
app.include_router(ml_predict.router, tags=["Machine Learning"])

# 4. Simple Health Check
@app.get("/")
def health_check():
    return {
        "status": "online", 
        "system": "Telecom Intelligence",
        "documentation": "/docs"
    }