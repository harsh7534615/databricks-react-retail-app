import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Retail Sales Analytics API", version="2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. API Endpoints
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "databricks-retail-backend", "mode": "databricks-uc-ready"}

@app.get("/api/sales-summary")
def get_sales_summary():
    return {
        "total_revenue": 1450200.00,
        "total_orders": 9120,
        "top_category": "Home Appliances",
        "recent_transactions": [
            {"id": "TXN-2001", "store": "Noida Sector 62", "amount": 6200.00, "status": "Completed"},
            {"id": "TXN-2002", "store": "Greater Noida West", "amount": 3400.00, "status": "Completed"},
            {"id": "TXN-2003", "store": "Delhi Connaught Place", "amount": 12500.00, "status": "Processing"}
        ]
    }

# 2. Robust Frontend Static Mounting (Databricks Apps Container Path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "dist"))

if os.path.exists(FRONTEND_DIST):
    # Mount static assets folder
    assets_path = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    # Serve index.html for root and any unmatched non-API routes (React Router support)
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # If an API route wasn't matched above, return 404 instead of index.html
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
        index_file = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"detail": "Frontend build index.html not found"}
else:
    @app.get("/")
    def root_fallback():
        return {"message": "FastAPI backend is running, but frontend/dist directory was not found during build."}