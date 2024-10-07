import streamlit as st
import json
from modules.api_key_utils import get_google_api_key
from modules.llm_pipeline import setup_pipeline
from modules.ui_components import display_feedback
from cryptography.fernet import Fernet

# Define paths to the encrypted JSON files
TASK_1_ACADEMIC_CRITERIA_PATH = (
    "tasks/Academic_IELTS_Writing_Task_1_Band_Descriptors.json.enc"
)
TASK_1_GENERAL_TRAINING_CRITERIA_PATH = (
    "tasks/General_Training_IELTS_Writing_Task_1_Band_Descriptors.json.enc"
)
TASK_2_CRITERIA_PATH = "tasks/IELTS_Writing_Task_2_Band_Descriptors.json.enc"


def load_encrypted_json(file_path, key):
    """Load and decrypt an encrypted JSON file using the provided key."""
    # Initialize Fernet with the given key
    cipher = Fernet(key)

    # Read and decrypt the encrypted file
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data).decode()

    # Load the decrypted JSON content
    return json.loads(decrypted_data)


def load_criteria(task_type):
    """Load the evaluation criteria based on the selected task type."""
    # Fetch the encryption key from Streamlit secrets
    encryption_key = st.secrets["encryption_key"].encode()

    # Select the appropriate file path
    if task_type == "Task 1 Academic":
        file_path = TASK_1_ACADEMIC_CRITERIA_PATH
    elif task_type == "Task 1 General Training":
        file_path = TASK_1_GENERAL_TRAINING_CRITERIA_PATH
    elif task_type == "Task 2":
        file_path = TASK_2_CRITERIA_PATH

    # Load and decrypt the JSON file
    return load_encrypted_json(file_path, encryption_key)


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
    if "word_count" not in st.session_state:
        st.session_state["word_count"] = 0  # Track the word count of the user response


def reset_state():
    """Reset session state variables to start over."""
    st.session_state["task_type"] = None
    st.session_state["ielts_question"] = ""
    st.session_state["user_response"] = ""
    st.session_state["step"] = 1
    st.session_state["feedback_ready"] = False
    st.session_state["word_count"] = 0


def main():
    # Set up Streamlit configuration
    st.set_page_config(
        page_title="IELTSEvaL - Your AI Writing Evaluator", page_icon="✍️"
    )

    # Initialize session state variables
    initialize_session_state()

    # Step 1: Task Selection and Introduction
    if st.session_state["step"] == 1:
        st.title("✨ IELTSEvaL: Your AI-Powered Writing Evaluator")

        st.header("Why Use IELTSEvaL?")
        st.write(
            """
            Getting your IELTS Writing tasks assessed can be expensive, with some services charging over $50 for just one evaluation! 💸  
            That's why we created IELTSEvaL: to provide a **cost-effective, AI-powered evaluation tool** that gives you **detailed feedback** on your writing,  
            so you can **improve your skills** and **boost your score** — all for free!
            """
        )

        st.subheader("How It Works:")
        st.write(
            """
            1. **Select the IELTS Writing Task** (Task 1 Academic, Task 1 General Training, or Task 2).
            2. **Enter the Task Question** (e.g., "Describe the process of making coffee.") and then **your response**.
            3. Click **"Evaluate Response"** to receive detailed feedback on each criterion — including **Task Response**, **Coherence & Cohesion**, **Lexical Resource**, and **Grammatical Range & Accuracy**.
            4. **Review your feedback** and see what to improve!
            """
        )

        st.caption(
            "**Please Note**: This app is *not* affiliated with the official IELTS organization. It is designed as a supportive tool for self-evaluation and improvement."
        )

        st.divider()

        # Task selection using radio buttons
        st.subheader("Select the IELTS Writing Task to Evaluate 👇")
        task_type = st.radio(
            "Choose a Task",
            options=[
                "Task 1 Academic ✏️",
                "Task 1 General Training ✏️",
                "Task 2 Writing 📝",
            ],
            index=0,
        )

        # "Next" button to confirm selection
        if st.button("Next"):
            if task_type == "Task 1 Academic ✏️":
                st.session_state["task_type"] = "Task 1 Academic"
            elif task_type == "Task 1 General Training ✏️":
                st.session_state["task_type"] = "Task 1 General Training"
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

        # Define the minimum word count based on the task type
        if st.session_state["task_type"] == "Task 2":
            min_word_count = 250
        else:
            min_word_count = 150

        # User response input
        st.session_state["user_response"] = st.text_area(
            f"✍️ Enter your response to the above IELTS {st.session_state['task_type']} question here",
            value=st.session_state["user_response"],
            height=300,
            help="Provide your detailed response to the question above.",
        )

        # Button to check word count
        if st.button("Check Word Count"):
            # Calculate the word count and store it
            word_count = len(st.session_state["user_response"].split())
            st.session_state["word_count"] = word_count
            st.write(f"**Word Count**: {word_count}")

        # Error messages above the Evaluate button
        if (
            st.session_state["user_response"].strip()
            and len(st.session_state["user_response"].split()) < min_word_count
        ):
            st.warning(
                f"Your response must be at least {min_word_count} words. You currently have {st.session_state['word_count']} words."
            )

        # Button to evaluate the response
        if st.button("Evaluate Response 🚀"):
            # Ensure both question and response are provided
            if (
                not st.session_state["ielts_question"].strip()
                or not st.session_state["user_response"].strip()
            ):
                st.error(
                    "Please enter both the question and your response for evaluation."
                )
            elif len(st.session_state["user_response"].split()) < min_word_count:
                st.error(
                    f"Your response must be at least {min_word_count} words before you can proceed."
                )
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

            with st.spinner(
                f"Evaluating your {st.session_state['task_type']} response..."
            ):
                # Pass the question, response, and word count to the LLM
                combined_result = combined_chain.run(
                    {
                        "question": st.session_state["ielts_question"],
                        "response": st.session_state["user_response"],
                        "word_count": st.session_state["word_count"],
                    }
                )

                # Store the generated feedback in session state
                st.session_state["generated_feedback"] = combined_result
                st.session_state["feedback_ready"] = True

                # Display the feedback using markdown for better formatting
                st.subheader("📈 Detailed Feedback")
                st.markdown(
                    st.session_state.get(
                        "generated_feedback", "Feedback is not available."
                    ),
                    unsafe_allow_html=True,
                )
        else:
            st.error("Google API key is required to evaluate the response.")

        # Start Over button to reset the app
        if st.button("Start Over 🔄"):
            reset_state()
            st.rerun()


if __name__ == "__main__":
    main()
