from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

# Import your service
from app.services.llm_service import generate_story

router = APIRouter()

class StoryRequest(BaseModel):
    topic: str
    # CHANGE: Default is now "gemini"
    model: Literal["gemini", "openai"] = "gemini" 

@router.post("/generate-story")
def generate_story_api(req: StoryRequest):
    try:
        story_text = generate_story(req.model, req.topic)
        
        return {
            "requested_model": req.model,
            "topic": req.topic,
            "story": story_text
        }

    except Exception as e:
        # This will print the error to your VS Code terminal
        print(f"!!! CRITICAL API ERROR: {e}") 
        raise HTTPException(status_code=500, detail=str(e))