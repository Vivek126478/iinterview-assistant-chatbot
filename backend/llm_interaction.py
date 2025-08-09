import subprocess
import json
from typing import List, Dict

def run_gemma_prompt(prompt: str) -> str:
    """
    Sends a prompt to the local Gemma model via Ollama and returns the response.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma2:2b"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode("utf-8").strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Ollama inference failed: {e}")
        return "Error: Could not get a response from the local AI model. Is Ollama running and is the model 'gemma2:2b' installed?"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred while communicating with the model."

def generate_interview_question(round_name: str, skills: List[str]) -> str:
    """
    Generates a real-time interview question using the LLM.
    """
    skill_string = ", ".join(skills) if skills else "general software engineering"
    
    prompt = f"""
    You are an AI Interview Coach. Your task is to ask a single, concise interview question.
    Do NOT provide any preamble, conversation, or explanation. Only output the question itself.

    Interview Round: {round_name}
    User's Skills: {skill_string}

    Based on the round and skills, generate one appropriate interview question.
    For example, if the round is 'Coding' and skills are 'Python', ask a Python coding question.
    If the round is 'HR', ask a behavioral question.
    """
    return run_gemma_prompt(prompt)

def evaluate_user_answer(question: str, answer: str, round_name: str) -> str:
    """
    Uses the LLM to provide feedback on a user's answer.
    """
    prompt = f"""
    You are an AI Interview Coach. Your task is to provide CONCISE feedback on a user's answer to an interview question.
    Keep the feedback to 2-3 sentences. Start by directly addressing the user's answer and then provide a constructive tip.

    Interview Round: {round_name}
    Question Asked: "{question}"
    User's Answer: "{answer}"

    Provide your feedback now.
    """
    return run_gemma_prompt(prompt)

def generate_session_summary(chat_history: List[Dict]) -> str:
    """
    Uses the LLM to generate a final summary of the interview session.
    """
    transcript = "\n".join(f"{msg['role']}: {msg['content']}" for msg in chat_history)
    
    prompt = f"""
    You are an AI Interview Coach. Based on the following interview transcript, please provide a brief, 2-3 bullet point summary of the user's performance.
    Focus on identifying potential strengths and key areas for improvement.

    Transcript:
    ---
    {transcript}
    ---

    Provide the summary now.
    """
    return run_gemma_prompt(prompt)