from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def setup_pipeline(google_api_key):
    """Set up the LLM chains for combined feedback and scoring in a single call."""
    
    llm = ChatGoogleGenerativeAI(
        api_key=google_api_key,
        model="gemini-1.5-flash",
        temperature=0.0,
        max_tokens=4000,
    )

    # Combined prompt for both feedback and scoring
    combined_prompt_template = """
    You are an IELTS Writing examiner. Evaluate the provided IELTS Writing response in the context of the given question.
    For each of the four criteria below, use the descriptors to assess the response and assign a score between 1 and 9.

    Provide concise feedback for each criterion, focusing only on aspects mentioned in the criteria.

    Criteria to Evaluate:
    1. Task Response (Task Achievement)
    2. Coherence & Cohesion
    3. Lexical Resource
    4. Grammatical Range & Accuracy

    Use the following format:
    - **Task Response**: [Feedback based on criteria, Score out of 9]
    - **Coherence & Cohesion**: [Feedback based on criteria, Score out of 9]
    - **Lexical Resource**: [Feedback based on criteria, Score out of 9]
    - **Grammatical Range & Accuracy**: [Feedback based on criteria, Score out of 9]

    After evaluating all criteria, calculate the average of the four scores and present it as the **final band score**.

    Question:
    {question}

    User Response:
    {response}

    Use only the descriptors provided in the criteria and avoid introducing new interpretations.
    """

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
