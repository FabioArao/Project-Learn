from fastapi import APIRouter
from pydantic import BaseModel
from app.crewai_config import create_learning_task

router = APIRouter()

class LearningRequest(BaseModel):
    input: str

@router.post("/api/learning-request")
async def create_learning_request(request: LearningRequest):
    # Create and assign the learning task using CrewAI agents
    result = create_learning_task(request.input)
    # Customize the response based on the crew's output or status
    return {"message": "Learning request received and processed", "result": result}
