import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Retail Sales Analytics API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "databricks-retail-backend"}

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "dist"))

if os.path.exists(FRONTEND_DIST):
    assets_path = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
        index_file = os.path.join(FRONTEND_DIST, "index.html")
        return FileResponse(index_file)