import os
from datetime import datetime, date
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import Workout, Metric

app = FastAPI(title="Fitness Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Fitness Tracker Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# -------- Fitness Tracker Endpoints --------

class WorkoutCreate(Workout):
    pass


class MetricCreate(Metric):
    pass


@app.post("/api/workouts", response_model=dict)
async def add_workout(payload: WorkoutCreate):
    try:
        workout_id = create_document("workout", payload)
        return {"id": workout_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workouts", response_model=List[dict])
async def list_workouts(limit: Optional[int] = 50):
    try:
        docs = get_documents("workout", {}, limit=limit)
        # Convert ObjectId to string for frontend safety
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
            # Ensure date is ISO string
            if isinstance(d.get("date"), (datetime, date)):
                d["date"] = d["date"].isoformat()
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/metrics", response_model=dict)
async def add_metric(payload: MetricCreate):
    try:
        metric_id = create_document("metric", payload)
        return {"id": metric_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics", response_model=List[dict])
async def list_metrics(limit: Optional[int] = 50):
    try:
        docs = get_documents("metric", {}, limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
            if isinstance(d.get("date"), (datetime, date)):
                d["date"] = d["date"].isoformat()
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
