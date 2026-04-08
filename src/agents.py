import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from utils.logger import logger

# Load environment variables (API Keys)
load_dotenv()

def get_model():
    """Initializes and returns the Groq Llama 3 model."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("CRITICAL: GROQ_API_KEY not found in .env file!")
        return None
    
    # Using Llama 3 70B for high-quality reasoning
    return ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=api_key,
        temperature=0.1  # Low temperature for consistent, factual results
    )

def email_sorter_agent(email_content: str):
    model = get_model()
    if not model: return "General"

    prompt = f"""
    You are a Personal Assistant. Analyze the email content below.
    Determine the primary intent (e.g., Question, Meeting, Notification, Personal).
    
    Email Content:
    {email_content}
    
    Respond with ONLY the one-word intent.
    """
    
    try:
        logger.info("Sorter is identifying intent...")
        response = model.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        logger.error(f"Sorter failed: {e}")
        return "General"

def email_drafter_agent(category: str, email_content: str):
    model = get_model()
    if not model: return "Error"

    prompt = f"""
    You are a professional assistant writing a draft for a human to review.
    Original Email: {email_content}
    
    Task: Write a reply that fits the intent: {category}.
    - If the email is a system notification, write a draft acknowledging it or asking for more info.
    - If it's a person, be polite and helpful.
    - ALWAYS include [Your Name] at the end.
    - Write only the body of the email.
    """
    
    try:
        logger.info("Drafter Agent is generating a response...")
        response = model.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        logger.error(f"Drafter Agent failed: {e}")
        return "Error"

def email_critic_agent(draft_content: str):
    """
    Step 3: Reviews the draft to ensure high quality before sending.
    """
    model = get_model()
    if not model: return draft_content

    prompt = f"""
    You are a Senior Communications Editor. 
    Review the following email draft for grammar, professional tone, and clarity.
    
    Draft:
    {draft_content}
    
    If the draft is already perfect, return it exactly as is.
    If it needs improvement, return ONLY the improved version.
    """
    
    try:
        logger.info("Critic Agent is performing final review...")
        response = model.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        logger.error(f"Critic Agent failed: {e}")
        return draft_content # Safety: return original draft if critic fails