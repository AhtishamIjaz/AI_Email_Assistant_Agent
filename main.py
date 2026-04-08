from src.gmail_service import (
    get_gmail_service, 
    fetch_unread_emails, 
    get_email_details, 
    create_gmail_draft
)
from src.graph import email_processor
from utils.logger import logger

def run_agentic_workflow():
    logger.info("--- Starting Universal Drafter (Human-in-the-Loop) ---")
    
    service = get_gmail_service()
    if not service: return

    unread_messages = fetch_unread_emails(service)
    if not unread_messages:
        logger.info("Inbox is clean.")
        return

    # Process latest unread emails
    for msg in unread_messages[:20]: # Start with 20 to test speed
        msg_id = msg['id']
        email_body = get_email_details(service, msg_id)
        
        if not email_body: continue

        # Pass to the AI Graph (Sorter -> Drafter -> Critic)
        initial_state = {"email_content": email_body}
        result = email_processor.invoke(initial_state)

        final_text = result.get('final_email')

        # ACTION: Create draft for EVERY email processed
        if final_text and final_text != "Error":
            logger.info(f"Creating draft for message: {msg_id}")
            create_gmail_draft(service, final_text, msg_id)
        else:
            logger.warning(f"Could not generate draft for {msg_id}")

    print("\n✅ All unread emails now have drafts waiting in your Gmail!")

if __name__ == "__main__":
    run_agentic_workflow()