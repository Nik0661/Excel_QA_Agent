import streamlit as st
from agent_app.loader import load_data, clear_cache
from agent_app.agent import initialize_agent

st.set_page_config(page_title="Excel QA Agent", layout="wide")

st.title("Excel QA Agent — Streamlit UI")

st.sidebar.header("Configuration")
# API key should come from the sidebar or environment, never hard-coded
api_key = st.sidebar.text_input("Google API Key", type="password")
model = st.sidebar.text_input("Model", value="gemini-2.5-flash")

st.sidebar.markdown("Using the default Excel files in the `Assignment/` folder.")

# Load data (cached by loader)
df_sales, df_forecast = load_data()

if df_sales is None and df_forecast is None:
    st.warning("No dataframes available. Place `data.xlsx` and `Forcast.xlsx` inside the `Assignment` folder.")
else:
    # Auto-initialize the agent if not present
    if 'agent' not in st.session_state:
        with st.spinner("Initializing agent..."):
            try:
                agent = initialize_agent([df_sales, df_forecast], api_key=api_key if api_key else None, model=model)
                if agent is None:
                    st.error("Agent could not be created (no data).")
                else:
                    st.session_state['agent'] = agent
                    st.success("Agent initialized.")
            except Exception as e:
                st.error(f"Failed to initialize agent: {e}")

    # Controls: initialize (redundant) and refresh cache
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Re-initialize Agent"):
            try:
                agent = initialize_agent([df_sales, df_forecast], api_key=api_key if api_key else None, model=model)
                if agent is None:
                    st.error("Agent could not be created (no data).")
                else:
                    st.session_state['agent'] = agent
                    st.success("Agent re-initialized.")
            except Exception as e:
                st.error(f"Failed to initialize agent: {e}")
    with col2:
        if st.button("Refresh cache"):
            try:
                clear_cache()
                st.success("Cache cleared. Reload the page to rebuild caches.")
            except Exception as e:
                st.error(f"Failed to clear cache: {e}")

    # Q&A area
    if 'agent' in st.session_state:
        user_question = st.text_input("Ask a question about the data", key="qa_input")
        if st.button("Ask") and user_question:
            agent = st.session_state['agent']
            try:
                with st.spinner("Getting answer..."):
                    answer = agent.invoke(user_question)
                output = answer.get('output') if isinstance(answer, dict) else str(answer)
                st.markdown("**Agent:**")
                st.write(output)
            except Exception as e:
                st.error(f"Agent failed to answer: {e}")
