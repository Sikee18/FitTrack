from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.pose.pose_detector import PoseDetector


router = APIRouter(prefix="/pose")

@router.post("/process_frame")
async def process_frame(request: Request):
    data = await request.json()
    image_base64 = data.get("image_base64")
    if not image_base64:
        return JSONResponse(status_code=400, content={"error": "Image data is required"})

    detector = PoseDetector()
    landmarks = detector.detect(image_base64)
    return {"landmarks": landmarks}
