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

def main():
    # Set up Streamlit configuration
    st.set_page_config(page_title="IELTS Writing Task Evaluator", page_icon="✍️")

    # Initialize session state variables
    initialize_session_state()

    st.title("IELTS Writing Task Evaluator")
    st.subheader("Assess your IELTS Writing Task 1 or Task 2")

    # Task selection buttons
    st.write("### Select the IELTS Writing Task to Evaluate")
    col1, col2 = st.columns(2)

    # Handle task selection and store it in session state
    with col1:
        if st.button("Task 1 Writing"):
            st.session_state["task_type"] = "Task 1"

    with col2:
        if st.button("Task 2 Writing"):
            st.session_state["task_type"] = "Task 2"

    # Check if a task has been selected
    if st.session_state["task_type"]:
        task_type = st.session_state["task_type"]
        st.success(f"You selected {task_type}. Please enter your question and response below.")

        # Step 1: Ask the user to input the question they are answering
        st.session_state["ielts_question"] = st.text_area(
            "📋 Enter the IELTS Task Question (e.g., 'Describe the process of making coffee.')",
            value=st.session_state["ielts_question"],
            height=100,
            key="question_input",
        )

        # Step 2: Ask the user to input their response to the given question
        st.session_state["user_response"] = st.text_area(
            f"✍️ Enter your response to the above IELTS {task_type} question here",
            value=st.session_state["user_response"],
            height=300,
            key="response_input",
        )

        # Button to evaluate the response
        if st.button("Evaluate Response"):
            # Ensure both question and response are provided
            if not st.session_state["ielts_question"].strip() or not st.session_state["user_response"].strip():
                st.error("Please enter both the question and your response for evaluation.")
            else:
                st.success(f"Evaluating your {task_type} response based on the context of the question...")

                # Load the Google API key for the LLM pipeline
                google_api_key = get_google_api_key()

                if google_api_key:
                    # Set up the combined LLM pipeline for feedback and scoring
                    combined_chain = setup_pipeline(google_api_key)

                    with st.spinner(f"Evaluating your {task_type} response..."):
                        # Pass the question and response through the combined pipeline
                        combined_result = combined_chain.run(
                            {"question": st.session_state["ielts_question"], "response": st.session_state["user_response"]}
                        )

                        # Display the combined feedback and score
                        display_feedback(combined_result)

                else:
                    st.error("Google API key is required to evaluate the response.")

    else:
        st.info("Please select either 'Task 1 Writing' or 'Task 2 Writing' to get started.")

if __name__ == "__main__":
    main()