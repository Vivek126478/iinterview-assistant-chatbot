# utils.py

def format_skills_list(skills):
    """
    Format a list of skills into a comma-separated string.
    """
    if not skills:
        return "No skills found."
    return ", ".join(skills)

def clean_text(text):
    """
    Simple text cleaner: lowercases and strips whitespace.
    """
    if not text:
        return ""
    return text.strip().lower()

# Add more utility functions as needed
