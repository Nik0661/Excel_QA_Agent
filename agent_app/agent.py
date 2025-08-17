from typing import List, Optional
import os

# Lazy import heavy dependencies so module can be imported for tests without them installed.

def initialize_agent(df_list: List[Optional[object]], api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
    """Initializes and returns a pandas dataframe agent using langchain.

    This function does lazy imports to avoid import-time failures when dependencies are missing.
    Returns the agent instance or None if it cannot be created.
    """
    if all(df is None for df in df_list):
        return None

    try:
        # Lazy imports
        from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
        from langchain_google_genai import GoogleGenerativeAI
    except Exception as e:
        raise RuntimeError("Required langchain or google-genai packages are not available: " + str(e))

    if api_key:
        os.environ.setdefault("GOOGLE_API_KEY", api_key)

    llm = GoogleGenerativeAI(model=model)

    agent = create_pandas_dataframe_agent(
        llm,
        df_list,
        verbose=False,
        handle_parsing_errors=True,
        allow_dangerous_code=True
    )

    return agent
