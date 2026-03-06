# Agent Environment Setup

## Requirements
- Python 3.6 or newer
- The `python` command available in your PATH

## Steps
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the environment (works on all OSes):
   - **Linux / macOS**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (Command Prompt)**
     ```batch
     .venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell)**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
3. Once the environment is active, install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

> Once you install some packages with `pip install`, run `pip freeze > requirements.txt` on this directory to update the depedencies.

---

Happy develop :D