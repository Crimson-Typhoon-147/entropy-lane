#!/bin/bash

echo "=========================================="
echo "[EntropyLane] Automated Demo Launcher"
echo "=========================================="

# ---------------- CONFIG ----------------
BACKEND_PORT=8000
FRONTEND_DIR="frontend"
ENV_FILE="$FRONTEND_DIR/.env.local"

BACKEND_LOG="cloudflare-backend.log"
FRONTEND_LOG="cloudflare-frontend.log"
VITE_LOG="vite.log"

# ---------------- CLEANUP ----------------
cleanup() {
  echo ""
  echo "[*] Shutting down demo environment..."
  kill $BACKEND_PID $BACKEND_TUNNEL_PID $FRONTEND_TUNNEL_PID 2>/dev/null
  exit 0
}
trap cleanup INT TERM

# ---------------- BACKEND ----------------
echo "[1/6] Starting FastAPI backend..."
cd backend || exit
python3 -m uvicorn api.main:app --reload > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..
sleep 3

# ---------------- BACKEND TUNNEL ----------------
echo "[2/6] Starting Cloudflare tunnel (backend)..."
cloudflared --url http://127.0.0.1:$BACKEND_PORT > $BACKEND_LOG 2>&1 &
BACKEND_TUNNEL_PID=$!

sleep 6
BACKEND_URL=$(grep -o 'https://[-a-z0-9]*\.trycloudflare.com' $BACKEND_LOG | head -n 1)

if [ -z "$BACKEND_URL" ]; then
  echo "[ERROR] Failed to detect backend tunnel URL"
  cleanup
fi

echo "[+] Backend URL: $BACKEND_URL"

# ---------------- FRONTEND ENV ----------------
echo "[3/6] Updating frontend environment..."
echo "VITE_API_BASE=$BACKEND_URL" > $ENV_FILE

# ---------------- FRONTEND ----------------
echo "[4/6] Starting frontend (Vite)..."
cd $FRONTEND_DIR || exit
npm run dev > ../$VITE_LOG 2>&1 &
FRONTEND_PID=$!
cd ..

sleep 4

# ---------------- DETECT FRONTEND PORT ----------------
FRONTEND_PORT=$(grep -oE 'http://localhost:[0-9]+' $VITE_LOG | tail -n 1 | cut -d: -f3)

if [ -z "$FRONTEND_PORT" ]; then
  echo "[ERROR] Failed to detect frontend port"
  cleanup
fi

echo "[+] Frontend running on port: $FRONTEND_PORT"

# ---------------- FRONTEND TUNNEL ----------------
echo "[5/6] Starting Cloudflare tunnel (frontend)..."
cloudflared --url http://localhost:$FRONTEND_PORT > $FRONTEND_LOG 2>&1 &
FRONTEND_TUNNEL_PID=$!

sleep 6
FRONTEND_URL=$(grep -o 'https://[-a-z0-9]*\.trycloudflare.com' $FRONTEND_LOG | head -n 1)

if [ -z "$FRONTEND_URL" ]; then
  echo "[ERROR] Failed to detect frontend tunnel URL"
  cleanup
fi

# ---------------- QR DISPLAY ONLY ----------------
echo ""
echo "=========================================="
echo "✅ DEMO READY"
echo "🌍 Open this URL on ANY DEVICE:"
echo ""
echo "👉  $FRONTEND_URL"
echo ""
echo "📱 Scan this QR to join instantly:"
echo ""

# Terminal-only QR (no file saved)
qrencode -t ANSIUTF8 "$FRONTEND_URL"

echo ""
echo "=========================================="
echo "Press Ctrl+C to stop everything."

wait
