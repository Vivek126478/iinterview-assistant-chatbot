import subprocess
import json
import re

def run_local_gemma_inference(resume_text: str) -> dict:
    """
    Runs local Gemma2:2b via Ollama and extracts skills + primary field.
    This version has a more robust JSON extractor to handle model outputs
    that include Markdown fences or other text.
    """
    prompt = f"""
Extract the primary professional field and a list of key skills from the following resume text.

Resume:
{resume_text}

Respond ONLY in JSON format like this:
{{
  "primary_field": "Data Science",
  "key_skills": ["python", "java", "docker"]
}}
"""

    try:
        # Run the Ollama command
        result = subprocess.run(
            ["ollama", "run", "gemma2:2b"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output = result.stdout.decode("utf-8").strip()

        if not output:
            print("Gemma returned empty output. STDERR:", result.stderr.decode("utf-8"))
            return {"primary_field": None, "key_skills": []}

        # --- New, More Robust JSON Extraction Logic ---
        # Find the first '{' and the last '}' in the output string
        try:
            start_index = output.index('{')
            end_index = output.rindex('}') + 1
            # Slice the string to get only the JSON part
            json_str = output[start_index:end_index]
            
            # The model sometimes uses non-standard whitespace. Let's clean it.
            json_str = json_str.replace(u'\xa0', u' ')

            data = json.loads(json_str)

        except (ValueError, json.JSONDecodeError) as e:
            # This will now catch errors if the '{' or '}' are not found, or if parsing still fails.
            print("Model output was not valid JSON even after extraction. ERROR:", e)
            print("RAW MODEL OUTPUT:", output) # Print the raw output for better debugging
            return {"primary_field": None, "key_skills": []}

        # Return the extracted data in a consistent format
        return {
            "primary_field": data.get("primary_field"),
            "key_skills": data.get("key_skills", []) or data.get("skills", [])
        }

    except Exception as e:
        print(f"A critical error occurred in the Gemma model inference process: {e}")
        return {"primary_field": None, "key_skills": []}