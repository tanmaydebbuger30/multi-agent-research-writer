import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # reads .env into environment variables

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "2"))
USE_WEB_SEARCH = os.getenv("USE_WEB_SEARCH", "1") == "1"

llm = ChatOpenAI(model=MODEL, temperature=0.4, use_responses_api=True)