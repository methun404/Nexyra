<div align="center">

# ⚡ NEXYRA
### Next-Gen System Monitor, Process Controller & Automation Suite

[![Linux](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://www.kernel.org/)
[![Electron](https://img.shields.io/badge/Electron-41.0-47848F?style=for-the-badge&logo=electron&logoColor=white)](https://www.electronjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Nexyra</b> is an operating system utility suite for <b>Linux</b>, combining a modern <b>Glassmorphism UI</b> with high-performance <b>FastAPI</b> backend microservices and native <b>POSIX bash automation</b>. Designed for real-time telemetry, automated directory hygiene, process control, and system cleanup.
</p>

---

</div>

## 📑 Table of Contents
- [✨ Key Features](#-key-features)
- [🏛️ System Architecture](#️-system-architecture)
- [📂 Project Structure](#-project-structure)
- [🚀 Quick Start & Installation](#-quick-start--installation)
- [🛠️ Available Scripts](#️-available-scripts)
- [🔌 REST API Reference](#-rest-api-reference)
- [💻 Native OS Automation Scripts](#-native-os-automation-scripts)
- [🐧 Linux Troubleshooting](#-linux-troubleshooting)
- [🔐 Security & Environment Variables](#-security--environment-variables)
- [📜 License](#-license)

---

## ✨ Key Features

- **📊 Real-time Hardware Telemetry**
  - Live CPU core utilization tracking via `top` and `/proc/stat`.
  - Physical memory (RAM) usage and total RAM calculation via `/proc/meminfo` and `free`.
  - Root partition disk usage, available storage, and capacity visualization via `df`.

- **⚡ Process Manager & Task Control**
  - Interactive table of active system processes (PID, Command, %CPU, %MEM).
  - Search and filter processes with real-time refresh.
  - Safe process termination with dual-confirmation modal shields (`SIGKILL / kill -9`).

- **📦 Application Ecosystem Inspector**
  - Deep scan of installed applications via `.desktop` entries in `/usr/share/applications`, `~/.local/share/applications`, Flatpak and Snap export directories.
  - Metadata harvesting from `.desktop` files and the system package manager (`dpkg-query` / `rpm` / `pacman`).
  - Vendor classification (Mozilla, Google, Microsoft, JetBrains, Spotify, GNOME, KDE, etc.).

- **🧹 Automated Storage Hygiene & Junk Cleaner**
  - Live calculation of temporary cache and logs (`~/.cache`, `~/.local/share/Trash`, user-level `.tmp` / `.log` files).
  - One-click safe cache flushing to reclaim disk space.

- **🗂️ Smart File & Workspace Organizer**
  - Automated sorting for congested folders (e.g. `~/Downloads`).
  - Sorts files into structured folders: `Images`, `Documents`, `Archives`, and `Videos`.
  - Live preview of unorganized files with file-type color tagging and file sizes.

- **🎨 Cyberpunk / Glassmorphism Desktop UI**
  - Custom Electron desktop window with smooth 3D CSS cube animation and ambient particle engine.
  - Responsive collapsible sidebar with active status indicators and toast feedback.

---

## 🏛️ System Architecture

```mermaid
graph TD
    subgraph Client["Desktop Presentation Layer (Electron)"]
        UI["Glassmorphism UI (Tailwind CSS + Phosphor Icons)"]
        Splash["3D Cyberpunk Splash Screen (CSS 3D Engine)"]
        Views["Views: Home | Processes | Applications | Organizer"]
        WinMgr["Electron Main Process (Lifecycle & Window Manager)"]
    end

    subgraph IPC["Communication Layer"]
        HTTP["HTTP / REST API (Port 8000)"]
    end

    subgraph Server["Backend Microservice (FastAPI + Uvicorn)"]
        API["FastAPI REST Router"]
        CorsMW["CORS Middleware"]
        Runner["Subprocess Bash Execution Wrapper"]
    end

    subgraph Kernel["Linux Kernel & Native Utilities"]
        SysUtil["System Stats: top, free, /proc, df"]
        ProcUtil["Process Management: ps -eo, kill"]
        AppUtil["App Inspector: find, .desktop files, dpkg/rpm/pacman"]
        FileUtil["Storage Automation: du, find, mv, rm"]
    end

    WinMgr -->|Spawn & Monitor| Server
    Views -->|Fetch Telemetry| HTTP
    HTTP --> API
    API --> Runner
    Runner --> SysUtil
    Runner --> ProcUtil
    Runner --> AppUtil
    Runner --> FileUtil
```

---

## 📂 Project Structure

```text
Nexyra/
├── backend/
│   ├── main.py              # FastAPI server, CORS configuration, API routes
│   └── requirements.txt     # Python dependencies (FastAPI, Uvicorn, etc.)
├── electron/
│   ├── main.js              # Electron app entry point, process lifecycle manager
│   ├── package.json         # Electron dependencies and scripts
│   └── package-lock.json    # Locked node dependency tree
├── frontend/
│   ├── splash_screen/
│   │   └── splash.html      # 3D animated splash screen with particle engine
│   └── views/
│       ├── home.html        # Main telemetry dashboard (CPU, RAM, Disk, System)
│       ├── processes.html   # Real-time task manager & process terminator
│       ├── applications.html# Installed application browser and metadata viewer
│       └── organizer.html   # Smart file organizer & cache junk cleaner
├── scripts/
│   ├── os_tasks/
│   │   ├── applications.sh  # Scans installed applications (.desktop entries)
│   │   ├── clean_junk.sh    # Flushes user cache & logs safely
│   │   ├── kill_process.sh  # Terminates target PID via kill signal
│   │   ├── organizer.sh     # Auto-categorizes files into organized folders
│   │   ├── processes.sh     # Extracts top processes with CPU and RAM %
│   │   ├── setup_demo.sh    # Generates mock files for testing organizer
│   │   └── sys_info.sh      # Gathers hardware metrics from the Linux kernel
│   └── syatem_info/
│       └── get_system_info.sh
├── .env.example             # Example environment template
├── .gitignore               # Strict gitignore protecting secrets and artifacts
├── package.json             # Root workspace runner
└── README.md                # Project documentation
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- **Operating System**: Linux (tested target: Ubuntu / Debian, Fedora, Arch). Features rely on standard Linux tools such as `top`, `free`, `ps`, `df`, `/proc`, and `.desktop` files.
- **Node.js**: v18.0.0 or higher.
- **Python**: v3.10 or higher (with the `venv` module).
- **Desktop environment**: X11 or Wayland session (required to run the Electron window).

Install the basic system packages first:

```bash
# Debian / Ubuntu
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip nodejs npm procps

# Fedora
sudo dnf install -y git python3 python3-pip nodejs npm procps-ng

# Arch
sudo pacman -S --needed git python python-pip nodejs npm procps-ng
```

> 💡 Make sure Node.js is v18+. If your distro ships an older version, install it with [nvm](https://github.com/nvm-sh/nvm) or [NodeSource](https://github.com/nodesource/distributions).

### 1. Clone the Repository
```bash
git clone git@github.com:methun404/Nexyra.git
cd Nexyra
```

### 2. Configure Environment Variables
Copy the template configuration:
```bash
cp .env.example .env
```

### 3. Setup Python Backend Environment
```bash
# Create Python virtual environment inside backend/
python3 -m venv backend/venv

# Activate the virtual environment
source backend/venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 4. Install Electron Dependencies
```bash
npm --prefix electron install
```

### 5. Make the Scripts Executable
```bash
chmod +x scripts/os_tasks/*.sh scripts/syatem_info/*.sh
```

### 6. Launch the Application
Run everything with a single command from the project root:
```bash
npm start
```
*Electron will automatically launch the 3D splash screen, spin up the FastAPI server on `http://127.0.0.1:8000`, verify server health, and transition to the dashboard once ready.*

---

## 🛠️ Available Scripts

From the root project directory:

| Command | Description |
|---|---|
| `npm start` | Launches both the FastAPI backend and the Electron desktop app |
| `npm run electron` | Starts the Electron wrapper directly |
| `npm run backend` | Runs the FastAPI backend in standalone reload mode on port `8000` |

---

## 🔌 REST API Reference

The FastAPI service exposes the following endpoints on `http://127.0.0.1:8000`:

| Method | Endpoint | Description | Sample Output |
|---|---|---|---|
| `GET` | `/` | Service health status check | `{"status": "ok"}` |
| `GET` | `/api/sysinfo` | Real-time CPU, RAM and Disk metrics | `{"cpu":"18.4","ram_used":"7120M","ram_total":"8 GB",...}` |
| `GET` | `/api/processes` | List of top 30 active OS processes | `{"processes":[{"pid":"123","name":"firefox","cpu":"4.2","mem":"2.1"}]}` |
| `POST` | `/api/process/kill/{pid}`| Terminates process by PID | `{"result":"Success"}` |
| `GET` | `/api/apps` | Installed applications and metadata | `{"applications":[{"name":"Slack","publisher":"Slack","version":"4.38"}]}` |
| `GET` | `/api/junk/size` | Calculates safe-to-clean junk size | `{"size_gb":"2.4 GB","raw_bytes":2576980377}` |
| `POST` | `/api/clean` | Flushes user caches and log buffers | `{"status":"success","message":"System Cleanup Finished"}` |
| `GET` | `/api/files/unorganized` | Scans files waiting in `~/Downloads` | `{"files":[...],"path":"/home/<user>/Downloads"}` |
| `POST` | `/api/organize` | Sorts Downloads files into categories | `{"status":"success","message":"Organized /home/<user>/Downloads"}` |

---

## 💻 Native OS Automation Scripts

All backend routes execute hardened bash scripts located in `scripts/os_tasks/`:

- **`sys_info.sh`**: Interrogates `top -bn1`, `/proc/meminfo` (or `free -b`), `nproc`, and `df -h /` to parse real hardware loads.
- **`processes.sh`**: Runs `ps -eo pid,pcpu,pmem,comm --sort=-pcpu` with awk formatting for reliable delimiter parsing.
- **`kill_process.sh`**: Dispatches `kill -9` with safety parameter validation.
- **`applications.sh`**: Reads `.desktop` entries from `/usr/share/applications`, `~/.local/share/applications`, `/var/lib/flatpak/exports/share/applications`, and `/var/lib/snapd/desktop/applications`, and resolves versions through `dpkg-query`, `rpm`, or `pacman` when available.
- **`clean_junk.sh`**: Safely cleans temporary `.tmp` and `.log` files, with dedicated cleanup routines for `~/.cache` and `~/.local/share/Trash`.
- **`organizer.sh`**: Uses shell case-insensitive globbing (`nocaseglob`) to sort extensions (`jpg`, `pdf`, `zip`, `mp4`, etc.) into categorized sub-folders without overwriting data.
- **`setup_demo.sh`**: Generates a sandboxed `test_workspace/` directory with test assets to demonstrate organizer and cleaning tasks without touching personal files.

---

## 🐧 Linux Troubleshooting

| Problem | Fix |
|---|---|
| `The SUID sandbox helper binary was found, but is not configured correctly` | Run Electron with `--no-sandbox` for development, or fix `chrome-sandbox` permissions: `sudo chown root electron/node_modules/electron/dist/chrome-sandbox && sudo chmod 4755 electron/node_modules/electron/dist/chrome-sandbox` |
| `error while loading shared libraries: libgtk-3.so.0` / `libnss3.so` | Install Electron runtime libraries: `sudo apt install -y libgtk-3-0 libnss3 libasound2 libgbm1` |
| `python3 -m venv` fails | Install the venv module: `sudo apt install python3-venv` |
| `Permission denied` when running scripts | Run `chmod +x scripts/os_tasks/*.sh` |
| Port `8000` already in use | Stop the other service (`ss -ltnp \| grep 8000`) or change the port in `.env` |
| Window does not open over SSH / headless | Electron needs a graphical session (X11/Wayland); use a local desktop or `xvfb-run npm start` |

---

## 🔐 Security & Environment Variables

- `.env` files containing secrets or private tokens are strictly ignored by `.gitignore`.
- Destructive actions (killing processes, wiping cache directories, or moving files) require user confirmation through modal dialogs in the UI.
- All process calls avoid shell injection by sanitizing path inputs and executing scripts with fixed bash flags.
- Nexyra runs with your user's permissions. Killing processes owned by other users or `root` will fail unless the app is run with elevated privileges, which is not recommended.

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute as per the license conditions.

---

<div align="center">
  <b>Developed by Methun Ahmed</b><br>
  Built with passion for OS telemetry and desktop engineering.
</div>
