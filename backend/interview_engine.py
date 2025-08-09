# backend/interview_engine.py
from typing import List, Dict
from . import llm_interaction

class InterviewEngine:
    def __init__(self, user_skills: List[str]):
        self.user_skills = [skill.lower() for skill in user_skills]
        self.current_round: str = ""

    def select_round(self, round_name: str):
        """Sets the current interview round."""
        self.current_round = round_name.lower()

    def generate_question(self) -> str:
        """Generates a new question for the current round and skills."""
        if not self.current_round:
            return "Error: No round selected."
        
        # Add a spinner-friendly message
        print(f"Generating question for round: {self.current_round} with skills: {self.user_skills}")
        return llm_interaction.generate_interview_question(self.current_round, self.user_skills)

    def evaluate_answer(self, question: str, answer: str) -> str:
        """Evaluates a user's answer."""
        if not self.current_round:
            return "Error: No round selected."
        return llm_interaction.evaluate_user_answer(question, answer, self.current_round)

    def get_session_summary(self, chat_history: List[Dict]) -> str:
        """Gets a final summary of the session."""
        return llm_interaction.generate_session_summary(chat_history)