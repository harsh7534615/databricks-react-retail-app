import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Retail Sales Analytics API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. API Routes (Must come BEFORE static file catch-all)
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "databricks-retail-backend"}

@app.get("/api/sales-summary")
def get_sales_summary():
    return {
        "total_revenue": 1245500.50,
        "total_orders": 8420,
        "top_category": "Electronics",
        "recent_transactions": [
            {"id": "TXN-1001", "store": "Noida Sector 18", "amount": 4500.00, "status": "Completed"},
            {"id": "TXN-1002", "store": "Greater Noida", "amount": 1200.50, "status": "Completed"},
            {"id": "TXN-1003", "store": "Delhi NCR", "amount": 8900.00, "status": "Pending"}
        ]
    }

# 2. Serve Compiled React Frontend (Databricks Apps Production Pattern)
frontend_dist_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

if os.path.exists(frontend_dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_path, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Serve index.html for any non-API route (supports React Router)
        index_file = os.path.join(frontend_dist_path, "index.html")
        return FileResponse(index_file)