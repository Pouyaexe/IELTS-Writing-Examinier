from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import streamlit as st

def setup_pipeline(google_api_key):
    """Set up the LLM chains for combined feedback and scoring in a single call."""

    llm = ChatGoogleGenerativeAI(
        api_key=google_api_key,
        model="gemini-1.5-flash",
        temperature=0.0,  # Set temperature to 0 for consistent results
        max_tokens=1000,
    )

    # Access the prompt template from Streamlit secrets
    combined_prompt_template = st.secrets["prompt_template"]

    # Create the PromptTemplate instance
    combined_prompt = PromptTemplate(
        template=combined_prompt_template,
        input_variables=["question", "response"]
    )

    # Create a single LLMChain for the combined prompt
    combined_chain = LLMChain(
        llm=llm,
        prompt=combined_prompt
    )

    return combined_chain
