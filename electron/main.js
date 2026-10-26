const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const http = require("http");

let backendProcess;

// 🔹 Helper function to enforce a minimum wait time (for splash screen)
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// 🔹 Start FastAPI backend
function startBackend() {
  return new Promise((resolve, reject) => {
    let resolved = false;

    backendProcess = spawn(
      "bash",
      [
        "-c",
        "cd ../backend && ( [ -d venv ] && source venv/bin/activate || [ -d .venv ] && source .venv/bin/activate || true ) && exec uvicorn main:app --host 127.0.0.1 --port 8000",
      ],
      {
        cwd: __dirname,
      },
    );

    function checkStartup(data, streamName) {
      const msg = data.toString();
      console.log(`Backend (${streamName}):`, msg);

      if (!resolved && (msg.includes("Uvicorn running") || msg.includes("Application startup complete"))) {
        resolved = true;
        resolve();
      }
    }

    backendProcess.stdout.on("data", (data) => checkStartup(data, "stdout"));
    backendProcess.stderr.on("data", (data) => checkStartup(data, "stderr"));

    backendProcess.on("error", (err) => {
      if (!resolved) {
        resolved = true;
        reject(err);
      }
    });

    // Fallback: If 3 seconds pass without error, allow waitForBackend to check HTTP
    setTimeout(() => {
      if (!resolved) {
        resolved = true;
        resolve();
      }
    }, 3000);
  });
}

// 🔹 Wait until backend is reachable
function waitForBackend(url, timeout = 15000) {
  const startTime = Date.now();

  return new Promise((resolve, reject) => {
    function check() {
      http
        .get(url, (res) => {
          resolve();
        })
        .on("error", () => {
          if (Date.now() - startTime > timeout) {
            reject(new Error("Backend failed to start within timeout"));
          } else {
            setTimeout(check, 500);
          }
        });
    }
    check();
  });
}

// 🔹 Create Electron window
function createWindow() {
  const win = new BrowserWindow({
    width: 900,
    height: 600,
    show: true,
  });

  const splashPath = path.join(
    __dirname,
    "../frontend/splash_screen/splash.html",
  );

  // 🛠️ FIX 2: Correct path to the dashboard folder
  const mainPath = path.join(__dirname, "../frontend/views/home.html");

  // Load splash screen first
  win.loadFile(splashPath);

  console.log("Starting backend and waiting for splash screen animation...");

  // 🛠️ FIX 3: Wait for BOTH backend to be ready AND 6 seconds to pass
  Promise.all([
    startBackend().then(() => waitForBackend("http://127.0.0.1:8000")),
    delay(6000), // Waits exactly 6 seconds (5s splash + 1s fade out)
  ])
    .then(() => {
      console.log("✅ Backend is ready & Splash finished");
      win.loadFile(mainPath);
    })
    .catch((err) => {
      console.error("❌ Startup error:", err);
    });
}

// 🔹 App lifecycle
app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

// 🔹 Kill backend when app exits
app.on("before-quit", () => {
  if (backendProcess) {
    console.log("Stopping backend...");
    backendProcess.kill();
  }
});
