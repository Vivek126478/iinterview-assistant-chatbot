import streamlit as st
from backend import resume_parser, skill_extractor
from backend.gemma_inference import run_local_gemma_inference
from ui import interview_ui

def initialize_session_state():
    """Initialize all session state variables."""
    st.session_state.setdefault("resume_processed", False)
    st.session_state.setdefault("uploaded_resume_text", "")
    st.session_state.setdefault("key_skills", [])
    st.session_state.setdefault("primary_field", "")
    st.session_state.setdefault("selected_round", None)
    st.session_state.setdefault("interview_engine", None)
    st.session_state.setdefault("current_question", None)
    st.session_state.setdefault("chat_history", [])

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="AI Mock Interview Coach", layout="wide")
    initialize_session_state()

    st.title("🤖 AI Mock Interview Coach")

    # If resume has not been processed, show the upload UI
    if not st.session_state.resume_processed:
        st.markdown("Welcome! Upload your resume to start a mock interview tailored to your skills.")
        
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "docx"],
            help="Upload your resume in PDF or DOCX format."
        )

        if uploaded_file is not None:
            with st.spinner("Analyzing your resume... This may take a moment."):
                try:
                    # Parse the resume file
                    resume_text = resume_parser.parse_resume(uploaded_file, uploaded_file.name)
                    st.session_state.uploaded_resume_text = resume_text

                    # Extract skills using the backend model
                    extracted_data = skill_extractor.extract_skills_and_field(
                        resume_text,
                        use_local_gemma=True,
                        gemma_fn=run_local_gemma_inference
                    )
                    st.session_state.key_skills = extracted_data.get("key_skills", [])
                    st.session_state.primary_field = extracted_data.get("primary_field", "Not Detected")
                    
                    # Mark processing as complete and rerun to switch to the interview UI
                    st.session_state.resume_processed = True
                    st.rerun()

                except Exception as e:
                    st.error(f"An error occurred while processing your resume: {e}")
    
    # If resume has been processed, render the main interview interface
    else:
        interview_ui.render()

if __name__ == "__main__":
    main()