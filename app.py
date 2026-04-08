import streamlit as st
from src.gmail_service import get_gmail_service, fetch_unread_emails, get_email_details, create_gmail_draft
from src.graph import email_processor
import time

# --- Page Configuration ---
st.set_page_config(page_title="Agentic Email Executive", page_icon="📬", layout="wide")

st.title("📬 Agentic Email Executive")
st.markdown("Automate your inbox with a Human-in-the-Loop AI workflow.")

# --- Session State Management ---
# This keeps data alive while you click buttons
if 'service' not in st.session_state:
    st.session_state.service = get_gmail_service()
if 'emails' not in st.session_state:
    st.session_state.emails = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# --- Sidebar: Control Panel ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Sync Latest Emails", use_container_width=True):
        with st.spinner("Fetching unread emails..."):
            st.session_state.emails = fetch_unread_emails(st.session_state.service)[:10] # Top 10 for speed
            st.success(f"Found {len(st.session_state.emails)} emails!")

# --- Main Layout: Two Columns ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Inbox Queue")
    if not st.session_state.emails:
        st.info("No emails synced yet. Click 'Sync' in the sidebar.")
    
    for email in st.session_state.emails:
        with st.expander(f"✉️ ID: {email['id']}"):
            st.write(f"**Preview:** {email.get('snippet', 'No snippet available')}")
            if st.button("🧠 Analyze & Draft", key=f"btn_{email['id']}"):
                # 1. Real-Time Status Tracking
                status_placeholder = st.empty()
                with status_placeholder.container():
                    st.write("🔍 **Step 1:** Fetching full content...")
                    full_content = get_email_details(st.session_state.service, email['id'])
                    
                    st.write("🧠 **Step 2:** Running Agentic Sorter...")
                    time.sleep(0.5) # For visual effect
                    
                    st.write("✍️ **Step 3:** Generating & Critiquing Draft...")
                    result = email_processor.invoke({"email_content": full_content})
                    
                    # Store result in state for the editor
                    st.session_state.current_analysis = {
                        "id": email['id'],
                        "content": full_content,
                        "category": result.get('category'),
                        "draft": result.get('final_email'),
                        "logs": result # Full dict for logs
                    }
                    st.success("Draft Ready for Review!")

with col2:
    st.subheader("✍️ Human-in-the-Loop Editor")
    
    if st.session_state.current_analysis:
        analysis = st.session_state.current_analysis
        
        # 2. The Editor View
        st.info(f"**AI Intent Detection:** {analysis['category']}")
        
        # This is where the human edits the AI's work
        edited_draft = st.text_area(
            "Final Draft (Edit as needed):", 
            value=analysis['draft'], 
            height=300
        )
        
        if st.button("🚀 Push to Gmail Drafts", type="primary"):
            with st.spinner("Saving to Gmail..."):
                create_gmail_draft(st.session_state.service, edited_draft, analysis['id'])
                st.balloons()
                st.success("Draft successfully created in your Gmail!")

        # 3. Agentic Logs View (Chain of Thought)
        with st.expander("📝 View Agentic Logs (Chain of Thought)"):
            st.json(analysis['logs'])
    else:
        st.write("Select an email from the left to start the AI workflow.")

st.markdown("---")
st.caption("AI Email Agent v2.0 - Built with LangGraph & Streamlit")