from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def setup_pipeline(google_api_key):
    """Set up the LLM chains for feedback and scoring."""

    llm = ChatGoogleGenerativeAI(
        api_key=google_api_key,
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=500,
    )

    # Adjusted feedback prompt to include question context
    feedback_prompt_template = """
    Evaluate the provided IELTS Writing response in the context of the given question. Assess each of the following criteria and provide detailed feedback for each, including areas of improvement.

    Question:
    {question}

    Criteria:
    {criteria}

    User Response:
    {response}

    Feedback:
    """

    # Adjusted score prompt to include question context
    score_prompt_template = """
    Based on the given IELTS Writing question, assign an overall IELTS band score to the response considering the following criteria.

    Question:
    {question}

    Criteria:
    {criteria}

    User Response:
    {response}

    Score:
    """

    feedback_prompt = PromptTemplate(template=feedback_prompt_template, input_variables=["question", "response", "criteria"])
    score_prompt = PromptTemplate(template=score_prompt_template, input_variables=["question", "response", "criteria"])

    # Set up the LLM chains
    feedback_chain = LLMChain(llm=llm, prompt=feedback_prompt)
    score_chain = LLMChain(llm=llm, prompt=score_prompt)

    return feedback_chain, score_chain
