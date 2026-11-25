# wca-ai-tool-s12-DAS-LABS
# Pesa Coach: an AI money coach for M-Pesa users

Pesa Coach is a chat assistant that helps people in Kenya keep track of their spending. You tell it what you spent ("I spent 200 on matatu"), and it sorts each expense into a category, keeps running totals, answers questions about your spending, and gives you saving tips at the end of the session.

It runs in two ways from the same code:

- **Terminal version:** `python coach.py`
- **Browser version:** `streamlit run app.py`

Built for WeCan Academy, Season 12 (AI module project).

---

## 1. What the project does

| Feature | What it means | Where it lives |
|---|---|---|
| Structured prompt (RTCCO) | The coach's instructions are split into Role, Task, Context, Constraints and Output | `prompts.py` |
| Conversation memory | Earlier messages are sent back to the AI each turn, so it remembers what you spent | `coach.py`, `app.py` |
| RAG (retrieval) | The app looks up saving tips that match your message and gives them to the AI | `knowledge.py` |
| JSON output and validation | The AI must reply in JSON, and the app checks the reply before using it | `safeguards.py`, `coach.py` |
| Retry | If a reply is invalid, the app asks once more | `coach.py` |
| Offline fallback | If the AI cannot be reached, the app answers from the last saved totals | `safeguards.py` |
| Session summary | At the end, the AI summarises spending and gives three ways to save | `coach.py`, `app.py` |
| Saved sessions | Each session is saved to a file and can be reopened (terminal menu) | `coach.py` |

---

## 2. Project structure

```
Mpesa_Coach/
|-- coach.py          Gemini calls, terminal chat, saved-session menu
|-- app.py            Streamlit (browser) version of the chat
|-- prompts.py        The RTCCO prompts (chat prompt and summary prompt)
|-- knowledge.py      The RAG tip list and the find_tips() function
|-- safeguards.py     check_reply, check_summary, offline_reply
|-- requirements.txt  Libraries to install
|-- .gitignore        Files Git must not upload (.env, venv/, sessions/, __pycache__/)
|-- .env              Your API key (never committed to Git)
|-- cache.json        Created automatically: the last saved totals
|-- sessions/         Created automatically: one JSON file per session
```

### Who explains what

| File | Owner |
|---|---|
| `prompts.py` and `knowledge.py` | Debby |
| `safeguards.py` | Aggrey |
| `coach.py` and `app.py` | Oba |

Every team member should be able to explain the whole flow in section 3, and their own files in detail.

---

## 3. How it works (the whole story in 30 seconds)

1. The user types an expense, for example `I spent 200 on matatu`.
2. `find_tips()` in `knowledge.py` checks the message for keywords (like "matatu") and picks up to two matching saving tips. This is the **retrieval** step of RAG.
3. The tips are added to the prompt as extra text. This is the **augmentation** step.
4. `get_valid_reply()` in `coach.py` sends the whole conversation, plus the system prompt from `prompts.py`, to Gemini and asks for a JSON reply.
5. `check_reply()` in `safeguards.py` checks that the JSON has a `reply`, a `total_spent` and `totals`. If it does not, the app tries once more.
6. A valid reply is shown to the user, added to the conversation history (the memory), and saved to `cache.json`.
7. If the AI cannot be reached (for example, no internet), `offline_reply()` answers from `cache.json` instead.
8. When the user types `exit` (or clicks **End session and summarise** in the browser), `make_summary()` asks Gemini for a summary, `check_summary()` validates it, and the whole session is saved to `sessions/`.

```
User message
    |
    v
find_tips()  --->  tips added to prompt
    |
    v
Gemini (system prompt + history + tips)
    |
    v
check_reply()  --valid-->  show reply, save to history and cache.json
    |
  invalid (retry once)
    |
  AI unreachable  --->  offline_reply() answers from cache.json
```

---

## 4. The key ideas, file by file

### prompts.py: the RTCCO prompt

RTCCO stands for **R**ole, **T**ask, **C**ontext, **C**onstraints, **O**utput. Splitting the prompt this way keeps each instruction clear and easy to change.

| Part | What it tells the AI |
|---|---|
| Role | Who it is: Pesa Coach, a friendly money coach for people in Kenya |
| Task | Sort each expense into a category, keep running totals, answer questions |
| Context | The user is in Kenya, uses KES, and the chat has several turns |
| Constraints | Only talk about spending, never invent an amount, ask if an amount is missing, keep replies short |
| Output | Reply only with JSON using exact field names |

There are two prompts: `SYSTEM_PROMPT` for the chat, and `SUMMARY_PROMPT` for the end-of-session summary.

### knowledge.py: RAG

`KNOWLEDGE_BASE` is a list of saving tips, each with keywords. `find_tips(user_text)` loops through the list and returns the tips whose keywords appear in the user's message (at most two). The tips are then added to the prompt so the AI uses real, local advice and does not invent its own.

To add a tip, add one more entry to `KNOWLEDGE_BASE` with a list of `keywords` and a `tip`.

### safeguards.py: checks and the offline fallback

- `check_reply(data)` returns `True` only if the reply is a dictionary with a non-empty `reply`, a numeric `total_spent`, and a `totals` dictionary.
- `check_summary(data)` returns `True` only if the summary has `summary`, `breakdown`, `total_spent`, and exactly three `ways_to_save`.
- `offline_reply(user_text)` reads `cache.json` and answers from the last saved totals. It cannot record new expenses while offline.

### coach.py: the engine and the terminal app

- `get_valid_reply(history, extra)` calls Gemini and retries once if the reply is invalid.
- `make_summary(history)` makes the final summary call.
- `new_session()` runs the chat loop and saves the session.
- `open_past_session()` lists saved sessions and displays the one you pick.
- `main_menu()` shows the menu: new session, open a past session, exit.

### app.py: the browser version

Uses Streamlit. It reuses the same functions as the terminal version and keeps the conversation in `st.session_state`, because Streamlit re-runs the file on every click. The sidebar has buttons to end the session and summarise, and to start a new session.

---

## 5. Setup

You need Python 3 and a Gemini API key.

1. **Get the code**

   ```
   git clone <your-repository-url>
   cd <the-repository-folder>
   ```

2. **Create and activate a virtual environment (Windows PowerShell)**

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   Your prompt should now start with `(venv)`. If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` first.

3. **Install the libraries**

   ```
   pip install -r requirements.txt
   ```

   This installs `google-genai`, `python-dotenv` and `streamlit`.

4. **Add your API key.** Create a file named `.env` in the project folder with one line:

   ```
   API_KEY=your-own-key-here
   ```

   Use your own key. Never commit `.env` or share your key. It should be listed in `.gitignore`.

---

## 6. Running the project

**Terminal version**

```
python coach.py
```

Menu: `1` start a new session, `2` open a past session, `3` exit. In a session, type `exit` to finish and get your summary.

**Browser version**

```
streamlit run app.py
```

Open the address shown in the terminal (usually `http://localhost:8501`). Use the chat box at the bottom, then click **End session and summarise** in the sidebar.

---

## 7. Example (what to expect)

```
You: I spent 200 on matatu
[Knowledge base] Tips used: ['Fares often rise at peak hours ...']
Logged KES 200 under transport. Total so far: KES 200.

You: exit
Session ended.
writing your summary...

--- Session summary ---
(2 or 3 sentences)
Total spent: KES 200
- transport: 200
Ways to save:
* (three practical tips)
Session saved to sessions/session_<date>_<time>.json
```

The exact wording will differ because the AI writes the reply.

---

## 8. Testing checklist

Run these to confirm everything works:

1. **Normal chat:** type `I spent 200 on matatu`, then `I spent 150 on lunch`. Totals should add up.
2. **Memory:** ask `how much have I spent on food?`. The coach should remember the earlier messages.
3. **RAG:** the terminal prints the tips used. Messages with "matatu" or "lunch" should show a tip.
4. **Out-of-scope message:** ask something unrelated, like `write me a poem`. The coach should steer back to spending politely.
5. **Summary:** type `exit`. You should get a summary, a breakdown, and three ways to save.
6. **Saved session:** choose option 2 in the terminal menu and open the session you just saved.
7. **Offline:** turn off the internet, start a session, and ask `how much on food`. You should get an answer from the saved totals.

---

## 9. Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `ModuleNotFoundError: No module named 'google'` | The virtual environment is not active. Run `venv\Scripts\activate` and check for `(venv)` in the prompt |
| `ModuleNotFoundError: No module named 'prompts'` | The file is missing or misnamed (for example `prompts,py` with a comma). Check with `dir *.py` |
| `ImportError: cannot import name ...` | The file exists but is empty or missing that item. Check the file has content and is saved |
| `Key lost` is printed | `.env` is missing or does not contain `API_KEY=...` |
| `getaddrinfo failed` or "could not reach the AI" | No internet. The offline fallback should answer from saved totals |
| `503 UNAVAILABLE` / "high demand" | Google's servers are busy. Wait a minute and try again |
| Summary fails ("could not create a summary") | Usually a temporary AI error. Try again |
| Git pull shows nothing new | The teammate has not pushed yet. Ask them to click **Push origin** in GitHub Desktop |

---

## 10. Known limits

- **Offline mode is limited.** `cache.json` only stores the totals from the last reply, so offline answers are only as current as your last online message. It cannot record new expenses.
- **The coach is not a financial advisor.** It gives general saving tips based on what the user reports, and it only knows what the user tells it.
- **RAG is keyword matching.** It picks tips whose keywords appear in the message, so it can miss tips that use different words.
- **Saved sessions:** the terminal version has a menu to reopen past sessions. The browser version saves sessions but does not yet have a viewer for them.
- **Local data only.** Everything is stored in files on your own computer.

---

## 11. Team

| Name | Files |
|---|---|
| Oba Sawa | `coach.py`, `app.py` |
| Debby | `prompts.py`, `knowledge.py` |
| Aggrey | `safeguards.py` |
