# 🧠 Behavioral Intelligence Analyst

An agentic conversational system where you describe your customer or user behavior in natural language and receive intelligent behavioral analysis back.

Built with **Streamlit** and powered by **LLaMA 3.3 70B** via **Groq**.

---

## How It Works

The system uses two AI agents working in sequence:

| Agent | Role |
|---|---|
| **Clarifier Agent** | Evaluates if your query has enough detail. If it's too vague, it asks exactly ONE focused clarifying question before proceeding. |
| **Analyst Agent** | Takes your query (plus any clarification) and returns a structured analysis covering user segmentation, risk flags, and actionable recommendations. |

### Conversation Flow

```
User types query
      ↓
Clarifier Agent checks if query is sufficient
      ↓
If vague  → asks ONE clarifying question → waits for response → passes both to Analyst
If clear  → passes directly to Analyst Agent
      ↓
Analyst Agent returns structured analysis
      ↓
System suggests a follow-up question
```

---

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/behavioral-intelligence-analyst.git
cd behavioral-intelligence-analyst
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your Groq API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_key_here` with your actual [Groq API key](https://console.groq.com/keys).

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deploy on Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Select **Streamlit** as the SDK.
3. Upload the following files to the Space:
   - `app.py`
   - `agents.py`
   - `requirements.txt`
4. Add your `GROQ_API_KEY` as a **Secret** in the Space settings (Settings → Repository secrets).
5. The Space will automatically build and deploy.

---

## File Structure

```
├── app.py              # Main Streamlit application
├── agents.py           # Clarifier Agent and Analyst Agent logic
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # This file
```

---

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: LLaMA 3.3 70B Versatile (via Groq)
- **API**: Groq Python SDK (direct calls, no LangChain)

---

## License

MIT