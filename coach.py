import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
from datetime import datetime
from prompts import SYSTEM_PROMPT, SUMMARY_PROMPT
from knowledge import KNOWLEDGE_BASE, find_tips
from safeguards import check_reply, check_summary, offline_reply