"""Prints what .env holds, without exposing secrets."""
from dotenv import load_dotenv
import os

load_dotenv()
ua = os.getenv("SEC_USER_AGENT")
key = os.getenv("API_KEY")
print("SEC_USER_AGENT:", ua or "MISSING")
print("PROVIDER:", os.getenv("PROVIDER", "openai (default)"))
print("API_KEY:", (key[:4] + "…") if key else "MISSING")
