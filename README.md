# Password Manager

This is a high-security local credential management system designed to safely store, manage, and retrieve credentials. Leveraging industry-standard, robust cryptographic algorithms, it provides complete confidentiality, integrity, and authenticity for your private vault data, all without relying on third-party cloud hosting.

The application features a **desktop graphical interface (GUI)** using `pywebview`, a standalone **interactive Command Line Interface (CLI)**, and secure **Multi-Factor Authentication (MFA)** using Time-Based One-Time Passwords (TOTP).

---

## Key Features

*   **Secure Local Vault (AES-GCM)**: All credentials are encrypted locally with AES-256-GCM (Authenticated Encryption with Associated Data), ensuring absolute privacy and data integrity.
*   **Argon2 Key Derivation**: High-security master key derivation using Argon2id, configured with memory-hard, multi-threaded parameters to safeguard against brute-force attacks.
*   **Deterministic Password Generator**: Generates strong, unique, and reproducible site-specific passwords using HMAC-SHA256 based on your master password and site name. No storage required!
*   **Multi-Factor Authentication (MFA)**: Built-in support for Time-Based One-Time Passwords (TOTP) that links seamlessly to Google Authenticator, Authy, or any compatible authentication app.
*   **Dual Interface Options**:
    *   **Desktop GUI Portal**: A sleek, intuitive desktop interface running a Flask server inside a native window via `pywebview`.
    *   **Interactive CLI Tool**: A direct terminal-based shell for command-line efficiency.
*   **Standalone Executable**: Build script included to package the application into a single-file portable desktop executable.

---

## Cryptographic Architecture

*   **Master Key Derivation**: Argon2id KDF is applied to the master password with a unique, cryptographically secure random 16-byte salt to derive the Master Key ($MK$).
*   **Key Expansion (HKDF)**: HKDF-SHA256 is used to expand $MK$ into unique, isolated subkeys:
    *   `vault key` ($K_v$): For AES-256-GCM vault encryption and decryption.
    *   `auth verification key`: For verifying the master password locally without exposing it.
    *   `file mac key`: Generates a SHA256 HMAC signature of the entire vault file (`userData.json`) to detect tamper/corruption.
    *   `auth key`: Encrypts/decrypts the MFA seed bytes using AES-GCM before saving them to disk.
*   **Data Integrity Check**: Any modification to `userData.json` outside the app is immediately detected via the integrity MAC check, preventing unauthorized offline edits.
*   **File Isolation & Write Safety**: Vault writes use an atomic operation (writing to a temporary file first, then replacing) and a local file lock (`userData.json.lock`) to prevent concurrent write collisions.

---

## Project Structure

```text
├── spm.py                # Core cryptolib & CLI client
├── app.py                # Flask Web API server & pywebview entrypoint
├── desktop.py            # Secondary webview launcher
├── templates/            # HTML templates for the Web GUI
├── static/               # CSS styles, JS assets, and icons
├── verify_api.py         # Integration tests for Flask REST API
├── verify_mfa.py         # Integration tests for MFA flow
├── build.sh              # Bash script to package app via PyInstaller
├── app.spec              # PyInstaller configuration file
├── requirements.txt      # Python library dependencies
└── userData.json         # Encrypted database (created on registration)
```

## Installation & Setup

### Prerequisites
*   **Python 3.8+** must be installed.
*   **pip** package manager.

### 1. Clone the Repository
```bash
git clone https://github.com/ItsMinni1/Password-manager.git
cd Password-manager
```

### 2. Create and Activate a Virtual Environment (Recommended)
Creating an isolated environment prevents dependency conflicts:
```bash
# Create the environment
python3 -m venv venv

# Activate it (Linux/macOS)
source venv/bin/activate

# Activate it (Windows)
# venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries specified in `requirements.txt` along with graphical dependencies:
```bash
pip install -r requirements.txt
pip install pywebview pyinstaller
```

---

## 运行 / Running the Application

Minni Password Manager can be launched in two primary modes:

### Mode A: Desktop Graphical Interface (GUI)
This launches a backend Flask API server and opens the frontend UI inside a native webview container:
```bash
python app.py
```
> [!NOTE]
> **Automatic Browser Fallback**: If the desktop GUI components (`pywebview` graphical backends) are not present on your system or you are running in a headless/SSH session, the application will **automatically fall back to browser-only mode** and run a local server at `http://127.0.0.1:5000/`.
> 
> **To enable the native desktop GUI window**, ensure you have a Python graphical library installed in your virtual environment. You can install `PyQt5` (which bundles all required GUI packages) by running:
> ```bash
> pip install PyQt5
> ```


### Mode B: Interactive Terminal (CLI)
This launches the lightweight interactive terminal client. This mode does not require any graphical dependencies:
```bash
python spm.py
```
Inside the CLI, you can register, login, view, copy passwords directly to your clipboard, generate deterministic passwords, and toggle TOTP MFA.

---

## 🧪 Integration & Verification Tests

Ensure all components and APIs are functioning flawlessly by running the integrated verification scripts:

1.  **Test the Core REST APIs** (Registration, Login, Adding & Retrieving Entries):
    ```bash
    python verify_api.py
    ```
2.  **Test the MFA Flow** (TOTP Setup, Enabling, Disabling, and Relogin Checks):
    ```bash
    python verify_mfa.py
    ```

---

## Building a Standalone Executable

You can bundle Minni Password Manager into a single-file portable desktop executable (no Python installation required on the target machine!).

### On Linux / macOS:
Make the build script executable and run it:
```bash
chmod +x build.sh
./build.sh
```

### On Windows / Manual Build:
Run PyInstaller directly with the `.spec` file:
```bash
pyinstaller app.spec
```

Once completed, the standalone application can be found in the newly created **`dist/`** directory.

---

## ⚠️ Security Notes & Production Limitations

This project is tailored for **desktop deployment and academic/educational security purposes**. When using it, keep the following constraints in mind:

1.  **Local Storage Security**: The safety of your vault relies entirely on the strength of your **master password**. Choose a password with at least 12+ characters containing symbols, digits, and mixed-case letters.
2.  **Lack of Network HTTPS**: The Flask backend serves local requests over HTTP. While acceptable for a closed local webview or localhost browser, this server should **never** be exposed directly to a public network without reverse proxying (e.g., Nginx) and TLS configuration.
3.  **In-Memory Session Limits**: Active tokens and MFA steps are kept in-memory (`SESSIONS` and `PENDING_MFA`). High availability, multi-process WSGI hosting, or node failovers will require migrating these structures to database/caching engines (e.g., Redis).

# Screenshots
## Main Screen
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/79929185-420e-432a-a78e-5e03b044b599" />

## User Registration
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/f762fdf0-3ce2-4f12-9f2e-b3f626a298a4" />

## User Login
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/94d00595-bb1c-4299-ac50-1e22419be4f0" />

## Main Screen
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/40174799-1d37-4b17-9886-922f7f71d342" />

## Mode A: Deterministic Password Generator
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/ea824005-047f-4a8c-a785-65c22db57461" />

## Computed Password
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/a0ad9ff2-2d71-4ee1-b56d-fd69891d7655" />

## Screen for Mode B: Secure Vault Storage
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/59e6d8cf-c6a5-4b3a-83e2-4155a828e059" />

## Adding an entry to the Vault
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/971b8f1f-5c3b-48fa-ae52-1f4ef5a50047" />

## Added entry
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/3fb424f6-6266-4953-b81b-f5e52f9bd9a8" />

## Multi-Factor Authentication Configuration Screen
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/70bbaea0-1185-4056-9306-d4a5717b379b" />

## Time-Based OTP Seed 
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/61562581-d219-44e2-b6f9-1276269bcdcd" />
## Logout Functionality
<img width="1837" height="964" alt="image" src="https://github.com/user-attachments/assets/fe08ca2d-9dbe-42f7-9331-fb86e4480011" />


