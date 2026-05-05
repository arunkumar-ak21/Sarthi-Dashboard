# How to Run the Sarthi NLP System

> Follow these 3 simple steps every time you want to start the project.

---

### Step 1: Start Ollama (The AI Engine)
First, make sure the local AI is running.
1. Open a terminal (or normal Command Prompt/PowerShell).
2. Type: `ollama serve`
*(If it says "Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address", it means Ollama is already running in the background, which is perfectly fine!)*

### Step 2: Start the Backend Server (Flask)
This connects the AI to the website.
1. Open a terminal in VS Code (`Ctrl + ~`).
2. Make sure you are in the project folder:
   ```powershell
   cd "C:\Users\kumar\Pictures\Minor project\chakravyuh-backend"
   ```
3. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate
   ```
   *(You should see `(venv)` appear at the start of your command line).*
4. Move to the backend folder and start the server:
   ```powershell
   cd backend
   python app.py
   ```
   *(Leave this terminal open! If you close it, the server stops).*

### Step 3: Open the Dashboard (Frontend)
1. Open File Explorer and go to your project folder: `C:\Users\kumar\Pictures\Minor project\chakravyuh-backend\frontend`
2. Double-click the **`index.html`** file to open it in your browser (Chrome/Edge).
3. Alternatively, if you have the "Live Server" extension in VS Code, right-click `index.html` and select **"Open with Live Server"**.

---

### Troubleshooting
- **"Connection Error" / "Failed to fetch" on the website:** Your backend server isn't running. Do Step 2.
- **Backend starts but gives Ollama connection errors:** Your Ollama isn't running. Do Step 1.
- **Want to close the server?** Go to the VS Code terminal running `python app.py` and press `Ctrl + C`.
