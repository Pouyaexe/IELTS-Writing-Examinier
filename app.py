import streamlit as st
import json

# Import existing modules or pipelines (assuming they are defined elsewhere)
from modules.api_key_utils import get_google_api_key
from modules.llm_pipeline import setup_pipeline
from modules.ui_components import display_feedback, display_score

def load_criteria(task_type):
    """Load the evaluation criteria based on the selected task type."""
    if task_type == "Task 1":
        with open("/mnt/data/IELTS_Writing_Task_1_Band_Descriptors.json", "r") as file:
            return json.load(file)
    else:
        with open("/mnt/data/IELTS_Writing_Task_2_Band_Descriptors.json", "r") as file:
            return json.load(file)

def main():
    # Set up Streamlit configuration
    st.set_page_config(page_title="IELTS Writing Evaluator", page_icon="✍️")

    st.title("IELTS Writing Task Evaluator")
    st.subheader("Assess your IELTS Writing Task 1 or Task 2")

    # Sidebar for task selection
    task_type = st.sidebar.selectbox("Select Task Type", ["Task 1", "Task 2"])

    # Load criteria for the selected task
    criteria = load_criteria(task_type)

    # Step 1: Ask the user to input the question they are answering
    ielts_question = st.text_area(
        "📋 Enter the IELTS Task Question (e.g., 'Describe the process of making coffee.')", height=100
    )

    # Step 2: Ask the user to input their response to the given question
    user_response = st.text_area(
        f"✍️ Enter your response to the above IELTS {task_type} question here", height=300
    )

    # Button to evaluate the response
    if st.button("Evaluate Response"):
        if not ielts_question.strip() or not user_response.strip():
            st.error("Please enter both the question and your response for evaluation.")
        else:
            st.success(f"Evaluating your {task_type} response based on the context of the question...")

            # Load the Google API key for the LLM pipeline
            google_api_key = get_google_api_key()

            if google_api_key:
                # Set up LLM pipeline with question and answer
                feedback_chain, score_chain = setup_pipeline(google_api_key)

                with st.spinner(f"Evaluating your {task_type} response..."):
                    # Pass the question and response through the pipeline
                    feedback = feedback_chain.run(
                        {"question": ielts_question, "response": user_response, "criteria": criteria}
                    )
                    score = score_chain.run(
                        {"question": ielts_question, "response": user_response, "criteria": criteria}
                    )

                    # Display feedback and score
                    display_feedback(feedback)
                    display_score(score)

            else:
                st.error("Google API key is required to evaluate the response.")

if __name__ == "__main__":
    main()
