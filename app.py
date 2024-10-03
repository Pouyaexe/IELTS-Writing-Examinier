import streamlit as st
import json
from modules.api_key_utils import get_google_api_key
from modules.llm_pipeline import setup_pipeline
from modules.ui_components import display_feedback

# Define the paths to the JSON files
TASK_1_CRITERIA_PATH = "tasks/IELTS_Writing_Task_1_Band_Descriptors.json"
TASK_2_CRITERIA_PATH = "tasks/IELTS_Writing_Task_2_Band_Descriptors.json"

def load_criteria(task_type):
    """Load the evaluation criteria based on the selected task type."""
    file_path = TASK_1_CRITERIA_PATH if task_type == "Task 1" else TASK_2_CRITERIA_PATH
    with open(file_path, "r") as file:
        return json.load(file)

def initialize_session_state():
    """Initialize session state variables."""
    if "task_type" not in st.session_state:
        st.session_state["task_type"] = None
    if "ielts_question" not in st.session_state:
        st.session_state["ielts_question"] = ""
    if "user_response" not in st.session_state:
        st.session_state["user_response"] = ""
    if "step" not in st.session_state:
        st.session_state["step"] = 1  # Track which step the user is on
    if "feedback_ready" not in st.session_state:
        st.session_state["feedback_ready"] = False  # Track if feedback is ready

def reset_state():
    """Reset session state variables to start over."""
    st.session_state["task_type"] = None
    st.session_state["ielts_question"] = ""
    st.session_state["user_response"] = ""
    st.session_state["step"] = 1
    st.session_state["feedback_ready"] = False

def main():
    # Set up Streamlit configuration
    st.set_page_config(page_title="IELTS Writing Task Evaluator", page_icon="✍️")

    # Initialize session state variables
    initialize_session_state()

    # Step 1: Task Selection
    if st.session_state["step"] == 1:
        st.title("✍️ IELTS Writing Task Evaluator")
        st.header("Welcome to the IELTS Writing Task Evaluator! 🎉")

        st.subheader(
            """
            This app is designed to help you assess your IELTS Writing responses for both Task 1 and Task 2.
            Using AI-based evaluation, it provides detailed feedback on key criteria such as **Task Response, Coherence & Cohesion, Lexical Resource**, and **Grammatical Range & Accuracy**.
            """
        )
        st.caption("**Please Note**: This app is *not* affiliated with the official IELTS organization. It is designed as a supportive tool for self-evaluation and improvement.")

        st.divider()

        # Task selection using radio buttons
        st.subheader("Select the IELTS Writing Task to Evaluate 👇")
        task_type = st.radio("Choose a Task", options=["Task 1 Writing ✏️", "Task 2 Writing 📝"], index=0)

        # "Next" button to confirm selection
        if st.button("Next"):
            if task_type == "Task 1 Writing ✏️":
                st.session_state["task_type"] = "Task 1"
            elif task_type == "Task 2 Writing 📝":
                st.session_state["task_type"] = "Task 2"
            st.session_state["step"] = 2  # Move to the next step
            st.rerun()  # Trigger immediate rerun to update UI

    # Step 2: Enter Question and Response
    elif st.session_state["step"] == 2:
        st.header(f"You selected {st.session_state['task_type']}")

        # Back button to go back to task selection
        if st.button("⬅️ Back"):
            st.session_state["step"] = 1
            st.rerun()  # Trigger immediate rerun to update UI

        # Input boxes for question and response
        st.session_state["ielts_question"] = st.text_area(
            "📋 Enter the IELTS Task Question",
            value=st.session_state["ielts_question"],
            height=100,
            help="Type the question or task description for your IELTS writing task (e.g., 'Describe the process of making coffee.')",
        )

        st.session_state["user_response"] = st.text_area(
            f"✍️ Enter your response to the above IELTS {st.session_state['task_type']} question here",
            value=st.session_state["user_response"],
            height=300,
            help="Provide your detailed response to the question above.",
        )

        # Button to evaluate the response
        if st.button("Evaluate Response 🚀"):
            # Ensure both question and response are provided
            if not st.session_state["ielts_question"].strip() or not st.session_state["user_response"].strip():
                st.error("Please enter both the question and your response for evaluation.")
            else:
                st.session_state["step"] = 3  # Move to the feedback step
                st.rerun()  # Trigger immediate rerun to update UI

    # Step 3: Display Feedback
    elif st.session_state["step"] == 3:
        st.header("📝 Your Feedback is Ready!")

        # Load the Google API key for the LLM pipeline
        google_api_key = get_google_api_key()

        if google_api_key:
            # Set up the combined LLM pipeline for feedback and scoring
            combined_chain = setup_pipeline(google_api_key)

            with st.spinner(f"Evaluating your {st.session_state['task_type']} response..."):
                # Pass the question and response through the combined pipeline
                combined_result = combined_chain.run(
                    {"question": st.session_state["ielts_question"], "response": st.session_state["user_response"]}
                )

                # Store the generated feedback in session state
                st.session_state["generated_feedback"] = combined_result
                st.session_state["feedback_ready"] = True

                # Display the feedback using markdown for better formatting
                st.subheader("📈 Detailed Feedback")
                st.markdown(st.session_state.get("generated_feedback", "Feedback is not available."), unsafe_allow_html=True)
        else:
            st.error("Google API key is required to evaluate the response.")

        # Start Over button to reset the app
        if st.button("Start Over 🔄"):
            reset_state()
            st.rerun()


if __name__ == "__main__":
    main()
