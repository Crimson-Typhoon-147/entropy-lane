#!/bin/bash

echo "=========================================="
echo "[EntropyLane] Automated Demo Launcher"
echo "=========================================="

BACKEND_PORT=8000
FRONTEND_DIR="frontend"
ENV_FILE="$FRONTEND_DIR/.env.local"

BACKEND_LOG="cloudflare-backend.log"
FRONTEND_LOG="cloudflare-frontend.log"
VITE_LOG="vite.log"

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
uvicorn api.main:app --reload > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..

echo "[*] Waiting for backend to stabilize..."
sleep 5

# ---------------- BACKEND TUNNEL ----------------
echo "[2/6] Starting Cloudflare tunnel (backend)..."
cloudflared tunnel --url http://127.0.0.1:$BACKEND_PORT > $BACKEND_LOG 2>&1 &
BACKEND_TUNNEL_PID=$!

echo "[*] Waiting for backend tunnel..."
sleep 8

BACKEND_URL=$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' $BACKEND_LOG | head -n 1)

if [ -z "$BACKEND_URL" ]; then
  echo "[ERROR] Backend tunnel failed"
  cat $BACKEND_LOG
  cleanup
fi

echo "[+] Backend URL: $BACKEND_URL"

# ---------------- FRONTEND ENV ----------------
echo "[3/6] Updating frontend environment..."
echo "VITE_API_BASE=$BACKEND_URL" > $ENV_FILE

# ---------------- FRONTEND ----------------
echo "[4/6] Starting frontend..."
cd $FRONTEND_DIR || exit
npm run dev > ../$VITE_LOG 2>&1 &
FRONTEND_PID=$!
cd ..

echo "[*] Waiting for Vite..."
sleep 6

FRONTEND_PORT=$(grep -Eo 'localhost:[0-9]+' $VITE_LOG | cut -d: -f2 | tail -n 1)

if [ -z "$FRONTEND_PORT" ]; then
  echo "[ERROR] Could not detect frontend port"
  cat $VITE_LOG
  cleanup
fi

echo "[+] Frontend running on port: $FRONTEND_PORT"

# ---------------- FRONTEND TUNNEL ----------------
echo "[5/6] Starting Cloudflare tunnel (frontend)..."
cloudflared tunnel --url http://127.0.0.1:$FRONTEND_PORT > $FRONTEND_LOG 2>&1 &
FRONTEND_TUNNEL_PID=$!

echo "[*] Waiting for frontend tunnel..."
sleep 8

FRONTEND_URL=$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' $FRONTEND_LOG | head -n 1)

if [ -z "$FRONTEND_URL" ]; then
  echo "[ERROR] Frontend tunnel failed"
  cat $FRONTEND_LOG
  cleanup
fi

# ---------------- OUTPUT ----------------
echo ""
echo "=========================================="
echo "✅ DEMO READY"
echo "🌍 Open this URL on ANY DEVICE:"
echo ""
echo "👉  $FRONTEND_URL"
echo ""
echo "📱 Scan QR:"
echo ""

qrencode -t ANSIUTF8 "$FRONTEND_URL"

echo ""
echo "=========================================="
echo "Press Ctrl+C to stop everything."

wait