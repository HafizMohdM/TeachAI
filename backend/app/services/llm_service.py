import logging
from openai import OpenAI
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#INITIALIZATION OF CLIENTS
gemini_model = None
openai_client = None

#GEMINI INIT
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    # USE 'gemini-1.5-flash' (Faster/Cheaper/Newer) instead of 'gemini-pro'
    gemini_model = genai.GenerativeModel('gemini-flash-latest')
    logger.info("Gemini Client Initialized")
except Exception as e:
    logger.error(f"Gemini Init Failed: {e}")


#OPENAI INIT
try:
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
except Exception as e:
    logger.error(f"OpenAI Init Failed: {e}")



#GENERATION FUNCTIONS
def generate_story_gemini(topic: str):
    if not gemini_model:
        raise RuntimeError("Gemini client not ready.")
    
    # Generate content
    resp = gemini_model.generate_content(f"Write a short story about {topic}")
    
    # Safe extraction
    if hasattr(resp, "text"):
        return resp.text
    if hasattr(resp, "parts"):
        return resp.parts[0].text
    return str(resp)

def generate_story_openai(topic: str):
    if not openai_client:
        raise RuntimeError("OpenAI client not ready.")
    
    resp = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Write a short story about {topic}"}]
    )
    return resp.choices[0].message.content



# --- 3. MAIN SELECTOR (PRIORITY: GEMINI) ---

def generate_story(model: str, topic: str):
    """
    Main function to decide which AI to use.
    """
    
    # If user wants GEMINI (or default)
    if model == "gemini":
        try:
            return generate_story_gemini(topic)
        except Exception as e:
            # Log the REAL Gemini error so we can see it
            logger.error(f"Gemini Failed: {e}")
            logger.warning("Attempting fallback to OpenAI...")
            
            # Fallback
            return generate_story_openai(topic)

    # If user explicitly wants OPENAI
    elif model == "openai":
        try:
            return generate_story_openai(topic)
        except Exception as e:
            logger.error(f"OpenAI Failed: {e}")
            logger.warning("Attempting fallback to Gemini...")
            
            # Fallback
            return generate_story_gemini(topic)
    
    else:
        # Absolute fallback for invalid inputs -> Gemini
        return generate_story_gemini(topic)