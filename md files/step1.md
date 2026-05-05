# Step 1: Environment Setup & Ollama Installation

> **Goal:** Install Ollama, download the AI model, set up Python virtual environment, and install dependencies.
> **Time Estimate:** 20-30 minutes (mostly waiting for model download)

---

## What You'll Do in This Step

| Task | Status |
|------|--------|
| Install Ollama on your PC | [ ] |
| Download gemma3:4b model (~3 GB) | [ ] |
| Test that the model responds | [ ] |
| Create Python virtual environment | [ ] |
| Install Python dependencies | [ ] |
| Verify everything works | [ ] |

---

## 1.1 Install Ollama

Ollama is the software that runs AI models locally on your machine. No cloud, no API keys, no internet needed after setup.

### Steps:
1. Go to **[ollama.com/download](https://ollama.com/download)**
2. Click **"Download for Windows"**
3. Run the installer (just click Next/Install, nothing special to configure)
4. After installation, **restart your terminal** (close VS Code terminal and open a new one)

### Verify installation:
Open a **new terminal** in VS Code (`Ctrl + ~`) and run:

```powershell
ollama --version
```

**Expected output:** Something like `ollama version 0.6.x` (any version number = success)

**If you get "ollama is not recognized":**
- Close VS Code completely and reopen it
- Or restart your PC
- Ollama adds itself to PATH during install, but terminals opened before installation won't see it

---

## 1.2 Pull the AI Model (gemma3:4b)

This downloads Google's Gemma 3 4B model to your machine. It's a one-time download (~3 GB).

### Why gemma3:4b?
- **Best Hinglish support** — Google's models understand Hindi in Roman script (e.g., "Yeh Parth, tum kaha ho?") better than any other model
- **Lightweight** — Only needs ~6 GB RAM
- **Fast** — Quick responses for dashboard and eventually game integration

### Download the model:

```powershell
ollama pull gemma3:4b
```

**This will take 5-15 minutes** depending on your internet speed. You'll see a progress bar.

### Verify it downloaded:

```powershell
ollama list
```

**Expected output:** You should see `gemma3:4b` in the list with its size.

---

## 1.3 Test the Model

Let's make sure the model can respond before we build anything:

```powershell
ollama run gemma3:4b "Say namaste in Hinglish (Hindi written in English letters)"
```

**Expected:** The model should respond in Hinglish (Hindi words in English/Roman script).

To exit the Ollama chat, type:
```
/bye
```

### Quick Roleplay Test:

```powershell
ollama run gemma3:4b "You are Lord Krishna from Mahabharata. Introduce yourself in Hinglish (Hindi in English letters). Keep it short."
```

**If this works, your AI model is ready!**

---

## 1.4 Set Up Python Virtual Environment

A virtual environment keeps your project's Python packages separate from your system Python. This prevents conflicts.

### Navigate to project folder:

Open terminal in VS Code and make sure you're in the project root:

```powershell
cd "C:\Users\kumar\Pictures\Minor project\chakravyuh-backend"
```

### Create the virtual environment:

```powershell
python -m venv venv
```

This creates a `venv/` folder in your project. It takes a few seconds.

### Activate the virtual environment:

```powershell
.\venv\Scripts\Activate
```

**How to know it's active:** You'll see `(venv)` at the beginning of your terminal prompt:
```
(venv) PS C:\Users\kumar\Pictures\Minor project\chakravyuh-backend>
```

> **IMPORTANT:** You must activate the venv EVERY TIME you open a new terminal.
> If you don't see `(venv)`, your packages won't be found and nothing will work.

---

## 1.5 Install Python Dependencies

With the venv activated (you see `(venv)` in prompt), run:

```powershell
pip install -r backend/requirements.txt
```

This installs:
| Package | What It Does |
|---------|-------------|
| **flask** | Web server framework — creates our REST API |
| **flask-cors** | Allows frontend (browser) to talk to backend (different port) |
| **requests** | HTTP library — we use this to talk to Ollama's local API |
| **python-dotenv** | Loads config from `.env` file |

### Verify installation:

```powershell
pip list
```

You should see all four packages in the list. If any are missing, run the install command again.

---

## 1.6 Verify Project Structure

Run this to see your project structure:

```powershell
Get-ChildItem -Recurse -Name -Exclude venv,.git | Sort-Object
```

**Expected output (should look like this):**
```
.env
.gitignore
backend/
backend/app.py
backend/character_engine.py
backend/config.py
backend/context_manager.py
backend/knowledge/
backend/knowledge/krishna_knowledge.json
backend/llm_client.py
backend/requirements.txt
frontend/
frontend/index.html
frontend/script.js
frontend/style.css
lore_files/
md files/
md files/process.md
md files/research.md
md files/step1.md
md files/version1.md
```

---

## 1.7 Verify .env Configuration

Open `.env` in VS Code and confirm it contains:

```env
OLLAMA_MODEL=gemma3:4b
OLLAMA_BASE_URL=http://localhost:11434
```

> **No API keys needed!** Ollama runs locally. This file just stores which model to use and where Ollama's server is running.

---

## Final Checklist for Step 1

Run through each of these to confirm everything is ready:

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | Ollama installed | `ollama --version` | Version number (e.g., `0.6.x`) |
| 2 | Model downloaded | `ollama list` | Shows `gemma3:4b` |
| 3 | Model responds | `ollama run gemma3:4b "Namaste"` | Gets a response |
| 4 | Venv exists | `Test-Path venv` | `True` |
| 5 | Venv activated | Look at prompt | Shows `(venv)` |
| 6 | Packages installed | `pip list` | Shows flask, flask-cors, requests, python-dotenv |
| 7 | .env exists | `Test-Path .env` | `True` |
| 8 | Project structure | `Get-ChildItem backend -Name` | Shows app.py, config.py, etc. |

---

## Troubleshooting

### "ollama is not recognized as a command"
- Restart VS Code completely (close window, reopen)
- If still failing, restart your PC
- Check that Ollama was installed correctly (look for it in Start Menu)

### "ollama pull" is very slow
- Normal on slow internet — the model is ~3 GB
- You can try the smaller `gemma3:1b` model first (only ~1 GB) to test faster:
  ```powershell
  ollama pull gemma3:1b
  ```
  (You can switch back to `gemma3:4b` later by changing `.env`)

### "python is not recognized"
- Python wasn't added to PATH during installation
- Reinstall Python from [python.org](https://python.org) and CHECK the "Add Python to PATH" box
- Or use `python3` instead of `python`

### Virtual environment won't activate
- If you get a red error about "execution policy", run this ONCE:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
  Then try `.\venv\Scripts\Activate` again

### "pip install" fails with permission error
- Make sure venv is activated (you see `(venv)` in prompt)
- If still failing, try: `python -m pip install -r backend/requirements.txt`

---

## What's Next?

Once all checks pass, tell me **"Step 1 done"** and I'll provide the code for **Step 2: Backend Foundation — Config & Ollama LLM Client**.

In Step 2, we'll write `config.py` and `llm_client.py` — the code that makes our Python backend talk to Ollama.

---

> *"The journey of a thousand miles begins with a single step."*
> Step 1 is your foundation. Get it right, and everything else builds smoothly.
