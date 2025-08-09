from typing import Dict
from backend.gemma_inference import run_local_gemma_inference

def extract_skills_and_field(resume_text: str, use_local_gemma: bool = True, gemma_fn=None) -> Dict:
    """
    Extracts skills and primary professional field from resume text.
    
    This function acts as a wrapper, primarily calling the local Gemma 
    inference function. It can be extended to support other remote APIs.
    """
    if use_local_gemma:
        # If a specific Gemma function is passed, use it.
        # Otherwise, fall back to the default one.
        if gemma_fn:
            return gemma_fn(resume_text)
        return run_local_gemma_inference(resume_text)

    # This is a placeholder for a potential future remote API call.
    return {"primary_field": None, "key_skills": []}