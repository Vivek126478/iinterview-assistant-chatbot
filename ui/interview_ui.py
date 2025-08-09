import streamlit as st
from backend.interview_engine import InterviewEngine

def render():
    """Renders the main interview interface."""
    st.sidebar.header("Resume Analysis")
    st.sidebar.success(f"**Field:** {st.session_state.get('primary_field', 'N/A')}")
    st.sidebar.write("**Your Skills:**")
    st.sidebar.info(", ".join(st.session_state.key_skills) if st.session_state.key_skills else "None Detected")

    if st.session_state.get("selected_round") is None:
        _render_round_selection()
    elif st.session_state.get("session_ended", False):
        _render_session_summary()
    else:
        _render_chat_interface()

def _render_round_selection():
    """Shows the round selection buttons."""
    st.info("Your resume has been analyzed. Please select an interview round to begin.")
    col1, col2 = st.columns(2)
    if col1.button("🧠 Aptitude Round", use_container_width=True):
        _start_interview("Aptitude")
    if col2.button("💻 Coding Round", use_container_width=True):
        _start_interview("Coding")
    col3, col4 = st.columns(2)
    if col3.button("🏗️ System Design Round", use_container_width=True):
        _start_interview("System Design")
    if col4.button("👥 HR Round", use_container_width=True):
        _start_interview("HR")

def _start_interview(round_name: str):
    """Initializes the interview engine for the selected round."""
    st.session_state.selected_round = round_name
    st.session_state.session_ended = False
    engine = InterviewEngine(st.session_state.get("key_skills", []))
    engine.select_round(round_name)
    st.session_state.interview_engine = engine
    st.session_state.chat_history = []
    st.session_state.current_question = None
    st.rerun()

def _render_chat_interface():
    """Displays the chat interface for the dynamic interview."""
    engine = st.session_state.interview_engine
    st.header(f"{st.session_state.selected_round} Round")
    
    # Generate the first question if it doesn't exist
    if 'current_question' not in st.session_state or st.session_state.current_question is None:
        with st.spinner("🤔 Generating your first question..."):
            question = engine.generate_question()
            st.session_state.current_question = question
            st.session_state.chat_history.append({"role": "assistant", "content": question})

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    user_answer = st.chat_input("Your answer...")
    if user_answer:
        st.session_state.chat_history.append({"role": "user", "content": user_answer})
        
        with st.spinner("🧐 Evaluating your answer..."):
            feedback = engine.evaluate_answer(st.session_state.current_question, user_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            
        with st.spinner("🤔 Generating your next question..."):
            next_question = engine.generate_question()
            st.session_state.current_question = next_question
            st.session_state.chat_history.append({"role": "assistant", "content": next_question})
        
        st.rerun()

    if st.button("🔚 End Session & See Summary"):
        st.session_state.session_ended = True
        st.rerun()

def _render_session_summary():
    """Displays the final performance summary."""
    engine = st.session_state.interview_engine
    st.header("Session Summary")
    with st.spinner("✍️ Generating your performance summary..."):
        summary = engine.get_session_summary(st.session_state.chat_history)
        st.markdown(summary)

    if st.button("⬅️ Start a New Round"):
        # Reset state
        st.session_state.selected_round = None
        st.session_state.session_ended = False
        st.session_state.interview_engine = None
        st.session_state.chat_history = []
        st.session_state.current_question = None
        st.rerun()