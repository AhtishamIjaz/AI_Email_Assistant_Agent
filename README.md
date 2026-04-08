# 🤖 AI Email Assistant Agent

A professional, autonomous email management system built with **LangGraph**, **Groq (Llama 3)**, and **Docker**, deployed on **AWS**.

## 🚀 Overview
This agent monitors an inbox for unread emails, analyzes their intent, and generates high-quality drafts. It features a **Human-in-the-Loop** mechanism, allowing users to review and edit AI-generated responses before they are saved to Gmail.

## 🧠 Technical Architecture
- **Agentic Logic:** Built with **LangGraph** using a modular multi-agent approach (Sorter, Drafter, and Critic).
- **LLM:** Powered by **Groq (Llama-3.3-70b)** for ultra-fast, stateful reasoning.
- **Frontend:** Interactive **Streamlit** dashboard for human review and control.
- **Deployment:** Containerized with **Docker**, stored in **AWS ECR**, and hosted on **AWS EC2**.

## 🛠️ Tech Stack
* **Language:** Python
* **Frameworks:** LangChain, LangGraph, Streamlit
* **Infrastructure:** AWS (EC2, ECR), Docker
* **API:** Gmail API, Groq Cloud

## 📖 How it Works
1. **Fetch:** Retrieves unread emails via Gmail API.
2. **Sort:** AI identifies if the email is a Meeting, Question, or Notification.
3. **Draft:** Generates a professional reply based on the category.
4. **Reflect:** A 'Critic Agent' reviews the draft for tone and grammar.
5. **Human Review:** The user approves or edits the draft in the UI.
6. **Execute:** The final version is saved as a Gmail Draft.

## 🏠 Local Setup
1. Clone the repo.
2. Create a `.env` file with `GROQ_API_KEY`.
3. Place your `credentials.json` in the root.
4. Run:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   streamlit run app.py