from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "os_tasks")

def run_script(script_name, args=None):
    if args is None:
        args = []
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    result = subprocess.run(["/bin/bash", script_path] + args, capture_output=True, text=True)
    return result.stdout.strip()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/sysinfo")
def get_sysinfo():
    output = run_script("sys_info.sh")
    parts = output.split(",")
    # Expected format: CPU,RAM_USED,RAM_TOTAL,DISK_USED,DISK_TOTAL,DISK_PCT
    if len(parts) >= 6:
        return {
            "cpu": parts[0],
            "ram_used": parts[1],
            "ram_total": parts[2],
            "disk_used": parts[3],
            "disk_total": parts[4],
            "disk_pct": parts[5]
        }
    return {"error": "Failed to parse", "raw": output}

@app.get("/api/processes")
def get_processes():
    output = run_script("processes.sh")
    lines = output.split("\n")
    procs = []
    for line in lines:
        if line.strip():
            parts = line.split(",")
            if len(parts) >= 4:
                procs.append({
                    "pid": parts[0],
                    "name": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3]
                })
    return {"processes": procs}

@app.post("/api/process/kill/{pid}")
def kill_process(pid: str):
    output = run_script("kill_process.sh", [pid])
    return {"result": output}

@app.get("/api/apps")
def get_apps():
    output = run_script("applications.sh")
    lines = output.split("\n")
    
    app_data = []
    for line in lines:
        app_path = line.strip()
        if not app_path or not app_path.endswith(".app"): continue
        
        # Extract base name (e.g., Google Chrome)
        name = os.path.basename(app_path).replace(".app", "")
        
        # Real Metadata Fetching
        version = "Unknown"
        try:
            # CFBundleShortVersionString is the typical user-visible version
            ver_cmd = ["defaults", "read", f"{app_path}/Contents/Info.plist", "CFBundleShortVersionString"]
            version = subprocess.check_output(ver_cmd, text=True, stderr=subprocess.DEVNULL).strip()
        except:
            pass
            
        # Categorize icons
        icon = "ph-app-window"
        publisher = "Apple Inc."
        
        lower_name = name.lower()
        if "google" in lower_name or "chrome" in lower_name: 
            icon = "ph-google-chrome-logo"; publisher = "Google LLC"
        elif "code" in lower_name or "studio" in lower_name: 
            icon = "ph-code"; publisher = "Microsoft / JetBrains"
        elif "adobe" in lower_name: 
            icon = "ph-paint-brush"; publisher = "Adobe Inc."
        elif "safari" in lower_name or "mail" in lower_name: 
            icon = "ph-globe"; publisher = "Apple Inc."
        elif "spotify" in lower_name:
            icon = "ph-music-notes"; publisher = "Spotify AB"
        
        app_data.append({
            "name": name,
            "icon": icon,
            "publisher": publisher,
            "version": version,
            "size": "N/A" # Getting folder size is slow, skip for now
        })
        
    return {"applications": app_data}

@app.post("/api/organize")
def organize():
    # Real target: Downloads folder
    target = os.path.expanduser("~/Downloads")
    output = run_script("organizer.sh", [target])
    return {"status": "success", "message": f"Organized {target}", "details": output}

@app.post("/api/clean")
def clean():
    # Real targets: User Cache and Logs
    home = os.path.expanduser("~")
    targets = [
        os.path.join(home, "Library/Caches"),
        os.path.join(home, "Library/Logs")
    ]
    
    results = []
    for t in targets:
        if os.path.exists(t):
            res = run_script("clean_junk.sh", [t])
            results.append(f"{t}: {res}")
            
    return {"status": "success", "message": "System Cleanup Finished", "details": results}

@app.get("/api/junk/size")
def get_junk_size():
    home = os.path.expanduser("~")
    # Quick shell-based size calculation for speed on big folders
    cmd = f"du -sk {home}/Library/Caches {home}/Library/Logs 2>/dev/null | awk '{{sum+=$1}} END {{print sum}}'"
    try:
        raw_kb = subprocess.check_output(cmd, shell=True, text=True).strip()
        kb_size = int(raw_kb) if raw_kb else 0
        gb_size = kb_size / (1024 * 1024)
        return {"size_gb": f"{gb_size:.1f} GB", "raw_bytes": kb_size * 1024}
    except:
        return {"size_gb": "0.0 GB", "raw_bytes": 0}

@app.get("/api/files/unorganized")
def get_unorganized_files():
    target = os.path.expanduser("~/Downloads")
    if not os.path.exists(target):
        return {"files": []}
        
    files = []
    # Only list top-level files for simplicity
    try:
        for f in os.listdir(target):
            fp = os.path.join(target, f)
            if os.path.isfile(fp) and not f.startswith("."):
                stats = os.stat(fp)
                # Determine icon based on extension
                ext = f.split(".")[-1].lower() if "." in f else ""
                icon = "ph-file"
                color = "text-gray-400"
                
                if ext in ["jpg", "jpeg", "png", "gif"]: icon = "ph-fill ph-image"; color = "text-yellow-400"
                elif ext in ["pdf", "doc", "docx"]: icon = "ph-fill ph-file-pdf"; color = "text-red-400"
                elif ext in ["zip", "rar", "7z"]: icon = "ph-fill ph-file-archive"; color = "text-purple-400"
                elif ext in ["mp4", "mov"]: icon = "ph-fill ph-file-video"; color = "text-blue-400"
                elif ext in ["js", "py", "sh", "html"]: icon = "ph-fill ph-file-code"; color = "text-green-400"
                
                files.append({
                    "name": f,
                    "icon": icon,
                    "color": color,
                    "size": f"{stats.st_size / (1024*1024):.1f} MB",
                    "time": "Recent"
                })
    except:
        pass
    return {"files": [f for f in files if f is not None], "path": target}