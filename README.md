# Excel QA Agent

This small project refactors your notebook into a structured package and provides a Streamlit UI to ask questions about the sales and forecast Excel files.

Files added:
- `agent_app/loader.py` — loads Excel files into pandas DataFrames.
- `agent_app/agent.py` — initializes a pandas dataframe agent using LangChain and Google Generative AI.
- `streamlit_app.py` — Streamlit app to initialize the agent and ask questions.
- `requirements.txt` — suggested Python dependencies.

How to run:
1. Create a virtual environment and install the requirements.
2. From the workspace root run:

```bash
streamlit run streamlit_app.py
```

Notes:
- The app tries to read `Assignment/data.xlsx` and `Assignment/Forcast.xlsx` by default.
- Set your `GOOGLE_API_KEY` in the sidebar before initializing the agent.
