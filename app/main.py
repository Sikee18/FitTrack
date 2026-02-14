from fastapi import FastAPI
from app.routes import auth, pose_routes
from app.routes import exercise_routes
from app.routes import progress_routes
from app.routes import upload_routes      

app = FastAPI(title="FitTrack API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(exercise_routes.router)
app.include_router(pose_routes.router)
app.include_router(progress_routes.router)
app.include_router(upload_routes.router)
